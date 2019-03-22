from .items import ClueItem
from .models import ClueModel


# persistent Clue
class CluePersistentPipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, ClueItem):
            if not ClueModel.table_exists():
                ClueModel.create_table()
            model = ClueModel.from_item(item)
            model.save()
            item['req'].meta['clue_id'] = model.id
            spider.info('CluePersistentPipeline save clue [clue_id] %s to database' % item['req'].meta.get('clue_id'))
        return item


# route clue to queue
class CluePipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, ClueItem):
            spider.info('CluePipeline route clue [clue_id] %s to queue' % item['req'].meta.get('clue_id'))
            spider.route_clue('%s:%s:start_urls' % (item['project'], item['spider']), item['req'])
        return item
