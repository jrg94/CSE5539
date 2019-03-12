import json
import os

from musiparse.music_file import MusicFile


class MusicFileSet:

    def __init__(self):
        self.collection = list()

    def __str__(self):
        return "*************\n".join([str(file) for file in self.collection])

    def load_from_json(self, file_path: str):
        """
        A helper method for generating a MusicFileSet from json.

        :param file_path: a file path to a json file
        :return: None
        """
        with open(file_path) as f:
            collection = json.load(f)
            for item in collection:
                music_file = MusicFile(item["path"])
                music_file.__dict__ = item
                self.collection.append(music_file)

    def filter_by_genre(self, genre: str) -> 'MusicFileSet':
        """
        Generates a new MusicFileSet from the original collection.

        :param genre: a genre to filter by
        :return: a new MusicFileSet containing only songs of a particular genre
        """
        subset = MusicFileSet()
        subset.collection = [item for item in self.collection if item.genre == genre]
        return subset

    def truncate(self, limit: int) -> 'MusicFileSet':
        """
        Generates a new MusicFileSet from the original collection.

        :param limit: the number of elements in the subset
        :return: a new MusicFileSet containing only a specific number of songs
        """
        subset = MusicFileSet()
        subset.collection = self.collection[:limit]
        return subset

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

    def add_all(self, path: str, genre=None, limit=None):
        """
        A convenience method for adding all files from a path recursively.

        :param path: a path of files
        :param genre: the genre to filter by
        :param limit: the max number of items to read
        :return: None
        """
        count = 0
        for path, dirs, files in os.walk(path):
            for file in files:
                if file.split(".")[-1] == "m4a":
                    count += 1
                    print("Processing #%d: '%s'" % (count, file))
                    try:
                        self.add(os.path.join(path, file), genre)
                        if limit and len(self.collection) >= limit:
                            return
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
