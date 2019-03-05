from scrapy.selector import Selector
import json
import six
from scrapy.http import HtmlResponse, TextResponse
import jsonpath_rw as jsonpath
from . import utils
from .itemclassloader import ItemClassLoader
from .template import PETemplate
import time


# todo: https://docs.scrapy.org/en/latest/topics/loaders.html
def parse_with_tpl(response, tpl, **context):
    """

    :param response:
    :param tpl:
    :return:
    """
    return PEParser(tpl)(response, **context)


class PEParser(object):

    def __init__(self, tpl=None):
        self.item_loader = ItemClassLoader()
        if isinstance(tpl, PETemplate):
            self.tpl = tpl
        if isinstance(tpl, dict):
            self.tpl = PETemplate.from_json(tpl)

    def __call__(self, response, **context):
        """
        :param response: instance of scrapy.http.Response
        :return: instance of scrapy.Item's subclass
        """
        items = None
        if isinstance(response, HtmlResponse):
            items = self.parse_html(response)
        elif isinstance(response, TextResponse):
            items = self.parse_text(response)
        if not items:
            return
        if not utils.is_sequence(items):
            items = (items,)
        for k, v in context.items():
            for item in items:
                item[k] = v
                item['created_time'] = int(time.time())
        return self.transfer(items)

    def transfer(self, datas):
        return [self.get_item_cls()(data) for data in datas]

    @staticmethod
    def get_xpath_by_position(position):
        if position is None or position == '':
            return ""
        if isinstance(position, six.string_types) and (position.startswith('>') or position.startswith('<')):
            return "[position()%s]" % position
        pos = int(position)
        if pos > 0:
            return "[%d]" % pos
        elif pos < 0:
            return "[last()-%d]" % (abs(pos) - 1)

    def parse_html(self, response):
        """
        return
        :param response:
        :return:
        """
        item = {}
        for field in self.tpl.fields:
            self.log("field", field.key)
            selector_list = None
            if field._xpath:
                selector_list = response.xpath(field.__xpath)
            elif field._css:
                selector_list = response.css(field.__css)
            elif field.dom_id:
                selector_list = response.css(field.dom_id)
            elif field.tags:
                selector_list = response.xpath(
                    "//{tag}{tag_condition}{attribute_to_extract}{suffix}".format(
                        # match tag
                        tag='/'.join(field.tags),
                        # tag match attribute
                        tag_condition='[@' + field.attributes + "]" if field.attributes
                        # tag match position (without attribute match provided)
                        else self.get_xpath_by_position(field.position),
                        # select attribute
                        attribute_to_extract="/@" + field.attr_name if field.attr_name else "",
                        # select text as default (without attr_name provided)
                        suffix="/text()" if not field.attr_name else "",
                    ))
            if selector_list:
                if field.regexp:
                    v = selector_list.re(field.regexp)
                else:
                    v = selector_list.get()
                self.log("selector_list.get() return type", type(v), v)
                if isinstance(v, Selector):
                    item[field.key] = v.get()
                else:
                    item[field.key] = v
        return item

    def get_item_cls(self):
        return self.item_loader.get(self.tpl.itemname)

    def parse_text(self, response):
        data = json.loads(response.text)
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
                    pass
            return item

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
        elif t == 'singleton' and utils.is_sequence(o):
            return o[0]
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
