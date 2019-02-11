import struct

MAX = 4


class MusicFile:
    def __init__(self, path: str):
        self.path = path

    def decode(self):
        with open(self.path, "rb") as music_file:
            size = MusicFile.get_size(music_file)
            while size != 0:
                print(size)
                payload = music_file.read(size)
                print(struct.unpack(">" + str(size) + "B", payload))
                size = MusicFile.get_size(music_file)

    @staticmethod
    def get_size(music_file):
        size_raw = music_file.read(4)
        size_decoded = struct.unpack(">i", size_raw)[0] - 4
        return size_decoded
