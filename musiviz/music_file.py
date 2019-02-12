import os
import json
from musiviz import m4a_parse

ATOMS = [
    "moov",
    "trak",
    "mdia",
    "minf",
    "stbl",
    "udta",
]


class MusicFile:

    def __init__(self, path: str):
        self.path = path

    def decode(self):
        with open(self.path, "rb") as music_file:
            os_file_size = os.path.getsize(self.path)
            file_chunks = m4a_parse.read_chunks(music_file, os_file_size)
            file_dict = m4a_parse.create_root_dict(self.path, file_chunks)
            m4a_parse.traverse_atoms(file_chunks, file_dict["data"])
            with open("mapping.json", "w") as f:
                print(json.dumps(file_dict, indent=2, sort_keys=True), file=f)
