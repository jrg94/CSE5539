import struct
import os

WORD_SIZE = 4


class MusicFile:
    def __init__(self, path: str):
        self.path = path
        self.read_file_size = 0

    def decode(self):
        with open(self.path, "rb") as music_file:
            file_chunks = list()
            os_file_size = os.path.getsize(self.path)
            while self.read_file_size < os_file_size:
                chunk = self.read_chunk(music_file)
                print(chunk[:-1])
                file_chunks.append(chunk)

    def read_chunk(self, music_file) -> tuple:
        """
        Reads a chunk from an M4A file.

        :param music_file: an open music file
        :return: a tuple defining this chunk
        """
        size = self._get_size(music_file)
        data_type = self._get_type(music_file)
        payload = self._get_payload(music_file, size - 8)
        return size, data_type, payload

    def _get_size(self, music_file) -> int:
        """
        Grabs the size of the current chunk from a file.

        :param music_file: an open music file
        :return: the size of the current chunk in bytes
        """
        self.read_file_size += WORD_SIZE
        size_raw = music_file.read(WORD_SIZE)
        size_decoded = struct.unpack(">i", size_raw)[0]
        return size_decoded

    def _get_type(self, music_file) -> str:
        """
        Grabs the type of payload from a file.

        :param music_file: an open music file
        :return: the type as a string
        """
        self.read_file_size += WORD_SIZE
        data_type = music_file.read(4)
        return data_type.decode("utf-8")

    def _get_payload(self, music_file, payload_size: int) -> bytes:
        """
        Grabs and returns the next payload_size bytes from a file.

        :param music_file: an open music file
        :param payload_size: the size to be read in bytes
        :return: the payload as a set of bytes
        """
        self.read_file_size += payload_size
        payload = music_file.read(payload_size)
        return payload
