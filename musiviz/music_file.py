import struct

MAX = 4


class MusicFile:
    def __init__(self, path: str):
        self.path = path

    def decode(self):
        with open(self.path, "rb") as music_file:
            while music_file.readable():
                print(MusicFile.read_chunk(music_file)[:-1])

    @staticmethod
    def read_chunk(music_file) -> tuple:
        size = MusicFile.get_size(music_file)
        data_type = MusicFile.get_type(music_file)
        payload = MusicFile.get_payload(music_file, size - 8)
        return size, data_type, payload

    @staticmethod
    def get_size(music_file) -> int:
        size_raw = music_file.read(4)
        size_decoded = struct.unpack(">i", size_raw)[0]
        return size_decoded

    @staticmethod
    def get_type(music_file) -> str:
        data_type = music_file.read(4)
        return data_type.decode("utf-8")

    @staticmethod
    def get_payload(music_file, payload_size: int):
        payload = music_file.read(payload_size)
        return payload
