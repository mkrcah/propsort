from lline import get_llines_with_key


def to_formatted_output(sorter):

    output = []
    output.extend(sorter.sorted())

    if len(sorter.missing_keys()):
        _print_header(output, 'Missing keys')
        for k in sorter.missing_keys():
            output.append("# " + k)

    if len(sorter.duplicated_keys()):
        _print_header(output, 'Duplicated keys')
        for k in sorter.duplicated_keys():
            _print_pair(output, k, sorter.tosrt_llines)

    if len(sorter.unused_keys()):
        _print_header(output, 'Unused keys')
        for k in sorter.unused_keys():
            _print_pair(output, k, sorter.tosrt_llines)

    return output


def _print_header(output, title):
    output.append("")
    output.append("")
    output.append("##############################################")
    output.append("## " + title)
    output.append("##############################################")


def _print_pair(output, key, llines):
    for ll in get_llines_with_key(key, llines):
        output.extend(ll.natural_lines)

