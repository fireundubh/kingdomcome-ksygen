import re
from collections import OrderedDict


class TableRow:
    def __init__(self, row_data):
        self.attributes = row_data

    @classmethod
    def _fix_camelcase(cls, value):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', value)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def to_list(self):
        result = list()

        for attributes in self.attributes:
            id_attribute, type_attribute = attributes.split(',')

            key_value_pair = OrderedDict({
                'id': self._fix_camelcase(id_attribute),
                'type': type_attribute,
            })

            result.append(key_value_pair)

        return result
