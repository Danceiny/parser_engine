from parser_engine import TemplateAnnotation

from parser_engine.spider import PESpider
from parser_engine.decorator import find_by_id


def find_by_id_mock(tpl_id):
    """
    todo: improve query performance
    :param tpl_id:
    :return:
    """
    print('find_by_id_mock', tpl_id)
    return {
               "name": "demo",
               "itemname": "DemoItem",
               "fields": [
                   {
                       "dom_id": None,
                       "_css": None,
                       "xpath": None,
                       "tags": [
                           "h3"
                       ],
                       "classes": [],
                       "attributes": None,
                       "position": None,
                       "key": "steps",
                       "value_type": None,
                       "attr_name": "id"
                   }
               ]
           },


find_by_id = find_by_id_mock


def test_parse_start_url():
    @TemplateAnnotation(start_url_tpl=('demo',))
    class Spider(PESpider):
        name = "test"
        pass

    s = Spider()
    for rule in s.start_url_rules:
        print(rule.cb_kwargs.get('tpl_id'))
    try:
        s._parse_start_url(None, 'demo404')
        assert False
    except Exception as e:
        print(e)


if __name__ == '__main__':
    test_parse_start_url()
