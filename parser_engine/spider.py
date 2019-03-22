import copy
import six
import simplejson as json
import logging

import scrapy
from scrapy.http import Request, HtmlResponse
from scrapy.utils.spider import iterate_spider_output
from scrapy.spiders import Spider, Rule, CrawlSpider
from scrapy.spiders.crawl import identity
from scrapy.linkextractors import LinkExtractor
from scrapy_redis.spiders import RedisCrawlSpider
from scrapy_redis import defaults

from .request import TaskRequest
from .parser import PEParser
from .template import PETemplate

default_link_extractor = LinkExtractor()


class PERule(Rule):

    def __init__(self, template, link_extractor=default_link_extractor, callback=None, cb_kwargs=None, follow=None,
                 process_links=None,
                 process_request=identity):
        """

        :param template:
        :param link_extractor:
        :param callback:
        :param cb_kwargs:
        :param follow:
        :param process_links:
        :param process_request:
        """
        super(PERule, self).__init__(link_extractor, callback, cb_kwargs, follow, process_links, process_request)
        if isinstance(template, PETemplate):
            self.template = template
        else:
            self.template = PETemplate.from_json(template)

    def __str__(self):
        return '<PERule> template：' + str(self.template)


class PECrawlSpider(Spider):
    # subclass should init rules before call super init
    rules = ()
    start_rule = None

    def __init__(self, *a, **kw):
        super(PECrawlSpider, self).__init__(*a, **kw)
        self._compile_rules()

    def start_requests(self):
        if self.start_rule:
            for start_url in self.start_urls:
                r = Request(start_url, callback=self._response_downloaded)
                r.meta.update(rule=-1)
                yield r
        else:
            for req in super().start_requests():
                yield req

    def parse(self, response):
        # never reached now
        return self._parse_response(response, self.parse_start_url, None, cb_kwargs={}, follow=True)

    # @Override
    def parse_start_url(self, response):
        """
        @Override
        :param response:
        :return:
        """
        return []

    # @Override
    def process_results(self, response, results):
        return results

    def _build_request(self, rule_index, link):
        r = Request(url=link.url, callback=self._response_downloaded)
        r.meta.update(rule=rule_index, link_text=link.text)
        return r

    def _requests_to_follow(self, response):
        if not isinstance(response, HtmlResponse):
            # todo
            print("response type", type(response))
            return
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = self._build_request(n, link)
                yield rule.process_request(r)

    def _response_downloaded(self, response):
        rule = self._rules[response.meta['rule']]
        parser = getattr(rule, "parser", None)
        if not parser:
            parser = rule.callback
            callback = None
        else:
            callback = rule.callback
        return self._parse_response(response, parser, callback, rule.cb_kwargs, rule.follow)

    def _parse_response(self, response, parser, callback, cb_kwargs, follow=True):
        if parser:
            cb_res = parser(response, **cb_kwargs) or ()
            if callback:
                cb_res = callback(response, **cb_kwargs) or ()
            cb_res = self.process_results(response, cb_res)
            for requests_or_item in iterate_spider_output(cb_res):
                yield requests_or_item
        if follow and self._follow_links:
            for request_or_item in self._requests_to_follow(response):
                yield request_or_item

    def _compile_rules(self):
        def get_method(method):
            if callable(method):
                return method
            elif isinstance(method, six.string_types):
                return getattr(self, method, None)

        self._rules = [copy.copy(r) for r in self.rules]
        if self.start_rule:
            self._rules.append(self.start_rule)
        for rule in self._rules:
            # use template driven callback processor
            if getattr(rule, "template", None):
                rule.parser = get_method(PEParser(rule.template))
            rule.callback = get_method(rule.callback)
            rule.process_links = get_method(rule.process_links)
            rule.process_request = get_method(rule.process_request)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(PECrawlSpider, cls).from_crawler(crawler, *args, **kwargs)
        spider._follow_links = crawler.settings.getbool(
            'CRAWLSPIDER_FOLLOW_LINKS', True)
        return spider

    def set_crawler(self, crawler):
        super(PECrawlSpider, self).set_crawler(crawler)
        self._follow_links = crawler.settings.getbool('CRAWLSPIDER_FOLLOW_LINKS', True)


class PESpider(RedisCrawlSpider):

    def __init__(self, *args, **kwargs):
        super(PESpider, self).__init__(*args, **kwargs)
        self.project = self.get_project_name()

    def make_request_from_data(self, data):
        try:
            scheduled = TaskRequest(
                **json.loads(data.decode(self.redis_encoding))
            )
        except Exception as e:
            self.debug("parse request failed, exception:【%s】 data: %s" % (e, data.decode(self.redis_encoding)))
        else:
            return self.task_to_request(scheduled)

    @staticmethod
    def task_to_request(scheduled):
        return scrapy.Request(
            url=scheduled.url,
            method=scheduled.method,
            body=scheduled.body,
            cookies=scheduled.cookies,
            headers=scheduled.headers,
            meta=scheduled.meta,
            dont_filter=True
        )

    @staticmethod
    def request_to_task(request):
        request.headers[b'Cookie'] = None
        return TaskRequest(url=request.url, method=request.method,
                           body=request.body, headers=request.headers, cookies=None, meta=request.meta)

    def schedule_next_requests(self):
        for request in self.next_requests():
            self.crawler.engine.crawl(request, spider=self)

    def repush_request(self, request):
        self.route_task(
            "%s:%s:start_urls" % (request.meta.get('project', self.project), request.meta.get('spider', self.name)),
            self.request_to_task(request))

    def get_project_name(self):
        return self.settings.get("BOT_NAME")

    def route_task(self, queue_key, task_request):
        """
        push TaskRequest instance to redis queue
        :param queue_key: redis key
        :param task_request: TaskRequest instance
        :return:
        """
        self.info("push queue: %s， meta: %s" % (queue_key, task_request.meta))
        use_set = self.settings.getbool('REDIS_START_URLS_AS_SET', defaults.START_URLS_AS_SET)
        router = self.server.sadd if use_set else self.server.lpush
        router(queue_key, json.dumps(task_request))

    def add_task(self, task):
        """
        push TaskRequest instance to redis queue of this spider
        :param task:
        :return:
        """
        self.server.lpush(self.redis_key, json.dumps(task))

    def log(self, message, level=logging.DEBUG, **kw):
        """
        TODO
        :param message:
        :param level:
        :param kw:
        :return:
        """
        super().log(message, level, **kw)

    def info(self, message, **kw):
        self.log(message, logging.INFO, **kw)

    def debug(self, message, **kw):
        self.log(message, logging.DEBUG, **kw)

    def error(self, message, **kw):
        self.log(message, logging.ERROR, **kw)
