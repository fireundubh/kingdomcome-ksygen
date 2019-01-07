import yaml


class KaitaiDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(KaitaiDumper, self).increase_indent(flow, False)
