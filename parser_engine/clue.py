from peewee import Model, PrimaryKeyField, CharField, IntegerField
import time
import simplejson as json
from scrapy.item import Item, Field
from enum import IntEnum
from .config import mysqldb


class ClueStatus(IntEnum):
    PENDING = 0
    RUNNING = 1
    SUCCESS = 200
    FAILED = 500


class ClueItem(Item):
    channel = Field()
    business = Field()
    url = Field()
    from_clue_id = Field()
    req = Field()

    project = Field()
    spider = Field()


class ClueModel(Model):
    id = PrimaryKeyField()
    status = IntegerField(verbose_name="状态", default=0)
    created_time = IntegerField(verbose_name="创建时间", default=0)
    modified_time = IntegerField(verbose_name="更新时间", default=0)
    finished_time = IntegerField(verbose_name="完成时间", default=0)
    channel = CharField(verbose_name="渠道名称", max_length=20, default='')
    name = CharField(verbose_name="业务名称", max_length=20, default='')
    url = CharField(verbose_name="爬取url", max_length=500, default='')
    from_clue_id = IntegerField(verbose_name="来源clue的id", default=0)
    req = CharField(verbose_name="请求体", max_length=2048, default='')
    dw_count = IntegerField(verbose_name="打到dw数量", default=0)

    class Meta:
        table_name = 'clue'
        database = mysqldb

    @staticmethod
    def from_item(item):
        model = ClueModel()
        model.url = item.get('url')
        model.name = item.get('business') or item.get('spider')
        model.channel = item.get('channel') or item.get('project')
        model.created_time = int(time.time())
        model.modified_time = int(time.time())
        model.from_clue_id = item.get('from_clue_id')
        model.req = json.dumps(item.get('req'))
        return model

    def success(self):
        self.finished_time = int(time.time())
        self.status = ClueStatus.SUCCESS

    def fail(self):
        # 已经失败过的，用status++表示重试次数
        if self.status >= ClueStatus.FAILED:
            self.status += 1
        else:
            self.status = ClueStatus.FAILED
