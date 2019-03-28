# parse functions

import json
import time

import jsonpath_rw as jsonpath
from scrapy.selector import Selector

from . import utils
from .itemclassloader import ItemClassLoader
from .template import PETemplate
from .log import info, warning, error, debug


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
        elif isinstance(tpl, dict):
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
                item['crawled_time'] = int(time.time())
        return self.transfer(items)

    def transfer(self, datas):
        item_cls = self.get_item_cls()
        if item_cls:
            info(item_cls, "Item class loaded")
            return [item_cls(data) for data in datas]
        else:
            return datas

    def get_item_cls(self):
        return self.item_loader.get(self.tpl.itemname)

    def parse_html(self, response):
        """
        return
        :param response:
        :return:
        """
        return self._parse_html(response)

    def _parse_html(self, root):
        parent = self.tpl.parent
        if parent:
            parent_xpath = parent.get('xpath')
            if parent_xpath:
                root = root.xpath(parent_xpath)
            parent_css = parent.get('css')
            if not parent_css:
                error('parse html response failed, parent node no xpath/css')
                return tuple()
            root = root.css(parent_css)
        if utils.is_sequence(root):
            return self._parse_html_node_list(root)
        else:
            return self._parse_html_item(root),

    def _parse_html_node_list(self, root):
        items = []
        for d in root:
            item = self._parse_html_item(d)
            if item:
                items.append(item)
        return items

    def _parse_html_item(self, root):
        item = {}
        for field in self.tpl.fields:
            selector_list = None
            if field.xpath:
                selector_list = root.xpath(field.xpath)
            elif field.css:
                selector_list = root.css(field.css)
            if selector_list:
                if field.regexp:
                    value = selector_list.re(field.regexp)
                else:
                    value = selector_list.extract()
                if isinstance(value, Selector):
                    value = value.extract()
                break_flag = self._set_item_value(item, value, field)
                if break_flag:
                    return
        return item

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
            return self._parse_text_node_list(data)
        else:
            item = {}
            for field in self.tpl.fields:
                value = None
                if field.json_key:
                    value = data.get(field.json_key)
                elif field.json_path:
                    value = [match.value for match in jsonpath.parse(field.json_path).find(data)]
                break_flag = self._set_item_value(item, value, field)
                if break_flag:
                    return tuple()
            return item,  # Attention: return iterable tuple

    def _parse_text_node_list(self, root):
        items = []
        for d in root:
            item = self._parse_text_item(d)
            if item:
                items.append(item)
        return items

    def _parse_text_item(self, node):
        item = {}
        if self.tpl.extract_keys:
            for key in self.tpl.extract_keys:
                item[key] = node.get(key)
        elif self.tpl.extract_keys_map:
            for json_key, key in self.tpl.extract_keys_map.items():
                item[key] = node.get(json_key)
        else:
            for field in self.tpl.fields:
                value = None
                if field.json_key:
                    value = node.get(field.json_key)
                elif field.json_path:
                    value = [match.value for match in jsonpath.parse(field.json_path).find(node)]
                break_flag = self._set_item_value(item, value, field)
                if break_flag:
                    return
        return item

    def _set_item_value(self, item, value, field):
        """
        :param item: will update it
        :param value:
        :param field: PEField instance
        :return: True => required but missed, which means caller should discard this item
        """
        if not value and field.default_value is not None:
            value = field.default_value
        else:
            value = self.cast(value, field.value_type)
        # FIXME: more robust required check
        if field.required and not value:
            debug("%s required but get false value (shown as json): %s" % (field.key, json.dumps(value)))
            return True
        # do value map, e.g. map 1 to male, and 0 to female
        if field.mapper:
            value = field.mapper.get(value)
        # join list to string
        elif field.join and isinstance(value, list):
            value = field.join.join((str(v) for v in value))
        item[field.key] = value

    @staticmethod
    def cast(o, t):
        """
        cast o to type t
        :param o: origin value
        :param t: type
                    singleton
                    map
                    string
                    int
                    long
                    float
                    striped_string:  maybe very useful in html to remove '\r', '\n', '\t'
        :return:
        """
        if not t:
            return o
        elif t == 'singleton':
            if utils.is_sequence(o) and len(o) > 0:
                return o[0]
            return o
        elif t == 'map' and utils.is_string_like(o):
            return json.loads(o)
        elif t == 'int':
            if utils.is_not_empty_list(o):
                o = o[0]
            return int(o)
        elif t == 'float':
            if utils.is_not_empty_list(o):
                o = o[0]
            return float(o)
        elif t == 'stripped_string':
            if utils.is_not_empty_list(o):
                o = o[0]
            return str(o).strip()
        elif t == 'string':
            if utils.is_not_empty_list(o):
                o = o[0]
            return str(o)
        else:
            return o
