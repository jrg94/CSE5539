import struct
import os

WORD_SIZE = 4


class MusicFile:
    def __init__(self, path: str):
        self.path = path
        self.read_file_size = 0

    def decode(self):
        with open(self.path, "rb") as music_file:
            os_file_size = os.path.getsize(self.path)
            while self.read_file_size < os_file_size:
                print(self.read_chunk(music_file)[:-1])

    def read_chunk(self, music_file) -> tuple:
        size = self.get_size(music_file)
        data_type = self.get_type(music_file)
        payload = self.get_payload(music_file, size - 8)
        return size, data_type, payload

    def get_size(self, music_file) -> int:
        self.read_file_size += WORD_SIZE
        size_raw = music_file.read(WORD_SIZE)
        size_decoded = struct.unpack(">i", size_raw)[0]
        return size_decoded

    def get_type(self, music_file) -> str:
        self.read_file_size += WORD_SIZE
        data_type = music_file.read(4)
        return data_type.decode("utf-8")

    def get_payload(self, music_file, payload_size: int):
        self.read_file_size += payload_size
        payload = music_file.read(payload_size)
        return payload
