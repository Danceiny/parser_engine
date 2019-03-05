import collections
import six
import os
import json
from scrapy.utils import project


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
    return closest_parser_engine_json(fn, os.path.dirname(path), path)


def load_scrapy_settings():
    # FIXME: get scrapy project settings from outside
    return project.get_project_settings()


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
                default_config_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
                config_path1 = closest_parser_engine_json(config_path, default_config_dir)
                if not config_path1:
                    raise FileNotFoundError
            config_path = config_path1
        with open(config_path, mode='rb') as f:
            return json.loads(f.read())
