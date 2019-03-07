from parser_engine.template import PETemplate

if __name__ == '__main__':
    assert PETemplate("name", None, ha=10).ha == 10
    assert PETemplate("name", None, ha=10).get('ha') == 10
    assert PETemplate("name", None).get('ha') is None
    assert PETemplate("name", None).ha is None
