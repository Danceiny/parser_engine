# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from peewee import Model, MySQLDatabase, PrimaryKeyField, CharField, IntegerField

db = None


# db = PostgresqlDatabase("bxdw", host='bi.baixing.com', port=35432, user="biz_user", passwd="biz_user", charset="utf8")
def init_db(datasource):
    global db
    if not db:
        from scrapy.utils import project
        settings = project.get_project_settings()
        if datasource == 'mysql':
            db = MySQLDatabase(database=settings.get("MYSQL_DATABASE"),
                               host=settings.get("MYSQL_HOST"),
                               user=settings.get("MYSQL_USER"),
                               passwd=settings.get("MYSQL_PASSWORD"),
                               port=3306, charset="utf8")
    return db


class BaseItem(Item):
    channel_id = Field()
    channel = Field()
    created_time = Field()


class DemoItem(BaseItem):
    # define the fields for your item here like:
    name = Field()
    text = Field()
    author = Field()
    steps = Field()


class ClueItem(Item):
    channel = Field()
    name = Field()
    index = Field()
    url = Field()
    from_url = Field()
    status = Field()
    created_time = Field()
    finished_time = Field()


class LeadsItem(Item):
    channel_id = Field()
    channel = Field()
    name = Field()
    contact = Field()
    contact_type = Field()
    city = Field()
    category = Field()
    address = Field()
    created_time = Field()
    extra = Field()


class Leads(Model):
    id = PrimaryKeyField()
    channel_id = CharField(verbose_name="渠道id", max_length=50, null=False, unique=True)
    channel = CharField(verbose_name="渠道名称", null=False)
    name = CharField(verbose_name="名称", null=False, unique=True)
    contact = CharField(verbose_name="联系方式", null=False)
    contact_type = CharField(verbose_name="联系方式类型", null=False)
    city = CharField(verbose_name="城市")
    category = CharField(verbose_name="类目/行业")
    address = CharField(verbose_name="地址")
    created_time = IntegerField(verbose_name="创建时间")
    extra = CharField(verbose_name="附加信息")

    class Meta:
        database = init_db("mysql")
