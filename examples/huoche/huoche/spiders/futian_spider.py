from parser_engine import TemplateAnnotation
from parser_engine.clue.spider import ClueSpider


@TemplateAnnotation(start_url_tpl=({
                                       "name": "futian_pe",
                                       "itemname": "HuocheDealerItem",
                                       "extract_keys_map": {
                                           "id": "dealer_id",
                                           "dealerName": "leads_name",
                                           "dealerAddress": "address",
                                           "dealerTel": "phone"
                                       }},), channel='futian', leads_src='福田汽车')
class FutianSpider(ClueSpider):
    name = 'futian'

    def parse(self, response):
        items = self._parse_start_url(response)
        for item in items:
            yield item
        self.finish_clue(response, len(items))
