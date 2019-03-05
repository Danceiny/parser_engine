from parser_engine.parser import PEParser

p = PEParser()
v = p.cast(["daj"], 'singleton')
assert v == "daj"
