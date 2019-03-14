import pkg_resources
from .utils import *
import logging


def load_config_data():
    settings = load_scrapy_settings()
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


CONFIG_DATA = None


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
