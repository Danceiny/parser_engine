from scrapy.item import DictItem
from .log import debug


def __setitem__(self, key, value):
    if key in self.fields:
        self._values[key] = value
    else:
        debug("%s does not support field: %s, but PE will ignore" %
              (self.__class__.__name__, key))


DictItem.__setitem__ = __setitem__
