# -*- coding: utf-8 -*-
from scrapy.item import Item, Field


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
