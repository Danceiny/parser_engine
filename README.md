## Parser Engine 
代号PE，为[scrapy](https://scrapy.org/)框架量身定制的 **"可配置化的响应解析器引擎"**。

主要支持以下特性：
- [x] 基于xpath、jsonpath等规则解析html和json格式的http请求响应体
- [x] 输出值基于`scrapy.Item`，自动定位并返回实例化的`Item`
- [x] 支持 **父节点**、**列表for循环解析**
- [x] 字段枚举值的映射
- [x] 设置字段为必有字段，缺失时丢弃整个`Item`
- [x] 将list类型的字段拼接成字符串

### 安装
- 安装最新体验版: 
    >`pip install git+https://github.com/Danceiny/parser_engine`
    
- 安装稳定版：
    >`pip install -U parser_engine`

### 更新日志
请移步[CHANGELOG.md](CHANGELOG.md)。

### 速览
>如何使用PE从零开始快速编写一个网站的爬虫，并持久化数据？可移步[快速开始](./TUTORIAL.md)。

- 极简版，使用`CrawlSpider`的rules机制。
```python
from parser_engine import TemplateAnnotation
from scrapy.spiders.crawl import CrawlSpider
@TemplateAnnotation(tpls="demo")
class DemoSpider4(CrawlSpider):
    name = "demo4"
    start_urls = [
        "http://github.cannot.cc/baixing-helper"
    ]
```

- 使用scrapy_redis，解析start_urls的响应。
```python
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
```

- 使用scrapy_redis，灵活运用多种PE特性。
```python
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
            "key": "city",
            "json_path": "cityDto.cityName",
            "value_type": "singleton"
        }, {
            "key": "service_phone",
            "default_value": "",
        }, {
            "key": "wechat",
            "json_key": "wechat",
        },  {
            "key": "tags",
            "json_key": "tags",
            "join": ","
        }]
    }), channel='youka', leads_src='优卡')
class YoukaSpider(ClueSpider):
    name = 'youka'
    custom_settings = {
        'CONCURRENT_REQUESTS': 2,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1
    }
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
```

完整示例请参考：[examples](./examples)。

### 原理
- 解析器
    >PE向调用方提供一套简单、易懂的参数，实际会将其`编译`成较为复杂的xpath表达式，再借助scrapy封装的解析器将所需内容提取出来。

- 返回值
    >通过配置`itemname`参数，PE将`反射`得到所需的`Item`类，按照配置的映射关系，从提取出的值创建一个`Item`实例（或者多个），并返回一个可迭代的`Item`实例列表。
    
### 已知问题

- 如果提取规则较为复杂，建议直接使用xpath和css参数，因为PE的参数编译可能存在问题。
- 如果对性能有比较强的需求，不建议使用。

### 特性介绍
- [x] 支持表格、列表等形式的批量解析
    >通过在模板中定义一个父节点，从html页面中的表格、列表等组件中，批量抓取多个同类item
    
    >用法示例：使用`{"parent": {}, "fields": []}`这样的配置，将首先查找匹配`parent`的节点，然后遍历其每个子节点，对每个子节点应用`fields`规则，生成一个item。
    
- [x] Clue Mechanism
    > 基于scrapy_redis的线索机制，可持久化（目前支持mysql）线索，方便追踪。

- [x] 值映射
    >一个简单的需求场景：API返回的性别字段是0和1，但是需要将其转换成"男"和"女"。
    
### 待做清单
- 优化
    - [ ] 支持直接在`Item`的类定义中定义模板
        >用法示例：原模板的`itemname`参数通过注解传参，其他的模板参数定义在`Item`类中，如下所示。
        ```
        class MyItem(scrapy.Item):
            tpl = {"parent": {"xpath":"//div[@id=\"contentDiv\"]//table/tbody/tr[position()>1]"}
            name = Field(xpath="//a[@href]/text()")
        ```

### scrapy配置参数

- PARSER_ENGINE_CONFIG_FILE 
    > 模板配置文件的位置。默认是`parser_engine.json`，与`scrapy.cfg`文件同级。
- MYSQL
    > MySQL配置信息，dict类型，包含以下字段：
        - DATABASE
        - USER
        - PASSWORD
        - PORT 默认3306
        - HOST 默认127.0.0.1

下面的字段在MYSQL配置缺失时生效：
- MYSQL_USER
- MYSQL_PASSWORD
- MYSQL_PORT
- MYSQL_DATABASE

### 模板参数
模板配置文件，如`parser_engine.json`，其构成结构如下：
```json
{
  "templates": [
    {
      "name": "tpl1"   
    },
    {
      "name": "tpl2"
    }
  ]

}

```
模板配置文件中`templates`列表中的每一项，即为一个模板。

所谓模板，对应的类是[PETemplate](./parser_engine/template.py)，其构成结构如下：

- name 必要。相当于该模板在该模板文件中的id
- parent 不必要。如果指定，将按照其指定的规则，从响应中取出某节点作为后续提取规则的根节点。
- itemname 不必要。如果指定，将尝试加载实例化该item类；如果没有找到类或者没有指定，则返回`dict`类型的原始数据。
- extract_keys 不必要。json格式专属，用于直接从某个json对象中提取一组键值，通常可以搭配`parent`参数使用，较为高效。
- extract_keys_map 不必要。类似`extract_keys_map`，适用于需要转换原json对象中的键名的场景。
- fields 不必要。是一个`字段`的数组。

所谓字段，对应的类是[PEField](./parser_engine/template.py)，属于PE的核心，其构成结构如下：
- key 必要。提取结果保存的键名，通常是item的某个`Field`的变量名。
- xpath
- css
- tags 不必要。一组有序的html标签。如`["div","a"]`会被翻译成`//div/a`的xpath。
- attr_name 不必要。对于html来说，经常需要获取某个tag的某个属性值。
- attributes 不必要。支持多种结构。
    - string 直接作为`//div/a[{attributes}]`中的`{attributes}`
    - map `{"type": "password", "id": "id1"}` => `//div/a[@type=\"password\" and @id=\"id1\"]`
    - list `[["type","=","password"],["id", "!=","id1"]]` => `//div/a[@type=\"password\" and @id!=\"id1\"]`
- json_path 不必要。`json_path`完全遵循[json_path协议](https://goessner.net/articles/JsonPath/)，[json_path在线调试](http://jsonpath.com/)。
- json_key 不必要。直接作为json取值的键名。
- value_type 不必要。**但很有用**，主要是因为不管是xpath还是json_path，提取出来都是一个list，尽管有时字段明明是完全确定的，如果设置value_type=`singleton`，则PE将提取list的第一个元素。
- position 不必要。
- mapper 不必要。dict类型，用于实现值映射，例如：`{1: "male", 2: "femail"}`。
- join 不必要。str类型，用于实现`','.join([])`。

### TemplateAnnotation参数说明
TemplateAnnotation注解中传进来的参数，除了下面列出的，其他的参数都会被塞到返回值中（当然，如果通过定义`itemname`，实例化item的时候会静默抛弃那些不属于item的值）。

- start_url_tpl: 模板的数组，或者模板id的数组。
    >对应于start_urls的模板，会生成一个`_parse_start_url`方法绑定到spider类上，该方法有两个参数（不包括self）：
    - response 
    - tpl_index_or_id，默认是None
    
- tpls: 模板的数组，或者模板id的数组

具体请参考[decorator.py](./parser_engine/decorator.py)中的注释及源代码。

#### Html格式
举个简单的例子。

目标：抓取[抖音用户关键字搜索抓包数据分析脚本使用指南](http://github.cannot.cc/baixing-helper/抖音用户关键字搜索抓包数据分析脚本使用指南.html)页面的几个步骤标题，每个步骤是一个`h3`标签，步骤标题在`id`属性里，并且需要去掉形如`1-`的前缀。
那么相应的配置文件是：
```json
    {
      "name": "demo",
      "fields": [
        {
          "dom_id": null,
          "_css": null,
          "xpath": null,
          "tags": [
            "h3"
          ],
          "classes": [],
          "attributes": null,
          "position": null,
          "key": "步骤",
          "value_type": null,
          "regexp": "[\\d]{1,2}-(\\w+)",
          "attr_name": "id"
        }
      ]
    }
```
输出
```
{'步骤': ['准备工作', '找到电脑的ip地址和端口', '确保手机与电脑建立连接', '抖音搜索关键词', '抓包数据导出', '提取用户信息', '推荐在线转换工具', 'python脚本导出']}
```

如果只需要第二个步骤，将json配置中的`position`参数改为`2`，即可得到如下输出：
```
{'步骤': ['找到电脑的ip地址和端口']}
```

#### JSON格式
```json
    {
      "name": "json-api-demo",
      "fields": [
        {
          "key": "poi_id",
          "json_path": "$.pois[:1].id"
        },
        {
          "key": "地名",
          "json_path": "$.data.name",
          "value_type": "singleton"
        },
        {
          "key": "下级",
          "json_path": "$.data.children[*].name"
        }
      ]
    }
```


由于`json_path`解析总是返回一个list，对于一些确定的字段，比如通过调用API`http://172.31.1.4:30815/api/dict/area/0?childrenDepth=1`，想拿到该地区的name字段，则可以设置`value_type`为`singleton`，则PE会做一次转换。
