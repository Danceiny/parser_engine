from parser_engine import TemplateAnnotation
from parser_engine.clue.spider import ClueSpider
from parser_engine.clue.items import ClueItem
import re


@TemplateAnnotation(start_url_tpl=({
                                       "name": "kachezhijia_listing",
                                       "parent": {
                                           "xpath": "//ul[@class=\"dealers\"]/li/div[@class=\"detail\"]"
                                       },
                                       "itemname": "HuocheDealerItem",
                                       "fields": [
                                           {
                                               "key": "dealer_id",
                                               "xpath": "p[@class=\"contact\"]/a/@href",
                                               "regexp": "360che.com/(\\d+)/",
                                               "value_type": "singleton"
                                           },
                                           {
                                               "key": "url",
                                               "xpath": "p[@class=\"contact\"]/a/@href",
                                               "value_type": "singleton"
                                           },
                                           {
                                               "key": "leads_name",
                                               "xpath": "h2/a[@href]/text()",
                                               "value_type": "singleton"
                                           },
                                           {
                                               "key": "tags",
                                               "xpath": "span[@class=\"inline-block\"]/text()"
                                           },
                                           {
                                               "key": "address",
                                               "xpath": "p[last()-1]/text()",
                                               "regexp": "地址 : (\\w+)",
                                               "value_type": "stripped_string"
                                           },
                                           {
                                               "key": "brand",
                                               "xpath": "p[@class=\"contact\"]/a[@href]/text()",
                                               "value_type": "singleton"
                                           },
                                           {
                                               "key": "phone",
                                               "xpath": "p[@class=\"contact\"]/span[@class=\"tel\"]/text()",
                                               "value_type": "singleton"
                                           }
                                       ]
                                   }, {
                                       "name": "kachezhijia_pageinfo",
                                       "fields": [{
                                           "key": "totalPage",
                                           "xpath": "//ul[@class=\"page-list\"]/li[last()-1]//a[@href]/text()",
                                           "value_type": "int"
                                       }, {
                                           "key": "totalCount",
                                           "xpath": "//ul[@id=\"site-list\"]/li[1]/a[@href]/text()",
                                           "regexp": "不限 \((\\d+)\)",
                                           "value_type": "int"
                                       }
                                       ]
                                   }), channel='kachezhijia', leads_src='卡车之家')
class CachezhijiaSpider(ClueSpider):
    name = 'kachezhijia'

    def parse(self, response):
        from_url = response.request.url
        from_clue_id = response.meta.get('clue_id')
        # 翻页
        if response.meta.get('open_pages', False):
            data = self._parse_start_url(response, 1)
            try:
                total_count = data[0]['totalCount']
                total_page = data[0]['totalPage']
                self.info("卡车之家今日共计%d个HuocheDealer" % total_count)
            except (KeyError, IndexError) as e:
                self.error("get kachezhijia page totalCount error: %s data: %s, request.body: %s"
                           % (str(e), data, response.request.body))
            else:
                response.request.meta['open_pages'] = 0
                current_page = int(re.findall('0_c(\\d+)', from_url)[0])
                for i in range(0, total_page + 1):
                    if i == current_page:
                        continue
                    task = self.request_to_task(response.request)
                    task.url = re.sub('c(\\d)', 'c%d' % i, task.url)
                    yield ClueItem(
                        {"url": task.url, "req": task, "project": self.project, "spider": self.name,
                         "from_clue_id": from_clue_id, })
        items = self._parse_start_url(response)
        for item in items:
            yield item
        self.finish_clue(response, len(items))
