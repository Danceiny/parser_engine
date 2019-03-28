from parser_engine import TemplateAnnotation
from parser_engine.clue.spider import ClueSpider
from ..items import HuocheDealerItem
import json


@TemplateAnnotation(start_url_tpl=({
                        "name": "sxqc_pe",
                        "itemname": "HuocheDealerItem",
                        "extract_keys_map": {
                            "title": "leads_name",
                            "address": "address",
                            "phone": "phone"
                        }},), channel='', leads_src='')
class FutianSpider(ClueSpider):
    name = 'sxqc'

    def parse(self, response):
        body = '[' + bytes.decode(response.body) + ']'
        body = body.replace("'", '"')
        data = json.loads(body)
        for v in data:
            item = HuocheDealerItem(
                leads_name=v['title'],
                address=v['address'],
                phone=v['phone'],
                channel="sxqc",
                leads_src="陕西重卡"
            )
            yield item
        self.finish_clue(response, len(data))
