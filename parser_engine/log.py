# logger

from .config import logging


def pretty_dict_str(data):
    return '\n'.join([str(k) + ':\t' + str(v) for k, v in data.items()])


def log(level, data, *msgs, **kwargs):
    logging.log(level, "[parser-engine] %s %s %s", str(data), ' '.join([str(msg) for msg in msgs]),
                pretty_dict_str(kwargs))


def info(data, *msgs, **kwargs):
    log(logging.INFO, data, *msgs, **kwargs)


def debug(data, *msgs, **kwargs):
    log(logging.DEBUG, data, *msgs, **kwargs)


def warning(data, *msgs, **kwargs):
    log(logging.WARNING, data, *msgs, **kwargs)


def error(data, *msgs, **kwargs):
    log(logging.ERROR, data, *msgs, **kwargs)
