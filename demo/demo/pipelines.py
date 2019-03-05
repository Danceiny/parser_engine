# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import logging
from demo.items import LeadsItem, Leads


class DuplicatesPipeline(object):
    def __init__(self):
        self.leads_id_set = set()
        self.leads_name_set = set()

    def process_item(self, item, spider):
        channel_id = item['channel_id']
        name = item['name']
        if channel_id in self.leads_id_set:
            pass
        if name in self.leads_name_set:
            pass
        self.leads_id_set.add(channel_id)
        self.leads_name_set.add(name)
        return item


class MongoDBPipeline(object):
    collection_name = 'leads'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert(dict(item))
        logging.debug("item added to MongoDB")
        return item


class MySQLPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, LeadsItem):
            if not Leads.table_exists():
                Leads.create_table()
            leads = Leads(
                channel_id=item['channel_id'],
                channel=item['channel'],
                name=item['name'],
                contact=item['contact'],
                contact_type=item['contact_type'],
                city=item['city'],
                category=item['category'],
                address=item['address'],
                created_time=item['created_time'],
                extra=item.get('extra', ''))
            leads.save()
            return item
