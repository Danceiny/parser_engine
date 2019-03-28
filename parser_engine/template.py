# define template in parser engine

import json
import copy
import six

from scrapy.linkextractors import LinkExtractor

from .utils import is_string
from . import log


class PETemplate(object):
    def __init__(self, name, fields=None, **kwargs):
        self.name = name
        self.fields = fields
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def __getattr__(self, item):
        return self.get(item)

    @classmethod
    def from_json(cls, s):
        if not s:
            raise RuntimeError(
                "init " + cls.__name__ + " from empty json/dict error, maybe the template not found by id?")
        s = copy.deepcopy(s)
        if not isinstance(s, dict):
            try:
                s = json.loads(s)
            except json.decoder.JSONDecodeError as e:
                raise e
        fields = s.pop("fields", tuple())
        if fields:
            fields = [PEField(field.pop('key'), **field) for field in fields if field.get('key')]
        return cls(s.pop('name'), fields, **s)

    def get(self, key):
        try:
            return self.__getattribute__(key)
        except AttributeError:
            pass

    def get_link_extractor(self):
        return LinkExtractor(allow=self.get('allow'),
                             deny=self.get('deny'),
                             allow_domains=self.get('allow_domains'),
                             deny_domains=self.get('deny_domains'),
                             restrict_css=self.get('restrict_css'),
                             restrict_xpaths=self.get('restrict_xpaths'))


# {
#   css: css query in scrapy Selector.css
#   xpath: xpath query in scrapy Selector.xpath
#   tags: [] // like div, a,  etc. e.g: [div,a] => div->a
#   classes: [] // css class match, e.g: classes=["classA", "classB"] => class="classA classB"
#   attributes: string // xpath [{attributes}]
#   position: int
#   key: string // value's key
#   value_type: A_tuple // for simple type cast
#   regexp: string // regular expression must be matched, for scrapy.Selector.re use
#   attr_name: string // attributes name, e.g: "href", "src"
#   parent: map, // contains one of xpath/css/json_key/json_path, should return an iterable list after parsing
#   json_key  // to get "json_value" in {"json_key":"json_value"}
#   json_path // to get "json_value" in {"json_key":"json_value"} using jsonpath expression
#   mapper map // for mapping raw value to another value
# }

class PEField(dict):
    def __init__(self, key, **kwargs):
        kwargs['key'] = key
        super().__init__(**kwargs)
        if not self.xpath and self.tags:
            self._compile_xpath()
        if not self.css and self.attr_name:
            self._compile_css()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '<PEField> ' + json.dumps(self, indent=2)

    def __getattr__(self, item):
        return self.get(item)

    def _compile_xpath(self):
        self._compile_xpath_tag_condition()
        self.xpath = ".//{tag}{tag_condition}{attribute_to_extract}{suffix}".format(
            # match tag
            tag='/'.join(self.tags),
            # tag match attribute
            tag_condition='[' + self.tag_condition + "]" if self.tag_condition
            # tag match position (without attribute match provided)
            else self.get_xpath_by_position(self.position),
            # select attribute
            attribute_to_extract="/@" + self.attr_name if self.attr_name else "",
            # select text as default (without attr_name provided)
            suffix="/text()" if not self.attr_name else "",
        )

        log.debug("field [%s] xpath: \"%s\"" % (self.key, self.xpath))

    def _compile_css(self):
        # todo: compile complicated css like `response.css('a[href*=image] img::attr(src)').getall()`
        pass

    def _compile_xpath_tag_condition(self):
        attr = self.attributes
        if is_string(attr):
            self.tag_condition = attr
        elif isinstance(attr, dict):
            s = []
            for k, v in attr.items():
                s.append('@' + k + '=' + self._cast_value(v))
            self.tag_condition = 'and'.join(s)
        elif isinstance(attr, list):
            s = []
            for i in attr:
                s.append('@' + i[0] + self._cast_operator(i[1]) + self._cast_value(i[2]))

            self.tag_condition = 'and'.join(s)

    @staticmethod
    def _cast_operator(origin):
        return origin

    @staticmethod
    def _cast_value(origin):
        if is_string(origin):
            return '"' + origin + '"'
        return origin

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
