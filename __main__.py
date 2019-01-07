import os
import re
import shutil
from collections import OrderedDict

import yaml

from TableData import Blocks, TypeBlocks

ROOT = os.path.dirname(__file__)
TABLES = os.path.join(ROOT, 'tables.csv')


def main():
    delete_folder('out')

    with open(TABLES, mode='r') as f:
        tables = f.read().splitlines()

    for table in tables:
        relative_path, field_data = table.split('\t')
        _, file_name = os.path.split(relative_path)

        # create meta block
        meta_block = {'meta': OrderedDict({
            'id': file_name[:-4],
            'file-extension': 'tbl',
            'encoding': 'utf-8',
            'endian': 'le'
        })}

        # create seq block
        seq_block = Blocks.seq()

        # create types block
        types_block = {'types': OrderedDict()}

        types_block['types'].update(TypeBlocks.header())
        types_block['types'].update(TypeBlocks.padding())
        types_block['types'].update(TypeBlocks.quat())
        types_block['types'].update(TypeBlocks.quatt())

        row_type = {'row': {'seq': build_attributes_list(field_data.split(';'))}}
        types_block['types'].update(row_type)

        types_block['types'].update(TypeBlocks.vec3())

        # create block layout
        block_layout = [meta_block, seq_block, types_block]

        # write block layout to file
        target_file = os.path.join(ROOT, 'out', f'{relative_path[:-4]}.yml')

        print('Writing: %s' % target_file)
        for block in block_layout:
            write_yaml(target_file, block)


def build_attributes_list(field_data):
    result = list()

    for attributes in field_data:
        id_attribute, type_attribute = attributes.split(',')

        key_value_pair = OrderedDict({
            'id': fix_camelcase(id_attribute),
            'type': type_attribute,
        })

        result.append(key_value_pair)

    return result


def delete_folder(relative_path):
    folder_path = os.path.join(ROOT, relative_path)
    shutil.rmtree(folder_path, ignore_errors=True)


def fix_camelcase(s):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def fix_data(stream):
    stream = stream.replace('type: character_varying', 'size: 12')
    stream = stream.replace('type: uuid', 'size: 16')
    return stream


def fix_indentation(stream):
    indent = ' ' * 2
    stream = stream.replace('- id:',
                            f'{indent}- id:')
    stream = stream.replace(f'{indent}type:',
                            f'{indent*2}type:')
    stream = stream.replace(f'{indent}size:',
                            f'{indent*2}size:')
    stream = stream.replace(f'{indent}repeat:',
                            f'{indent*2}repeat:')
    stream = stream.replace(f'{indent}repeat-expr:',
                            f'{indent*2}repeat-expr:')
    return stream


def represent_ordereddict(dumper, data):
    value = list()

    for item_key, item_value in data.items():
        node_key = dumper.represent_data(item_key)
        node_value = dumper.represent_data(item_value)

        value.append((node_key, node_value))

    return yaml.nodes.MappingNode(u'tag:yaml.org,2002:map', value)


def write_yaml(target_file, types_block):
    os.makedirs(os.path.dirname(target_file), exist_ok=True)

    with open(target_file, 'a+') as o:
        stream = yaml.dump(types_block, default_flow_style=False)
        stream = fix_indentation(stream)
        stream = fix_data(stream)
        o.write(stream)


if __name__ == '__main__':
    yaml.add_representer(OrderedDict, represent_ordereddict)
    main()
