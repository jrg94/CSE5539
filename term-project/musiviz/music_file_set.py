from musiviz.music_file import MusicFile
import json


class MusicFileSet:

    def __init__(self):
        self.collection = list()

    def __str__(self):
        return "*************\n".join([str(file) for file in self.collection])

    def add(self, path: str):
        """
        Adds a song by path to the collection.

        :param path: the file path of the song
        :return: None
        """
        song = MusicFile(path)
        song.load()
        self.collection.append(song)

    def as_json_text(self) -> str:
        """
        Returns the json format of the collection.

        :return: the music set as json
        """
        return json.dumps([file.__dict__ for file in self.collection], indent=4)
