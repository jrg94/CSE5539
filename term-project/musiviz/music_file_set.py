from musiviz.music_file import MusicFile


class MusicFileSet:

    def __init__(self):
        self.collection = list()

    def add(self, path: str):
        song = MusicFile(path)
        song.load()
        self.collection.append(song)