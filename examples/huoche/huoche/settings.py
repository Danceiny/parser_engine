# -*- coding: utf-8 -*-

BOT_NAME = 'huoche'

SPIDER_MODULES = ['huoche.spiders']
NEWSPIDER_MODULE = 'huoche.spiders'

SCHEDULER = "scrapy_redis.scheduler.Scheduler"
DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

REDIS_PARAMS = {
    "url": "redis://127.0.0.1:6379"
}
MYSQL_HOST = '127.0.0.1'
MYSQL_PORT = 3306
MYSQL_USER = 'root'
MYSQL_PASSWORD = ''
MYSQL_DATABASE = 'crawler'
ENV = 'local'

SCHEDULER_PERSIS = True
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'
REDIS_START_URLS_KEY = BOT_NAME + ":" + '%(name)s:start_urls'

PARSER_ENGINE_CONFIG_FILE = "gaode_pe.json"
ROBOTSTXT_OBEY = False

DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": 543
}
RETRY_TIMES = 1
RETRY_HTTP_CODES = []
ITEM_PIPELINES = {
    'huoche.pipelines.HuocheDealerMySQLPipeline': 339,
    'huoche.pipelines.HuocheDealerDwPipeline': 340,
    'parser_engine.clue.pipelines.CluePersistentPipeline': 341,
    'parser_engine.clue.pipelines.CluePipeline': 342,
}