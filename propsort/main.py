import click
from parsing import to_logical_lines
from sorting import Sorter
from printing import to_formatted_output


def get_lines_for(path):
    with open(path, 'r') as f:
        return f.read().splitlines()


def to_sorted_output(template, file_to_sort):
    parse = lambda f: to_logical_lines(get_lines_for(f))
    llines_tmpl = parse(template)
    llines_tosort = parse(file_to_sort)
    sorter = Sorter(llines_tmpl, llines_tosort)
    return to_formatted_output(sorter)


@click.command()
@click.argument('template', type=click.Path(exists=True))
@click.argument('file-to-sort', type=click.Path(exists=True))
def cli(template, file_to_sort):
    """Sort the Properties file according to a given template."""
    output_lines = to_sorted_output(template, file_to_sort)
    for l in output_lines:
        click.echo(l)




