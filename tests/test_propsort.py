from propsort.main import *


def test_missing_keys():
    sorted = sort(['k1=v1', 'k2=v2', 'k3=v3'], ['k4:v4-alt', 'k3 = v3-alt'])
    assert sorted.missing_keys == ['k1', 'k2']


def test_missing_keys_on_files():
    formatted = format_result(sort(nl("missing1_ref"), nl("missing1_tosort")))
    assert formatted == nl("missing1_res")


def test_sort_complete_files():
    assert sort(nl("sort1_ref"), nl("sort1_tosort")).lines == nl("sort1_res")



def test_to_logical_lines():
    assert to_logical_lines(nl('to_logical_lines1')) == [
        LogicalLine(None, None, ['# c1']),
        LogicalLine('k1', 'v1', ['k1 = v1']),
        LogicalLine('k2', 'v2', ['k2 : v2']),
        LogicalLine('k3', 'v3-p1 \\', ['k3   v3-p1 \\', '    v3-p2']),
        LogicalLine(None, None, ['']),
        LogicalLine(None, None, [' ! c2']),
        LogicalLine('k4', '', ['k4']),
    ]


def test_line_starting_with_hash_or_excl_mark_is_comment():
    assert_function_on_cases(is_comment, {
        '#': True,
        '!': True,
        ' # comment': True,
        ' ! comment': True,
        '\t\t#comment': True,
        '\t\t!comment': True,
        ' key = value # comment': False,
        ' key = value ! comment': False,
    })


def test_line_with_whitespaces_only_is_empty():
    assert_function_on_cases(is_empty, {
        '': True,
        ' \t ': True,
        ' key ': False,
    })


def test_line_ending_with_odd_number_of_backslashes_is_terminated():
    assert_function_on_cases(is_terminated, {
        ' key = value ':        True,
        ' key = v\\alue':       True,
        ' key = value \\\\':    True,
        ' key = value \\ ':     True,
        ' key = value \\':      False,
        ' key = value \\\\\\':  False
    })


def test_line_without_value_is_parsed_to_key_value_pair():
    assert_function_on_cases(to_key_value, {
        'key':                 ('key', ''),
        'key ':                ('key', ''),
        'key=':                ('key', ''),
        'key:':                ('key', ''),
        'key:=':               ('key', '='),
        'key: ':               ('key', ''),
        'key : ':              ('key', ''),
        'key = ':              ('key', ''),
        'key  ':               ('key', '')
    })


def test_line_with_key_vlaue_is_parsed_to_key_value_pair():
    assert_function_on_cases(to_key_value, {
        'key=value':           ('key', 'value'),
        'key= value':          ('key', 'value'),
        '   key   =   value':  ('key', 'value'),
        ' key   :   value':    ('key', 'value'),
        'key:value':           ('key', 'value'),
        'key: value':          ('key', 'value'),
        'key value':           ('key', 'value'),
        'key  value':          ('key', 'value'),
        'key   =  value  ':    ('key', 'value  ')
    })


def test_line_with_special_characters_is_parsed_to_key_value_pair():
    assert_function_on_cases(to_key_value, {
        'key value=':          ('key', 'value='),
        'key\= value=':        ('key\=', 'value='),
        'key\= = value=':      ('key\=', 'value='),
        'key\=: value=':       ('key\=', 'value='),
        'key\=\:\ :=value=':   ('key\=\:\ ', '=value='),
        'key\= = \=value=':    ('key\=', r'\=value='),
        '\=========':          ('\=', '======='),
        '\=\:\  :   ':         ('\=\:\ ', ''),
        '# test = test':       ('#', 'test = test'),
        '#':                   ('#', ''),
        'key = value\\':       ('key', 'value\\')
    })


def test_line_with_wrong_key_value_format_is_not_parsed_to_key_value_pair():
    assert_function_on_cases(to_key_value, {
        '':    (None, None),
        '   ': (None, None),
        ':':   (None, None),
        '===': (None, None),
        '=:=': (None, None)
    })


def assert_function_on_cases(fn, cases):
    for c in cases:
        assert fn(c) == cases[c], '{0}({1}) returns {2}, expected {3}'.format(fn.__name__, c, fn(c), cases[c])


def nl(name):
    """Get natural lines for a testing properties file"""
    filename = 'tests/test_files/{}.properties'.format(name)
    return natural_lines_for(filename)

