import collections
import six
import os
import json


def is_sequence(seq):
    """Returns a true if its input is a collections.Sequence (except strings).
    Args:
      seq: an input sequence.
    Returns:
      True if the sequence is a not a string and is a collections.Sequence.
    """
    return (isinstance(seq, collections.Sequence)
            and not isinstance(seq, six.string_types))


def is_string_like(s):
    return isinstance(s, six.string_types) or isinstance(s, six.binary_type) or isinstance(s, bytearray)


def closest_parser_engine_json(fn='parser_engine.json', path='.', prevpath=None):
    """Return the path to the closest parser_engine.json file by traversing the current
    directory and its parents
    """
    if path == prevpath:
        return ''
    path = os.path.abspath(path)
    cfgfile = os.path.join(path, fn)
    if os.path.exists(cfgfile):
        return cfgfile
    return closest_parser_engine_json(os.path.dirname(path), path)


def load_scrapy_settings():
    # FIXME: get scrapy project settings from outside
    from scrapy.settings import Settings
    settings = Settings()
    settings_module_path = os.environ.get('SCRAPY_ENV')
    settings.setmodule(settings_module_path, priority='project')
    return settings


def load_config_data():
    settings = load_scrapy_settings()
    db_table = settings.get('PARSER_ENGINE_CONFIG_TABLE')
    if db_table:
        # todo
        pass
    else:
        config_path = settings.get("PARSER_ENGINE_CONFIG_FILE", 'parser_engine.json')
        if not os.path.isabs(config_path):
            config_path = closest_parser_engine_json(config_path)
        with open(config_path) as f:
            return json.loads(f.read())
