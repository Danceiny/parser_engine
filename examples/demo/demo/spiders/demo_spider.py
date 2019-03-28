from parser_engine.spider import PECrawlSpider, PERule
from parser_engine.template import PETemplate, PEField
from parser_engine import TemplateAnnotation, Template
from scrapy.spiders import CrawlSpider


@TemplateAnnotation(tpls=("demo", "dict-api-demo"), channel_id="cannot.cc", channel="Danceiny")
class DemoSpider(PECrawlSpider):
    name = "demo1"

    start_urls = [
        "http://github.cannot.cc/baixing-helper/"
    ]

    def process_results(self, response, results):
        print("处理结果", results)
        return results


class DemoSpider2(PECrawlSpider):
    def __init__(self, *args, **kwargs):
        DemoSpider2.start_rule = PERule(callback="callback", template=PETemplate("demo2", [
            PEField(key="步骤3", tags=["h3"], regexp="^[0-9]-([^0-9.]+)", position=3, attr_name="id")]))
        super(DemoSpider2, self).__init__(self)

    name = "demo2"
    start_urls = [
        "http://github.cannot.cc/baixing-helper/抖音用户关键字搜索抓包数据分析脚本使用指南.html"
    ]

    def callback(self, data):
        print("准备持久化", data)

    def process_results(self, response, results):
        print("处理结果", results)
        return results


@Template.PageTemplate(start_url_tpl_id="dict-api-demo")
class DemoSpider3(PECrawlSpider):
    """
    for json api spider
    """

    name = "demo3"
    start_urls = [
        "https://restapi.amap.com/v3/place/text?citylimit=true&output=json&offset=20&city=shanghai&page=1&key=0f1ef779f17ac1f0541bef5452eb7570&keywords=%E6%95%99%E8%82%B2"
    ]

    def process_results(self, response, results):
        print("处理结果", results)
        return results


@Template.PageTemplate(tpls="demo")
class DemoSpider4(CrawlSpider):
    name = "demo4"
    start_urls = [
        "http://github.cannot.cc/baixing-helper"
    ]
