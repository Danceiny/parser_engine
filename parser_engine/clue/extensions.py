import logging
import json
import time
import requests
from scrapy import signals

logger = logging.getLogger(__name__)


class ExceptionHandler(object):
    api = None

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        crawler.signals.connect(ext.spider_error, signal=signals.spider_error)
        crawler.signals.connect(ext.item_error, signal=signals.item_error)
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        settings = crawler.settings
        ext.api = settings.get('NOTIFICATION_API')
        return ext

    def send_notification(self, data):
        if self.api:
            retry_times = 3
            while retry_times > 0:
                try:
                    resp = requests.post(self.api, json=data)
                    if resp.status_code == 200:
                        break
                except requests.RequestException:
                    pass
                time.sleep(1)
                retry_times -= 1

    def spider_error(self, failure, response, spider):
        content = "Spider Error on {0}, traceback: {1}".format(response.url, failure.getTraceback())
        logger.error(content)
        self.send_notification({
            "title": "{} Spider Error".format(spider.name),
            "content": content
        })

    def spider_opened(self, spider):
        content = "ExceptionHandler opened spider {}".format(spider.name)
        self.send_notification({
            "title": "{} Spider Opened".format(spider.name),
            "content": content
        })

    def item_error(self, item, response, spider, failure):
        content = "Item Pipeline on {0}, traceback: {1}\nitem: {2}".format(
            type(item),
            failure.getTraceback(),
            json.dumps(dict(**item)), )
        self.send_notification({
            "title": "{1} Spider {1} item error".format(spider.name, type(item).__name__),
            "content": content
        })
