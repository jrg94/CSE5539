import json
import os
import pathlib

from musiviz import m4a_parse


class MusicFile:

    def __init__(self, path: str):
        self.path = path
        self._raw_json = None
        self.genre = None
        self.title = None
        self.artist = None

    def __str__(self):
        output = (
                    "Title: %s\n"
                    "Artist: %s\n"
                    "Genre: %s"
                  )
        formatting = (
            self.title,
            self.artist,
            self.genre
        )
        return output % formatting

    def load(self):
        self._raw_json = m4a_parse.decode(self.path)
        self._populate_fields()
        self._output_parse()
        print("*********")
        print(self)

    def _output_parse(self):
        data_dir = "data\\" + "\\".join(self.path.split("\\")[-3:-1])
        json_name = self.path.split("\\")[-1].replace(".m4a", ".json")
        pathlib.Path(data_dir).mkdir(parents=True, exist_ok=True)
        with open(os.path.join(data_dir, json_name), "w") as f:
            print(json.dumps(self._raw_json, indent=2, sort_keys=True, ensure_ascii=False), file=f)

    def _populate_fields(self):
        self._extract_meta_data()

    def _extract_meta_data(self):
        """
        Extracts the genre from the json data.

        :return: None
        """
        entries = self._raw_json["data"]["moov"]["children"]["udta"]["children"]["meta"]["children"]["ilst"]["entries"]
        genre_meta_data = next((entry for entry in entries if entry["meta_code"] == "gnre"))
        self.genre = genre_meta_data["tag"]
        title_meta_data = next((entry for entry in entries if entry["meta_code"] == "©nam"))
        self.title = title_meta_data["data"]
        title_meta_data = next((entry for entry in entries if entry["meta_code"] == "©ART"))
        self.artist = title_meta_data["data"]
