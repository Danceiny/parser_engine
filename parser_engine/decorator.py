from .template import PETemplate
import json
import os
from scrapy.spiders import Spider, Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from .parser import parse_with_tpl
from .utils import is_sequence
from .spider import PECrawlSpider

from scrapy.utils import project
from scrapy.utils.conf import closest_scrapy_cfg


def load_config_data():
    settings = project.get_project_settings()
    db_table = settings.get('PARSER_ENGINE_CONFIG_TABLE')
    if db_table:
        # todo
        pass
    else:
        config_path = settings.get("PARSER_ENGINE_CONFIG_FILE", "parser_engine.json")
        if config_path:
            if not os.path.isabs(config_path):
                project_root_dir = os.path.dirname(closest_scrapy_cfg())
                config_path1 = os.path.join(project_root_dir, config_path)
                if not os.path.exists(config_path1):
                    config_path1 = os.path.join(os.path.dirname(project_root_dir), config_path)
                    if not os.path.exists(config_path1):
                        raise RuntimeError("parser_engine config file " + config_path + " not found")
                    else:
                        config_path = config_path1
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
                    print("cb_kwargs", rules[0].cb_kwargs)

                    def _parse(self, response):
                        return rules[0].callback(response, **rules[0].cb_kwargs)

                    spcls.tpl = rules[0].cb_kwargs['tpl']
                    spcls._parse = _parse
            if issubclass(spcls, CrawlSpider) or issubclass(spcls, PECrawlSpider):
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
