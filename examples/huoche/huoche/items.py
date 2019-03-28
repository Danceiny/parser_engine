# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from peewee import Model, PrimaryKeyField, CharField, IntegerField
from parser_engine.config import mysqldb


class HuocheDealerItem(Item):
    # channel + dealer_id 联合构成该dealer的唯一id
    channel = Field()
    dealer_id = Field()
    leads_src = Field()  # 线索渠道
    url = Field()  # 网站URL
    company_type = Field()  # 公司类型
    leads_name = Field()  # leads名称:公司名称，服务站名称
    area = Field()  # 区域
    province = Field()  # 省份
    city = Field()  # 城市
    address = Field()  # 地址
    phone = Field()  # 电话
    service_phone = Field()  # 24 小时服务电话
    wechat = Field()  # 微信
    linkman = Field()  # 联系人
    main_model = Field()  # 主销车型
    online_source = Field()  # 在线车源
    business_scope = Field()  # 经营范围
    brand = Field()  # 品牌
    tags = Field()  # 标签

    crawled_time = Field()


class HuocheDealerModel(Model):
    id = PrimaryKeyField()
    dealer_id = CharField(default='', max_length=32)  # 在该渠道的id
    channel = CharField(default='', max_length=16)  # channel是英文版的leads_src
    leads_src = CharField(default='', max_length=16)  # 线索渠道
    phone = CharField(default='', max_length=64)  # 电话
    wechat = CharField(default='', max_length=32)  # 微信
    url = CharField(default='', max_length=64)  # 网站URL
    brand = CharField(default='', max_length=16)  # 品牌
    tags = CharField(default='', max_length=64)  # 标签
    company_type = CharField(default='', max_length=16)  # 公司类型
    leads_name = CharField(default='', max_length=64)  # leads名称:公司名称，服务站名称
    area = CharField(default='', max_length=16)  # 区域
    province = CharField(default='', max_length=16)  # 省份
    city = CharField(default='', max_length=16)  # 城市
    address = CharField(default='', max_length=64)  # 地址
    service_phone = CharField(default='', max_length=64)  # 24 小时服务电话
    linkman = CharField(default='', max_length=64)  # 联系人
    main_model = CharField(default='', max_length=64)  # 主销车型
    online_source = CharField(default='', max_length=64)  # 在线车源
    business_scope = CharField(default='', max_length=64)  # 经营范围

    crawled_time = IntegerField(default=0)

    class Meta:
        database = mysqldb
        table_name = 'huoche_dealer'
