class MusicFile:
    def __init__(self, path: str):
        self.path = path

    def decode(self):
        with open(self.path) as music_file:
            print(music_file)
