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
                data_type = MusicFile.get_type(music_file)
                print(str(data_type))
                payload = music_file.read(size - 8)
                size = MusicFile.get_size(music_file)
                #print(struct.unpack(">" + str(size) + "s", payload))

    @staticmethod
    def get_size(music_file) -> int:
        size_raw = music_file.read(4)
        size_decoded = struct.unpack(">i", size_raw)[0]
        return size_decoded

    @staticmethod
    def get_type(music_file) -> str:
        data_type = music_file.read(4)
        return data_type.decode("utf-8")
