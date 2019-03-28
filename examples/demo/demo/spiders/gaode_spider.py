# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider

from parser_engine import TemplateAnnotation


@TemplateAnnotation(start_url_tpl_id="gaode-place-api", channel="gaode_map", start_urls_generator="generate_urls")
class GaodeSpider(CrawlSpider):
    name = "gaode"

    def generate_urls(self):
        keywords = "教育|培训"
        key = '0f1ef779f17ac1f0541bef5452eb7570'
        total = 2
        adcodes = [
            310101,  # 黄浦区
        ]
        urls = []
        for adcode in adcodes:
            for page in range(1, total):
                url = 'https://restapi.amap.com/v3/place/text?citylimit=true&output=json&offset=20&city=' + str(
                    adcode) + '&page=' + str(page) + '&key=' + key + '&keywords=' + keywords
                urls.append(url)
        return urls

    def parse(self, response):
        items = self._parse_start_url(response)
        if items:
            for item in items:
                yield item
