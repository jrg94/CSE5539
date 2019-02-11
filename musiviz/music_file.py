import struct

class MusicFile:
    def __init__(self, path: str):
        self.path = path

    def decode(self):
        with open(self.path, "rb") as music_file:
            while True:
                data = music_file.read(7)
                print(struct.unpack(">7B", data))
