from parser_engine.clue.spider import ClueSpider
from parser_engine import TemplateAnnotation
from parser_engine.clue.items import ClueItem
from parser_engine.request import TaskRequest
from scrapy import Request


@TemplateAnnotation(start_url_tpl=({
                                       "name": "youka_shop_listing_api",
                                       "parent": {
                                           "json_key": "data",
                                       },
                                       "fields": [{
                                           "key": "totalPage",
                                           "json_key": "totalPage",

                                       }, {
                                           "key": "ids",
                                           "json_path": "dataList[*].id"
                                       }]
                                   },),
    tpls=({
        "name": "youka_shop_detail_api",
        "itemname": "HuocheDealerItem",
        "parent": {
            "json_key": "data",
        },
        "fields": [{
            "key": "company_type",
            "json_key": "category",
            "mapper": {
                1: "二手车直营店",
                2: "4S店"
            }
        }, {
            "key": "dealer_id",
            "json_key": "id",
            "required": 1,
        }, {
            "key": "leads_name",
            "json_key": "shopName",
        }, {
            "key": "area",
            "json_path": "districtDto.districtName",
            "value_type": "singleton"
        }, {
            "key": "province",
            "json_path": "provinceDto.provinceName",
            "value_type": "singleton"
        }, {
            "key": "city",
            "json_path": "cityDto.cityName",
            "value_type": "singleton"
        }, {
            "key": "address",
            "json_key": "wholeAddress",
        }, {
            "key": "phone",
            "json_key": "mobile",
        }, {
            "key": "service_phone",
            "default_value": "",
        }, {
            "key": "wechat",
            "json_key": "wechat",
        }, {
            "key": "linkman",
            "json_key": "contactName"
        }, {
            "key": "tags",
            "json_key": "tags",
            "join": ","
        }, {
            "key": "brand",
            "json_key": "brandList",
            "join": ","
        }, {
            "key": "business_scope",
            "json_key": "scope"
        }]
    }), channel='youka', leads_src='优卡')
class YoukaSpider(ClueSpider):
    name = 'youka'
    custom_settings = {
        'CONCURRENT_REQUESTS': 2,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1
    }

    # 二手车直营店 "category": 1,
    # 4S店 "category": 2,
    def parse(self, response):
        items = self._parse_start_url(response)
        meta = response.meta
        clue_id = meta.get('clue_id')
        from_url = response.request.url
        if meta.get('open_pages'):
            total_page = items[0]['totalPage']
            import re
            current_page = int(re.findall('page=(\\d+)', from_url)[0])
            for i in range(1, total_page + 1):
                if current_page == i:
                    continue
                url = "http://www.china2cv.com/truck-foton-web/api/shop/v1/getShopList?page=%d&pageSize=10" % i
                yield ClueItem({"project": "huoche", "spider": self.name, "req": TaskRequest(
                    url=url,
                    meta={"from_clue_id": clue_id}
                )})
        for item in items:
            for id in item['ids']:
                r = Request(url="http://www.china2cv.com/truck-foton-web/api/shop/v1/getShopInfo?shopId=%d" % int(id),
                            callback=self._response_downloaded)
                r.meta.update(rule=0, from_clue_id=clue_id)
                yield r

    def process_results(self, response, results):
        for item in results:
            item['url'] = 'http://www.china2cv.com/storeDetail.html?typess=1&shopId=' + str(item['dealer_id'])
        return results
