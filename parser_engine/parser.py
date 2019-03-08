from scrapy.selector import Selector, SelectorList
import json
import jsonpath_rw as jsonpath
from . import utils
from .itemclassloader import ItemClassLoader
from .template import PETemplate
import time


def parse_with_tpl(response, tpl, **context):
    """

    :param response:
    :param tpl:
    :return:
    """
    return PEParser(tpl)(response, **context)


class PEParser(object):

    def __init__(self, tpl=None, **kwargs):
        self.item_loader = ItemClassLoader(**kwargs)
        if isinstance(tpl, PETemplate):
            self.tpl = tpl
        if isinstance(tpl, dict):
            self.tpl = PETemplate.from_json(tpl)

    def __call__(self, response, **context):
        """
        todo: 使用ItemLoader优化 https://docs.scrapy.org/en/latest/topics/loaders.html
        :param response: instance of scrapy.http.Response
        :return: instance of scrapy.Item's subclass
        """
        if utils.is_json_response(response):
            items = self.parse_text(response)
        else:
            items = self.parse_html(response)
        if not items:
            return tuple()
        if not utils.is_sequence(items):
            items = (items,)
        for k, v in context.items():
            for item in items:
                item[k] = v
                item['created_time'] = int(time.time())
        return self.transfer(items)

    def transfer(self, datas):
        item_cls = self.get_item_cls()
        if item_cls:
            return [item_cls(data) for data in datas]
        else:
            return datas

    def parse_html(self, response):
        """
        return
        :param response:
        :return:
        """
        item = {}
        for field in self.tpl.fields:
            selector_list = None
            if field.xpath:
                selector_list = response.xpath(field.xpath)
            elif field.css:
                selector_list = response.css(field.css)
            if selector_list:
                if field.regexp:
                    v = selector_list.re(field.regexp)
                else:
                    v = selector_list.extract()
                if isinstance(v, Selector):
                    v = v.extract()
                item[field.key] = self.cast(v, field.value_type)
        return item

    def get_item_cls(self):
        return self.item_loader.get(self.tpl.itemname)

    def parse_text(self, response):
        return self._parse_text(response.body)

    def _parse_text(self, body):
        data = json.loads(body)
        parent = self.tpl.parent
        if parent:
            parent_json_key = parent.get('json_key')
            if parent_json_key:
                data = data[parent_json_key]
            else:
                data = data[parent.get('json_path')]
        if utils.is_sequence(data):
            items = []
            for d in data:
                item = {}
                continue_flag = False
                if isinstance(d, dict):
                    if self.tpl.extract_keys:
                        for key in self.tpl.extract_keys:
                            item[key] = d.get(key)
                    elif self.tpl.extract_keys_map:
                        for json_key, key in self.tpl.extract_keys_map.items():
                            item[key] = d.get(json_key)
                else:
                    for field in self.tpl.fields:
                        value = None
                        if field.json_key:
                            value = d.get(field.json_key)
                        elif field.json_path:
                            value = [match.value for match in jsonpath.parse(field.json_path).find(d)]
                        # FIXME: more robust required check
                        if not value and field.default_value is not None:
                            value = field.default_value
                        else:
                            value = self.cast(value, field.value_type)
                        if field.required and not value:
                            continue_flag = True
                            break
                        item[field.key] = value
                if not continue_flag and item:
                    items.append(item)
            return items
        else:
            item = {}
            for field in self.tpl.fields:
                try:
                    item[field.key] = self.cast([match.value for match in jsonpath.parse(field.json_path).find(data)],
                                                field.value_type)
                except Exception as e:
                    self.log(e)
            return item,  # Attention: return iterable tuple

    @staticmethod
    def log(*msgs):
        print("[parser engine] " + ' '.join([str(msg) for msg in msgs]))

    @staticmethod
    def cast(o, t):
        """

        :param o: origin value
        :param t: type
                    singleton
                    map
                    string
                    int
                    long
                    float
        :return:
        """
        if not t:
            return o
        elif t == 'singleton':
            if utils.is_sequence(o):
                return o[0]
            return o
        elif t == 'map' and utils.is_string_like(o):
            return json.loads(o)
        elif t == 'int':
            return int(o)
        elif t == 'float':
            return float(o)
        elif t == 'string':
            return str(o)
        else:
            return o
