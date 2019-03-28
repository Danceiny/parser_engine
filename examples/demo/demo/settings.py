# -*- coding: utf-8 -*-
BOT_NAME = 'demo'
SPIDER_MODULES = ['demo.spiders']
NEWSPIDER_MODULE = 'demo.spiders'
PARSER_ENGINE_CONFIG_FILE = "parser_engine2.json"
SCHEDULER_PERSIS = True
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.7'
ROBOTSTXT_OBEY = False
DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 1
COOKIES_ENABLED = False
ITEM_PIPELINES = {
    'demo.pipelines.DemoPipeline': 350,
}