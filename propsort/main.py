import re
from collections import namedtuple
import click

LogicalLine = namedtuple('LogicalLine', ['key', 'value', 'natural_lines'])

"""
The propsort implementation revolves around logical lines, as described in
http://docs.oracle.com/javase/7/docs/api/java/util/Properties.html#load(java.io.Reader)

A logical line has the following fields:
 - key: The key for lines which define a key-value pair. None for empty/comment lines.
 - value: Value contained in first natural line. None for empty/comment lines.
 - natural_lines: List of natural lines that comprise a logical line.
"""


def is_comment(line):
    return re.search(r'^\s*[!#]', line) is not None


def is_empty(line):
    return len(line.strip()) == 0 is not None


def is_terminated(line):
    """Return true if value continues on next line"""
    m = re.search(r'\\+$', line)
    return m is None or len(m.group(0)) % 2 == 0


def to_key_value(line):
    """Parse a line into a (key,value) tuple"""
    pair = re.match(r'\s*(?P<key>((\\[ =:])|[^ =:\s])+)\s*([=: ]\s*(?P<value>.*))?$', line)
    if pair is None:
        return None, None
    else:
        return pair.group('key'), pair.group('value') or ''


def natural_lines_for(path):
    with open(path, 'r') as f:
        return f.read().splitlines()


def to_logical_lines(natural_lines):
    """ Parse natural lines into a list of logical lines."""
    lines = []
    terminated_logical_line = True

    for l in natural_lines:

        if is_comment(l):
            lines.append(LogicalLine(natural_lines=[l], key=None, value=None))
            continue

        if not terminated_logical_line:
            lines[-1].natural_lines.append(l)
            terminated_logical_line = is_terminated(l)
            continue

        if is_empty(l):
            lines.append(LogicalLine(natural_lines=[l], key=None, value=None))
            continue

        key, value = to_key_value(l)
        if key is not None:
            lines.append(LogicalLine(natural_lines=[l], key=key, value=value))
            terminated_logical_line = is_terminated(l)

    return lines


# todo: detect missing/duplicated files
def sort(tmpl_natural_lines, tosrt_natural_lines):
    tmpl_logic_lines = to_logical_lines(tmpl_natural_lines)
    tosrt_logic_lines = to_logical_lines(tosrt_natural_lines)

    for (key, value, natural_lines) in tmpl_logic_lines:
        if key is None:
            yield natural_lines[0]
        else:
            matched_line = filter(lambda x: x.key == key, tosrt_logic_lines)[0]
            yield natural_lines[0][:-len(value)] + matched_line.value
            for l in matched_line.natural_lines[1:]:
                yield l


@click.command()
@click.argument('template', type=click.Path(exists=True))
@click.argument('file-to-sort', type=click.Path(exists=True))
def cli(template, file_to_sort):
    """Sort the Properties file according to a given template."""
    tmpl_natural_lines = natural_lines_for(template)
    tosrt_natural_lines = natural_lines_for(file_to_sort)
    for l in sort(tmpl_natural_lines, tosrt_natural_lines):
        click.echo(l)
