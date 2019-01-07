import os

import yaml

from KaitaiDumper import KaitaiDumper


class TableStream:
    def __init__(self, file_path):
        self.file_path = file_path

    @classmethod
    def _format_types(cls, stream):
        stream = stream.replace('type: character_varying', 'size: 12')
        stream = stream.replace('type: quatt', 'size: 28')
        stream = stream.replace('type: uuid', 'size: 16')
        return stream

    def write(self, blocks):
        target_path = os.path.normpath(self.file_path)
        target_folder = os.path.dirname(target_path)

        os.makedirs(target_folder, exist_ok=True)

        with open(target_path, 'a+') as o:
            print('Writing: %s' % target_path)

            for block in blocks:
                stream = yaml.dump(block, Dumper=KaitaiDumper, default_flow_style=False)
                stream = self._format_types(stream)
                o.write(stream)
