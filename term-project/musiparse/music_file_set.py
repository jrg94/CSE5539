import json
import os

from musiparse.music_file import MusicFile


class MusicFileSet:

    def __init__(self):
        self.collection = list()

    def __str__(self):
        return "*************\n".join([str(file) for file in self.collection])

    def add(self, path: str, genre=None):
        """
        Adds a song by path to the collection.

        :param path: the file path of the song
        :param genre: a genre filter
        :return: None
        """
        song = MusicFile(path)
        song.load()
        if not genre or genre == song.genre:
            self.collection.append(song)

    def add_all(self, path: str, genre=None):
        """
        A convenience method for adding all files from a path recursively.

        :param path: a path of files
        :param genre: the genre to filter by
        :return: None
        """
        for path, dirs, files in os.walk(path):
            for file in files:
                if file.split(".")[-1] == "m4a":
                    print("Processing '%s'" % file)
                    try:
                        self.add(os.path.join(path, file), genre)
                    except:
                        print("- Failed to process '%s'" % file)

    def as_json_text(self) -> str:
        """
        Returns the json format of the collection.

        :return: the music set as json
        """
        return json.dumps([file.__dict__ for file in self.collection], indent=4)

    def to_json(self, path: str):
        """
        Dumps the set of music files to JSON for interpretation in D3.

        :param path: a path to a string file
        :return: None
        """
        with open(path, "w") as out:
            json.dump([file.__dict__ for file in self.collection], out, indent=4)
