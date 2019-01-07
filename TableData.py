from collections import OrderedDict


class Blocks:
    @staticmethod
    def seq():
        result = OrderedDict({'seq': [
            OrderedDict({'id': 'table', 'type': 'header'}),
            OrderedDict({'id': 'rows', 'type': 'row', 'repeat': 'expr', 'repeat-expr': 'table.row_count'}),
            OrderedDict({'id': 'strings', 'type': 'strz', 'repeat': 'expr', 'repeat-expr': 'table.unique_strings_count'}),
        ]})
        return result


class TypeBlocks:
    @staticmethod
    def header():
        result = {'header': {'seq': [
            OrderedDict({'id': 'version', 'type': 's4'}),
            OrderedDict({'id': 'descriptors_hash', 'type': 'u4'}),
            OrderedDict({'id': 'layout_hash', 'type': 'u4'}),
            OrderedDict({'id': 'table_version', 'type': 's4'}),
            OrderedDict({'id': 'row_count', 'type': 's4'}),
            OrderedDict({'id': 'string_data_size', 'type': 's4'}),
            OrderedDict({'id': 'unique_strings_count', 'type': 's4'}),
        ]}}
        return result

    @staticmethod
    def padding():
        result = {'padding': {'seq': [
            OrderedDict({'id': 'padding_type', 'size': 16})
        ]}}
        return result

    @staticmethod
    def quat():
        result = {'quat': {'seq': [
            OrderedDict({'id': 'quat_x', 'type': 's4'}),
            OrderedDict({'id': 'quat_y', 'type': 's4'}),
            OrderedDict({'id': 'quat_z', 'type': 's4'}),
            OrderedDict({'id': 'quat_w', 'type': 's4'}),
        ]}}
        return result

    @staticmethod
    def quatt():
        result = {'quatt': {'seq': [
            OrderedDict({'id': 'quatt_type', 'size': 28})
        ]}}
        return result

    @staticmethod
    def vec3():
        result = {'vec3': {'seq': [
            OrderedDict({'id': 'vec3_x', 'type': 's4'}),
            OrderedDict({'id': 'vec3_y', 'type': 's4'}),
            OrderedDict({'id': 'vec3_z', 'type': 's4'}),
        ]}}
        return result

