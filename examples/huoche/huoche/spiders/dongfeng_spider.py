from parser_engine import TemplateAnnotation
from parser_engine.clue.spider import ClueSpider


@TemplateAnnotation(start_url_tpl=({
                        "name": "dongfeng_pe",
                        "parent": {
                            "xpath": "//li"
                        },
                        "itemname": "HuocheDealerItem",
                        "fields": [
                            {
                                "key": "dealer_id",
                                "xpath": "@data-id",
                                "value_type": "singleton"
                            },
                            {
                                "key": "leads_name",
                                "xpath": "div[contains(@class,'data-Title')]/text()",
                                "value_type": "singleton"
                            },
                            {
                                "key": "address",
                                "xpath": "p/span[@class='data-Address']/text()",
                                "value_type": "singleton"
                            },
                            {
                                "key": "phone",
                                "xpath": "p/span[@class='data-Tel']/text()",
                                "value_type": "singleton"
                            },
                            {
                                "key": "brand",
                                "xpath": "p/span[@class='data-Main']/text()",
                                "value_type": "singleton"
                            },
                        ]},), channel='dongfeng', leads_src='东风')
class DongfengSpider(ClueSpider):
    name = 'dongfeng'

    def parse(self, response):
        items = self._parse_start_url(response)
        for item in items:
            yield item
        self.finish_clue(response, len(items))