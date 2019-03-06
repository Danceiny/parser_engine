## Parser Engine Driven by Template
### Install
- Fresh pre-release: 
    >`pip install git+https://github.com/Danceiny/parser_engine`

### TemplateAnnotation
参数约定：
- 业务名称name，即采用该注解的Spider类的name类变量

其他请参考[decorator.py](./parser_engine/decorator.py)中的注释。

### Html response
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
```json
{'步骤': ['准备工作', '找到电脑的ip地址和端口', '确保手机与电脑建立连接', '抖音搜索关键词', '抓包数据导出', '提取用户信息', '推荐在线转换工具', 'python脚本导出']}
```

如果只需要第二个步骤，将json配置中的`position`参数改为`2`，即可得到如下输出：
```json
{'步骤': ['找到电脑的ip地址和端口']}
```

### JSON text response
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

`json_path`字段完全遵循[json_path协议](https://goessner.net/articles/JsonPath/)，[json_path在线调试](http://jsonpath.com/)。
由于`json_path`解析总是返回一个list，对于一些确定的字段，比如通过调用API`http://172.31.1.4:30815/api/dict/area/0?childrenDepth=1`，想拿到该地区的name字段，则可以设置`value_type`为`singleton`，则PE会做一次转换。

具体使用可以参考：
- [demo_spider](./demo/demo/spiders/demo_spider.py)。
- [gaode_spider](./demo/demo/spiders/gaode_spider.py)。

