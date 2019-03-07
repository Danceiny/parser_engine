import copy
import six
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from .template import PETemplate
from .parser import parse_with_tpl
from .utils import is_sequence, load_config_data, classproperty, is_string_like, is_string


# todo: build request
def make_request_from_data(self, data):
    """Returns a Request instance from data coming from Redis.

    By default, ``data`` is an encoded URL. You can override this method to
    provide your own message decoding.

    Parameters
    ----------
    data : bytes
        Message from redis.

    """
    pass


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
    def get_rules(cls, tpls, **kwargs):
        if not tpls:
            return ()
        if not is_sequence(tpls):
            tpls = tpls,
        if cls.src:
            rules = [cls.get_rule(cls.src.find_by_id(tpl_id), **kwargs) for tpl_id in tpls]
        else:
            rules = []
            if is_string(tpls[0]):
                for tpl in tpls:
                    rules.append(cls.get_rule_by_id(tpl, **kwargs))
            else:
                for tpl in tpls:
                    rules.append(cls.get_rule(tpl, **kwargs))
        return rules

    @classmethod
    def get_rule_by_id(cls, tpl_id, **kwargs):
        """
        Deprecated: 😒仅通过一个tpl_id如何构造LinkExtractor？
        Solution：先生成Rule对象，后面再想办法给它打补丁
        :param tpl_id:
        :param kwargs:
        :return:
        """
        kwargs['tpl_id'] = tpl_id
        return Rule(LinkExtractor(),
                    callback=parse_with_tpl_id, cb_kwargs=kwargs)

    @classmethod
    def get_rule(cls, tpl, **kwargs):
        """
        todo: 构造全功能的LinkExtractor
        :param tpl:  PETemplate / dict / json(str,bytes,)
        :param kwargs:
        :return:
        """
        if not isinstance(tpl, PETemplate):
            tpl = PETemplate.from_json(tpl)
        kwargs['tpl'] = tpl
        return Rule(tpl.get_link_extractor(),
                    callback=parse_with_tpl,
                    cb_kwargs=kwargs)

    @classmethod
    def PageTemplate(cls, **kw):
        """
        you can use it like this:
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
            @TemplateAnnotation(tpls=("tpl_id_0","tpl_id_1"))
            class SpiderB(CrawlSpider):
                name = "spider_b"
                start_urls = ["http://example.org"]

                def process_results(self, response, results):
                    for result in results:
                        # result has been parsed by PE, should be an instance of scrapy.Item subclass,
                        # and you can do something else, like:
                        result['channel'] = "gaode_map"
                        result['extra'] = {}
                    return results

        :param tpl_ids: [string] or string
        :param kw: assign k-v to `item`, except following keys
            tpls => list/tuple of string, which we view it as tpl_id, or of dict/PETemplate, which we view it as real tpl
            src => we use src to call `src.find_by_id('id')`
            start_urls_generator => string, method name, we use this method to get start_urls and bind it to the `cls`
            start_url_tpl_id/start_url_tpl => string, like tpl_id, but for scrapy.spiders.CrawlSpider `start_urls` contract
            customize_link_extractor => # if you store your LinkExtractor construct params in template
            use_default_request_builder => will override `make_request_from_data` using "PE clue-schema"
        """

        def _deco(spcls):
            tpls = kw.pop('tpls', None)
            kw['business'] = spcls.name
            cls.src = kw.pop('src', None)
            start_url_generator_name = kw.pop('start_urls_generator', None)
            if start_url_generator_name:
                spcls.start_urls = spcls.__dict__[start_url_generator_name](spcls)
                # todo: [feature request] check scrapy_redis.spiders
                # redis_key = spcls.__dict__.get("redis_key")
                # if redis_key:
                #     for start_url in spcls.start_urls:
                #         pass
            redis_key = spcls.__dict__.get("redis_key")
            hasredis = bool(redis_key)

            if hasredis:
                # allow a switch to determine whether assign the special method to spcls
                if kw.pop('use_default_request_builder', False):
                    spcls.make_request_from_data = make_request_from_data

            customize_link_extractor = kw.pop('customize_link_extractor', False)

            suti = kw.pop('start_url_tpl_id', kw.pop('start_url_tpl', None))
            if suti:
                rules = cls.get_rules(suti, **kw)
                if len(rules) >= 1:
                    spcls.start_rule = rules[0]

                    # keep pace with CrawlSpider.parse_start_url
                    def _parse_start_url(self, response):
                        return rules[0].callback(response, **rules[0].cb_kwargs)

                    spcls._parse_start_url = _parse_start_url

            if tpls and issubclass(spcls, CrawlSpider):
                spcls.rules = cls.get_rules(tpls, **kw)
                if not cls.src and customize_link_extractor and is_string(tpls) or is_string(tpls[0]):
                    # following code comes from scrapy.spiders.CrawlSpider._compile_rules
                    def _compile_rules(self):
                        def get_method(method):
                            if callable(method):
                                return method
                            elif isinstance(method, six.string_types):
                                return getattr(self, method, None)

                        self._rules = [copy.copy(r) for r in self.rules]
                        for rule in self._rules:
                            # diff start
                            tpl = PETemplate.from_json(find_by_id(rule.cb_kwargs['tpl_id']))
                            rule.link_extractor = tpl.get_link_extractor()
                            rule.callback = parse_with_tpl
                            # diff end
                            rule.process_links = get_method(rule.process_links)
                            rule.process_request = get_method(rule.process_request)

                    # do patch
                    spcls._compile_rules = _compile_rules
            else:
                pass
                # FIXME: scrapy.Spider && scrapy_redis.spiders.RedisSpider case
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

    def __call__(self, **kwargs):
        return self.PageTemplate(**kwargs)
