from propsort.main import to_sorted_output, get_lines_for
from propsort.parsing import to_logical_lines, _to_key_value, _is_terminated
from propsort.lline import LLine


## -------------------------------
## Propsort tests
## -------------------------------


def test_missing_keys_on_files():
    assert_files_equal("missing1")


def test_duplicated_keys_on_files():
    assert_files_equal("duplicated1")


def test_sort_complete_files():
    assert_files_equal("sort1")


## -------------------------------
## Parser tests
## -------------------------------

def test_to_logical_lines():
    assert to_logical_lines(get_lines_for(f('to_logical_lines1'))) == [
        LLine(None, None, ['# c1']),
        LLine('k1', 'v1', ['k1 = v1']),
        LLine('k2', 'v2', ['k2 : v2']),
        LLine('k3', 'v3-p1 \\', ['k3   v3-p1 \\', '    v3-p2']),
        LLine(None, None, ['']),
        LLine(None, None, [' ! c2']),
        LLine('k4', '', ['k4']),
    ]


def test_line_ending_with_odd_number_of_backslashes_is_terminated():
    assert_function_on_cases(_is_terminated, {
        ' key = value ':        True,
        ' key = v\\alue':       True,
        ' key = value \\\\':    True,
        ' key = value \\ ':     True,
        ' key = value \\':      False,
        ' key = value \\\\\\':  False
    })


def test_line_without_value_is_parsed_to_key_value_pair():
    assert_function_on_cases(_to_key_value, {
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
    assert_function_on_cases(_to_key_value, {
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
    assert_function_on_cases(_to_key_value, {
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
    assert_function_on_cases(_to_key_value, {
        '':    (None, None),
        '   ': (None, None),
        ':':   (None, None),
        '===': (None, None),
        '=:=': (None, None)
    })


## -------------------------------
## Utils
## -------------------------------

def assert_function_on_cases(fn, cases):
    for c in cases:
        assert fn(c) == cases[c], '{0}({1}) returns {2}, expected {3}'.format(fn.__name__, c, fn(c), cases[c])


def assert_files_equal(testname):
    to_sorted_output(f(testname+'_ref'), f(testname+'_tosort')) == get_lines_for(f(testname+'_res'))


def f(name):
    return 'tests/test_files/{}.properties'.format(name)

