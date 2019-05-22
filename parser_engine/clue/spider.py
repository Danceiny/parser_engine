# define clue relative scrapy spider class
from . import *
from peewee import DoesNotExist
from parser_engine.spider import PESpider
from .models import ClueModel


class ClueSpider(PESpider):
    def finish_clue(self, response, dw_count=0):
        """
        mark clue as finished
        :param response: scrapy.http.Response
        :param dw_count: a number to compare with DW (data center), items count usually
        """
        meta = response.meta
        clue_id = meta.get('clue_id')
        self.log("after yield, update clue_id: %s" % clue_id)
        if clue_id:
            try:
                clue = ClueModel.get_by_id(clue_id)  # may raise DoesNotExist
            except DoesNotExist as e:
                self.error("clue_id: {clue_id} not found, exception: {e}".format(clue_id=clue_id, e=str(e)))
                return
            clue.success()
            clue.dw_count = dw_count
            clue.save()
