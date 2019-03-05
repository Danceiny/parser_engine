from scrapy.spiders import Rule, CrawlSpider
from scrapy_redis.spiders import RedisSpider
from scrapy.linkextractors import LinkExtractor
from .template import PETemplate
from .parser import parse_with_tpl
from .utils import is_sequence, load_config_data, classproperty
from .spider import PECrawlSpider


def parse_with_tpl_id(response, tpl_id, **context):
    """
    todo: this method called `inside` scrapy, which means settings of scrapy should be accessible
    :param response:
    :param tpl_id:
    :param context:
    :return:
    """
    return parse_with_tpl(response, PETemplate.from_json(find_by_id(tpl_id)), **context)


def find_by_id(tpl_id):
    """
    todo: improve query performance
    :param tpl_id:
    :return:
    """
    for tpl in Template.config_data['templates']:
        if tpl.get('name') == tpl_id:
            return tpl
    return tpl_id


class Template(object):
    # should implements
    # def find_by_id(tpl_id):
    #     return dict()
    src = None

    _config_data = None

    @classproperty
    def config_data(cls):
        if not cls._config_data:
            cls._config_data = load_config_data()
        return cls._config_data

    @classmethod
    def get_rules(cls, tpl_ids, **kwargs):
        if not tpl_ids:
            return ()
        if not is_sequence(tpl_ids):
            tpl_ids = [tpl_ids]
        if cls.src:
            rules = [cls.get_rule(cls.src.find_by_id(tpl_id), **kwargs) for tpl_id in tpl_ids]
        else:
            rules = []
            for tpl_id in tpl_ids:
                rules.append(cls.get_rule_v2(tpl_id, **kwargs))
        return rules

    @classmethod
    def get_rule_v2(cls, tpl_id, **kwargs):
        kwargs['tpl_id'] = tpl_id
        return Rule(LinkExtractor(), callback=parse_with_tpl_id, cb_kwargs=kwargs)

    @classmethod
    def get_rule(cls, tpl, **kwargs):
        kwargs['tpl'] = tpl
        if not isinstance(tpl, PETemplate):
            tpl = PETemplate.from_json(tpl)
        return Rule(LinkExtractor(allow=tpl.get('allow')), callback=parse_with_tpl, cb_kwargs=kwargs)

    @classmethod
    def PageTemplate(cls, tpl_ids=None, **kw):
        """
        will assign a method, which named `_parse`, to the decorated cls,
        and you can use it like this:
            @Singleton
            class DataSourse:
                def find_by_id(tpl_id):
                    return {} # do query

            @TemplateAnnotation(src=DataSource(), start_url_tpl_id="tpl_id_0", channel="gaode",
                                start_urls_generator="get_start_urls")
            class SpiderA(CrawlSpider):
                name = "spider_a"
                def get_start_urls(self):
                    return ["http://example.org"]

                def parse(self, response):
                    items = self._parse(response)
                    if items:
                        for item in items:
                            yield item

            # when you push your `parser_engine.json` on the same level of `scrapy.cfg`, which is strongly recommended,
            # we and find the config file, and `src` not needed any more
            @TemplateAnnotation(("tpl_id_0","tpl_id_1")
            class SpiderB(CrawlSpider):
                name = "spider_b"
                start_urls = ["http://example.org"]

                def process_results(self, response, results):
                    for result in results:
                        # result has been parsed by PE, should be an instance of scrapy.Item's subclass,
                        # and you can do something else, like:
                        result['channel'] = "gaode_map"
                        result['extra'] = {}
                    return results

        :param tpl_ids: [string] or string
        :param kw: assign k-v to `item`, except following keys
            src => we use src to call `src.find_by_id('id')`
            start_urls_generator => string, method name, we use this method to get start_urls and bind it to the `cls`
            start_url_tpl_id => string, like tpl_id, but for scrapy.spiders.CrawlSpider `start_urls` contract
        """

        def _deco(spcls):
            kw['business'] = spcls.name
            cls.src = kw.pop('src', None)
            start_url_generator_name = kw.pop('start_urls_generator', None)
            if start_url_generator_name:
                spcls.start_urls = spcls.__dict__[start_url_generator_name](spcls)
            suti = kw.pop('start_url_tpl_id', None)
            if suti:
                rules = cls.get_rules(suti, **kw)
                if len(rules) >= 1:
                    spcls.start_rule = rules[0]

                    def _parse(self, response):
                        return rules[0].callback(response, **rules[0].cb_kwargs)

                    spcls._parse = _parse
            if issubclass(spcls, CrawlSpider) or issubclass(spcls, PECrawlSpider) or issubclass(spcls, RedisSpider):
                spcls.rules = cls.get_rules(tpl_ids, **kw)
            else:
                pass
                # FIXME: normal spider case
                # def parse_response_patch(self, response):
                #     return self.start_rule.callback(response)
                #
                # spcls.parse_response = classmethod(parse_response_patch)
                #
                # def start_requests(self):
                #     for url in self.start_urls:
                #         yield Request(url, callback=spcls.parse_response)
                #
                # spcls.start_requests = classmethod(start_requests)
            return spcls

        return _deco

    def __call__(self, *args, **kwargs):
        return self.PageTemplate(*args, **kwargs)
