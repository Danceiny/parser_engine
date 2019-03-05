import json
import os
from scrapy.spiders import Spider, Rule, CrawlSpider
from scrapy_redis.spiders import RedisSpider
from scrapy.linkextractors import LinkExtractor
from .template import PETemplate
from .parser import parse_with_tpl
from .utils import is_sequence, closest_parser_engine_json
from .spider import PECrawlSpider


def load_config_data():
    from scrapy.settings import Settings
    settings = Settings()
    settings_module_path = os.environ.get('SCRAPY_ENV')
    print("parser_engine settings module path", settings_module_path)
    settings.setmodule(settings_module_path, priority='project')
    db_table = settings.get('PARSER_ENGINE_CONFIG_TABLE')
    if db_table:
        # todo
        pass
    else:
        config_path = settings.get("PARSER_ENGINE_CONFIG_FILE", 'parser_engine.json')
        if not os.path.isabs(config_path):
            config_path = closest_parser_engine_json(config_path)
        with open(config_path) as f:
            return json.loads(f.read())


class Template(object):
    src = None  # db/file object with get_template api

    config_data = None

    @classmethod
    def get_rules(cls, tpl_ids, **kwargs):
        if not tpl_ids:
            return ()
        if not is_sequence(tpl_ids):
            tpl_ids = [tpl_ids]
        rules = []
        if not cls.config_data:
            cls.config_data = load_config_data()
        for tpl in cls.config_data['templates']:
            if tpl.get('name') in tpl_ids:
                rules.append(cls.get_rule(tpl, **kwargs))
        return rules

    @classmethod
    def get_rule(cls, tpl, **kwargs):
        kwargs['tpl'] = tpl
        if not isinstance(tpl, PETemplate):
            tpl = PETemplate.from_json(tpl)
        return Rule(LinkExtractor(allow=tpl.get('allow')), callback=parse_with_tpl, cb_kwargs=kwargs)

    @classmethod
    def PageTemplate(cls, tpl_ids=None, **kw):
        def _deco(spcls):
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

                    spcls.tpl = rules[0].cb_kwargs['tpl']
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


TemplateAnnotation = Template()
