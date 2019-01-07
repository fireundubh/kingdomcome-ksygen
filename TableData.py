import os

from stdlib.ZipFilePatch import ZipFileFixed


class TableData:
    def __init__(self, table, table_data_path):
        self._table_data_path = table_data_path

        self._relative_path, self._field_data = table.split('\t')

        _, relative_path_tail = os.path.split(self._relative_path)
        self._file_name, _ = os.path.splitext(relative_path_tail)

    @property
    def name(self):
        return self._file_name

    @name.setter
    def name(self, value):
        self._file_name = value

    @property
    def yaml_name(self):
        return '%s.yml' % self._relative_path[:-4]

    @property
    def field_data(self):
        return self._field_data.split(';')

    def get_field_types(self):
        result = list()

        for field_attributes in self.field_data:
            _, field_type = field_attributes.split(',')
            result.append(field_type)

        return result

    def has_padding(self):
        with ZipFileFixed(self._table_data_path) as f:
            table_path = os.path.join('Libs\Tables', self._relative_path)
            table_path = table_path.replace(os.path.sep, '/')
            tbl_data = f.open(table_path).read()
            return tbl_data.find(b'\xff' * 16) > -1
