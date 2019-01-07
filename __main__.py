import configparser
import os
import shutil
from collections import OrderedDict

import yaml

from TableBlocks import Blocks, TypeBlocks
from TableData import TableData
from TableRow import TableRow
from TableStream import TableStream

ROOT = os.path.dirname(__file__)


def main():
    shutil.rmtree(os.path.join(ROOT, 'out'), ignore_errors=True)

    table_data_path = os.path.join(conf['Game']['Path'], 'Data', 'Tables.pak')

    with open(os.path.join(ROOT, 'tables.csv'), mode='r') as f:
        tables = [TableData(table, table_data_path) for table in f.read().splitlines()]

    for table in tables:
        # create meta block
        meta_block = {'meta': OrderedDict({
            'id': table.name,
            'file-extension': 'tbl',
            'encoding': 'utf-8',
            'endian': 'le'
        })}

        # create seq block
        seq_block = Blocks.seq()

        # create types block
        types_block = {'types': OrderedDict()}

        types_block['types'].update(TypeBlocks.header())

        if table.has_padding():
            types_block['types'].update(TypeBlocks.padding())

        row_type = {'row': {'seq': TableRow(table.field_data).to_list()}}
        types_block['types'].update(row_type)

        field_types = table.get_field_types()

        if 'quat' in field_types:
            types_block['types'].update(TypeBlocks.quat())

        if 'quatt' in field_types:
            types_block['types'].update(TypeBlocks.quatt())

        if 'vec3' in field_types:
            types_block['types'].update(TypeBlocks.vec3())

        table_stream = TableStream(os.path.join(ROOT, 'out', table.yaml_name))
        table_stream.write([meta_block, seq_block, types_block])

    print('Wrote %s files' % len(tables))


if __name__ == '__main__':
    conf = configparser.ConfigParser()
    conf.read(os.path.join(ROOT, 'ksygen.conf'))


    def represent_ordereddict(dumper, data):
        value = list()

        for item_key, item_value in data.items():
            node_key = dumper.represent_data(item_key)
            node_value = dumper.represent_data(item_value)

            value.append((node_key, node_value))

        return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)


    yaml.add_representer(OrderedDict, represent_ordereddict)
    main()
