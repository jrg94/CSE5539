import struct

MAX = 4


class MusicFile:
    def __init__(self, path: str):
        self.path = path

    def decode(self):
        with open(self.path, "rb") as music_file:
            i = 0
            while i < MAX:
                size_raw = music_file.read(4)
                size_decoded = struct.unpack(">i", size_raw)[0] - 4
                print(size_decoded)
                payload = music_file.read(size_decoded)
                print(struct.unpack(">" + str(size_decoded) + "B", payload))
                i += 1
