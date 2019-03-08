from scrapy.item import DictItem

from .log import info


def __setitem__(self, key, value):
    if key in self.fields:
        self._values[key] = value
    else:
        info("%s does not support field: %s, but PE will ignore" %
             (self.__class__.__name__, key))


DictItem.__setitem__ = __setitem__
