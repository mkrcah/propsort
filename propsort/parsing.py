import re
from lline import LLine


def to_logical_lines(natural_lines):
    """ Parse natural lines into a list of logical lines."""
    lines = []
    terminated_logical_line = True

    for l in natural_lines:

        if _is_comment(l):
            lines.append(LLine(natural_lines=[l], key=None, value=None))
            continue

        if not terminated_logical_line:
            lines[-1].natural_lines.append(l)
            terminated_logical_line = _is_terminated(l)
            continue

        if _is_empty(l):
            lines.append(LLine(natural_lines=[l], key=None, value=None))
            continue

        key, value = _to_key_value(l)
        if key is not None:
            lines.append(LLine(natural_lines=[l], key=key, value=value))
            terminated_logical_line = _is_terminated(l)

    return lines


# ----------------------------------
# Helper parsing functions
# ----------------------------------

def _is_comment(line):
    return re.search(r'^\s*[!#]', line) is not None


def _is_empty(line):
    return len(line.strip()) == 0


def _is_terminated(line):
    """Return true if value continues on next line"""
    m = re.search(r'\\+$', line)
    return m is None or len(m.group(0)) % 2 == 0


def _to_key_value(line):
    """Parse a line into a (key,value) tuple"""
    pair = re.match(r'\s*(?P<key>((\\[ =:])|[^ =:\s])+)\s*([=: ]\s*(?P<value>.*))?$', line)
    if pair is None:
        return None, None
    else:
        return pair.group('key'), pair.group('value') or ''

