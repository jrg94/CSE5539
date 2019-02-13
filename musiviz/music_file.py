import json
from musiviz import m4a_parse


class MusicFile:

    def __init__(self, path: str):
        self.path = path

    def load(self):
        file_dict = m4a_parse.decode(self.path)
        with open("mapping.json", "w") as f:
            print(json.dumps(file_dict, indent=2, sort_keys=True, ensure_ascii=False), file=f)
