from parser_engine import TemplateAnnotation
from parser_engine.clue.spider import ClueSpider
from six.moves.urllib.parse import parse_qsl


@TemplateAnnotation(start_url_tpl=({
                                       "name": "yiqijiefang_pe",
                                       "parent": {
                                           "xpath": "//table[@class='list_1']/tr"
                                       },
                                       "itemname": "HuocheDealerItem",
                                       "fields": [
                                           {
                                               "key": "city",
                                               "xpath": "td[@class='city']/text()",
                                               "value_type": "singleton"
                                           },
                                           {
                                               "key": "leads_name",
                                               "xpath": "td[@class='fwz_name']/text()",
                                               "value_type": "singleton"
                                           },
                                           {
                                               "key": "address",
                                               "xpath": "td[@class='address']/text()",
                                               "value_type": "singleton"
                                           },
                                           {
                                               "key": "phone",
                                               "xpath": "td[@class='phone']/text()",
                                               "value_type": "singleton"
                                           },
                                           {
                                               "key": "service_phone",
                                               "xpath": "td[@class='bei1']/text()",
                                               "value_type": "singleton"
                                           },
                                       ]},), channel='jiefang', leads_src='解放')
class YiqijiefangSpider(ClueSpider):
    name = 'yiqijiefang'

    def parse(self, response):
        items = self._parse_start_url(response)
        request_body = str(response.request.body, encoding="utf-8")
        request_data = dict(parse_qsl(request_body))
        province = request_data.get('province')
        for item in items:
            item['province'] = province
            yield item
        self.finish_clue(response, len(items))
