# logger

from .config import logging


def pretty_dict_str(data):
    return '\n'.join([str(k) + ':\t' + str(v) for k, v in data.items()])


def info(data, *msgs, **kwargs):
    logging.info("%s %s %s", str(data), ' '.join([str(msg) for msg in msgs]),
                 pretty_dict_str(kwargs))


def debug(data, *msgs, **kwargs):
    logging.debug("%s %s %s", str(data), ' '.join([str(msg) for msg in msgs]),
                  pretty_dict_str(kwargs))


def warning(data, *msgs, **kwargs):
    logging.warning("%s %s %s", str(data), ' '.join([str(msg) for msg in msgs]),
                    pretty_dict_str(kwargs))


def error(data, *msgs, **kwargs):
    logging.error("%s %s %s", str(data), ' '.join([str(msg) for msg in msgs]),
                  pretty_dict_str(kwargs))
