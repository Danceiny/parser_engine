# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider

from parser_engine import TemplateAnnotation


@TemplateAnnotation(start_url_tpl_id="gaode-place-api", channel="gaode_map", start_urls_generator="generate_urls")
class GaodeSpider(CrawlSpider):
    name = "gaode"

    def generate_urls(self):
        # keywords = getattr(self, 'keywords', None)
        # if keywords is None:
        keywords = "教育|培训"
        key = '0f1ef779f17ac1f0541bef5452eb7570'
        total = 2
        adcodes = [
            310101,  # 黄浦区
            # 310104,#徐汇区
            # 310105,#长宁区
            # 310106,#静安区
            # 310107,#普陀区
            # 310109,#虹口区
            # 310110,#杨浦区
            # 310115,#浦东新区
            # 310112,#闵行区
            # 310113,#宝山区
            # 310114,#嘉定区
            # 310116,#金山区
            # 310117,#松江区
            # 310118,#青浦区
            # 310120,#奉贤区
            # 310151,#崇明区
        ]
        urls = []
        for adcode in adcodes:
            for page in range(1, total):
                url = 'https://restapi.amap.com/v3/place/text?citylimit=true&output=json&offset=20&city=' + str(
                    adcode) + '&page=' + str(page) + '&key=' + key + '&keywords=' + keywords
                urls.append(url)
        return urls

    def parse(self, response):
        items = self._parse(response)
        if items:
            for item in items:
                yield item
