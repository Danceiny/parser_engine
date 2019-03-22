import collections
import six
import os
import json
from scrapy.utils import project
from scrapy.http import HtmlResponse


class classproperty(object):

    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)


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


def is_string(s):
    return isinstance(s, six.string_types)


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


def is_not_empty_list(seq):
    return is_sequence(seq) and len(seq) > 0


def is_html_response(response):
    return isinstance(response, HtmlResponse) \
           and b'text/plain' not in response.headers.get(b'Content-Type', b'') \
           and not is_json(response.body)


def is_json_response(response):
    return is_json(response.body)


def is_json(s):
    try:
        json.loads(s)
        return True
    except ValueError:
        return False
