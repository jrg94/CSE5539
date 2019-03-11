from musiviz.music_file import MusicFile


class MusicFileSet:

    def __init__(self):
        self.collection = list()

    def __str__(self):
        return "*************\n".join([str(file) for file in self.collection])

    def add(self, path: str):
        song = MusicFile(path)
        song.load()
        self.collection.append(song)