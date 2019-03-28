## Examples of parser-engine
### demo

>written before v0.1.0

为了验证PE的设计理念，从`http://github.cannot.cc/baixing-helper/`这一GitHub Pages的简单目录页着手，主要测试了`parser_engine.spider.PECrawlSpider`和PE模板配置文件的编写，以及PE对配置文件的加载、执行、输出等。

该项目不需要任何redis、db等依赖，可以直接进入到目录下`scrapy crawl **`运行，观察控制台标准输出即可。

注意，GitHub Pages似乎有轻微的反爬（症状是`连接被拒绝`），需要控制爬取速率。

### huoche

>written after v0.1.0

抓取国内几家货车网站的经销商信息。

PE的大量特性，是在该项目开发过程中遇到问题之后开发的，因此该demo具有较高的参考意义。

`parser_engine.spider.PESpider`及其子类`parser_engine.clue.spider.ClueSpider`，基于`scrapy_redis`进行了二次开发，需要构造一个[TaskRequest](../parser_engine/request.py)对象，经json序列化后扔进某个spider对应的redis队列（通常是redis的list结构）中。

如果对如何构造该demo中所需的`TaskRequest`有兴趣，可以联系 [Danceiny](mailto:danceiny@gmail.com)。这里给出[中国重汽](./huoche/huoche/spiders/zhongguozhongqi.py)的实际例子：
```python
import json
import redis
r = redis.from_url("redis://127.0.0.1:6379")
task_reqs = []
for i in range(34):
    task_reqs.append({
        'url': 'http://www.cnhtc.com.cn/View/XiaoShouWangLuoDetail.aspx?sc=5&Category=1&PV=0010%s' % (
            str(i) if i >= 10 else ('0%d' % i)),
        'headers': {
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }
    })
for task_req in task_reqs:
    r.lpush('huoche:zhongguozhongqi:start_urls', json.dumps(task_req))
```


运行该项目前，除了安装python依赖(`pip install -r requirements.txt`)之外，还需要部署并配置好redis、mysql，相应的连接配置项见[settings.py](./huoche/huoche/settings.py)。
