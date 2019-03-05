# -*- coding: utf-8
from parser_engine.utils import *

if __name__ == '__main__':
    p = closest_parser_engine_json('.json')
    assert p == ''

    data = load_config_data()
