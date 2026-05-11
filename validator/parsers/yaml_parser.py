import yaml


class YamlParser:

    def load(self, path: str):

        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
