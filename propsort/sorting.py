from itertools import groupby
from lline import get_llines_with_key


class Sorter:
    """ Sort logic lines based on a given template and detect differences in key sets. """

    def __init__(self, tmpl_llines, tosrt_llines):
        self.tmpl_llines = tmpl_llines
        self.tosrt_llines = tosrt_llines
        self.tmpl_keys = Sorter.get_keys(tmpl_llines)
        self.tosrt_keys = Sorter.get_keys(tosrt_llines)


    def sorted(self):
        output = []
        for (key, value, natural_lines) in self.tmpl_llines:
            if key is None:
                output.append(natural_lines[0])
            else:
                matched_logic_lines = get_llines_with_key(key, self.tosrt_llines)
                if len(matched_logic_lines) >= 1:
                    matched = matched_logic_lines[0]
                    output.append(natural_lines[0][:-len(value)] + matched.value)
                    output.extend(matched.natural_lines[1:])
        return output


    @staticmethod
    def get_keys(llines):
        """Get all keys contained in the logical lines"""
        return [ll.key for ll in llines if ll.key is not None]

    def missing_keys(self):
        return set(self.tmpl_keys) - set(self.tosrt_keys)

    def duplicated_keys(self):
        return [k for k, g in groupby(self.tosrt_keys) if len(list(g)) >= 2]

    def unused_keys(self):
        return set(self.tosrt_keys) - set(self.tmpl_keys)

