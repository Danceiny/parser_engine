# define template in parser engine

import json
import copy


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
            raise RuntimeError("init " + cls.__name__ + " from empty json/dict")
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


# {
#   dom_id: string // document.getElementById
#     _css: css query in scrapy Selector.css
#     _xpath: xpath query in scrapy Selector.xpath
#   tags: [] // like div, a,  etc. e.g: [div,a] => div->a
#   classes: [] // css class match, e.g: classes=["classA", "classB"] => class="classA classB"
#   attributes: string // xpath [@{attributes}]
#   position: int
#
#   key: string // value's key
#   value_type: A_tuple // for simple type cast
#   regexp: string // regular expression must be matched, for scrapy.Selector.re use
#   attr_name: string // attributes name, e.g: "href", "src"
#
#   parent: map, // with some k-v to find parent node
#   json_key  // to get "json_value" in {"json_key":"json_value"}
#   json_path // to get "json_value" in {"json_key":"json_value"} using jsonpath expression
# }
class PEField(dict):
    def __init__(self, key, **kwargs):
        kwargs['key'] = key
        super().__init__(**kwargs)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '<PEField> ' + json.dumps(self, indent=2)

    def __getattr__(self, item):
        return self.get(item)
