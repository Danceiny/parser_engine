# -*- coding: utf-8 -*-
class DemoPipeline(object):
    def process_item(self, item, spider):
        print("pipeline receive item, type: ", type(item), item)
        return item
