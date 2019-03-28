# -*- coding: utf-8 -*-
import json
from parser_engine.patch import get_redis
from parser_engine.singleton import Singleton


@Singleton
class DwLogger:
    def __init__(self, write_filename='dw_local.txt'):
        from scrapy.utils import project
        settings = project.get_project_settings()
        self.r = get_redis(**settings.getdict('REDIS_PARAMS'))
        self.ENV = settings.get('ENV')
        if write_filename:
            self.f = open(write_filename, 'a+')
        else:
            self.f = None

    def __del__(self):
        if self.f:
            self.f.close()

    def log_to_dw(self, action, **data):
        if self.ENV == 'local':
            if self.f:
                self.f.write(json.dumps(data) + '\n')
            return

        # dev环境才打数据到dw
        pass
