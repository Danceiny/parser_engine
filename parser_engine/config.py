import pkg_resources
import logging
from peewee import MySQLDatabase

from .utils import *

CONFIG_DATA = None

mysqldb = MySQLDatabase(None)


def load_config_data():
    settings = load_scrapy_settings()
    db_config = settings.getdict('MYSQL')
    if db_config:
        mysqldb.init(db_config.get('DATABASE'), host=db_config.get('HOST', '127.0.0.1'),
                     user=db_config.get('USER', 'root'), passwd=db_config.get('PASSWORD'),
                     port=db_config.get('PORT', 3306))
    elif settings.get('MYSQL_USER'):
        mysqldb.init(settings.get('MYSQL_DATABASE'), host=settings.get('MYSQL_HOST', '127.0.0.1'),
                     user=settings.get('MYSQL_USER', 'root'), passwd=settings.get('MYSQL_PASSWORD'),
                     port=settings.get('MYSQL_PORT', 3306))
    db_table = settings.get('PARSER_ENGINE_CONFIG_TABLE')
    if db_table:
        # todo
        pass
    else:
        config_path = settings.get("PARSER_ENGINE_CONFIG_FILE", 'parser_engine.json')
        if not os.path.isabs(config_path):
            config_path1 = closest_parser_engine_json(config_path)
            if not config_path1:
                resource_package = __name__
                resource_path = '/'.join(('templates', config_path))
                return json.load(pkg_resources.resource_stream(resource_package, resource_path))
            config_path = config_path1
        with open(config_path, mode='rb') as f:
            return json.loads(f.read())


def init_logger():
    logfile = CONFIG_DATA.get("PARSER_ENGINE_LOG_FILE")
    if logfile:
        logging.basicConfig(filename=logfile, filemode='w',
                            format='[parser-engine] %(ascii)s-%(levelname)s %(message)s',
                            level=logging.DEBUG)


def init_config():
    global CONFIG_DATA
    CONFIG_DATA = load_config_data()
    init_logger()


def get_config_data():
    global CONFIG_DATA
    if not CONFIG_DATA:
        init_config()
    return CONFIG_DATA
