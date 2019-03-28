from parser_engine import TemplateAnnotation
from parser_engine.clue.spider import ClueSpider


@TemplateAnnotation(start_url_tpl=({
    "name": "zhongguozhongqi_xiaoshouwangluo",
    "itemname": "HuocheDealerItem",
    "parent": {
        "xpath": "//tr[@class=\"bgcolor2\"]"
    },
    "fields": [
        {
            "key": "area",
            "xpath": "td[1]/text()",
            "value_type": "stripped_string"
        }, {
            "key": "leads_name",
            "xpath": "td[2]/text()",
            "value_type": "stripped_string"
        }, {
            "key": "address",
            "xpath": "td[3]/text()",
            "value_type": "stripped_string"
        }, {
            "key": "linkman",
            "xpath": "td[4]/text()",
            "value_type": "stripped_string"
        }, {
            "key": "phone",
            "xpath": "td[5]/text()",
            "value_type": "stripped_string"
        }
    ]
}), channel='zhongguozhongqi', leads_src='中国重汽')
class ZhongguozhongqiSpider(ClueSpider):
    name = 'zhongguozhongqi'
    def parse(self, response):
        items = self._parse_start_url(response)
        for item in items:
            phone = item.get('phone')
            if phone:
                item['phone'] = phone.replace('、', ',')
            yield item
        self.finish_clue(response, len(items))
