import json
import os
import pathlib

from musiviz import m4a_parse


class MusicFile:

    def __init__(self, path: str):
        self.path = path
        self._raw_json = None

    def load(self):
        self._raw_json = m4a_parse.decode(self.path)
        data_dir = "data\\" + "\\".join(self.path.split("\\")[-3:-1])
        json_name = self.path.split("\\")[-1].replace(".m4a", ".json")
        pathlib.Path(data_dir).mkdir(parents=True, exist_ok=True)
        with open(os.path.join(data_dir, json_name), "w") as f:
            print(json.dumps(self._raw_json, indent=2, sort_keys=True, ensure_ascii=False), file=f)
