# -*- coding: utf-8 -*-
from cpca import transform
from playhouse.shortcuts import dict_to_model
from .items import HuocheDealerItem, HuocheDealerModel
from .logger import DwLogger


class HuocheDealerItemPipeline(object):
    """
    地址分词，https://github.com/DQinYuan/chinese_province_city_area_mapper
    """

    def process_item(self, item, spider):
        if isinstance(item, HuocheDealerItem):
            if item.get('address') and (not item.get('province') or not item['city']):
                dataframe = transform([item['address']])
                item['province'] = dataframe['省'].values[0]
                item['city'] = dataframe['市'].values[0]
            if item.get('tags') and isinstance(item['tags'], list):
                item['tags'] = ','.join(item['tags'])
        return item


class HuocheDealerDwPipeline(object):

    def __init__(self):
        self.logger = DwLogger()

    def process_item(self, item, spider):
        if isinstance(item, HuocheDealerItem):
            self.logger.log_to_dw("huoche_dealer", **item)
        return item


class HuocheDealerMySQLPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, HuocheDealerItem):
            if not HuocheDealerModel.table_exists():
                HuocheDealerModel.create_table()
            try:
                model = HuocheDealerModel.get_or_none(dealer_id=item.get('dealer_id'), channel=item['channel'])
                if model:
                    HuocheDealerModel.update(**item).where(HuocheDealerModel.id == model.id).execute()
                else:
                    model = dict_to_model(HuocheDealerModel, item, True)
                    model.save()
            except Exception as e:
                spider.error("huoche_dealer MySQL pipeline failed, exception: %s" % str(e))
                print(item)
        return item
