from scrapy.downloadermiddlewares.retry import RetryMiddleware
from .models import ClueModel


class ClueRetryMiddleware(RetryMiddleware):
    def _retry(self, request, reason, spider):
        ret = super()._retry(request, reason, spider)
        if ret:
            return ret
        # failed clue
        clue_id = request.meta.get('clue_id')
        if clue_id:
            clue = ClueModel.get_by_id(clue_id)
            if clue.status == 200:
                spider.debug("!!!retry a successful clue!!!")
            else:
                clue.fail()
                clue.save()
