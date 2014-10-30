from collections import namedtuple

LLine = namedtuple('LLine', ['key', 'value', 'natural_lines'])
"""
The propsort implementation revolves around Logical Lines, as described in
http://docs.oracle.com/javase/7/docs/api/java/util/Properties.html#load(java.io.Reader)

A logical line has the following fields:
 - key: The key for lines which define a key-value pair. None for empty/comment lines.
 - value: Value contained in first natural line. None for empty/comment lines.
 - natural_lines: List of natural lines that comprise a logical line.
"""


def get_llines_with_key(key, llines):
    return filter(lambda x: x.key == key, llines)