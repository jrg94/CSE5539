import struct
import os
import io

WORD_SIZE = 4


class MusicFile:
    def __init__(self, path: str):
        self.path = path

    def decode(self):
        with open(self.path, "rb") as music_file:
            os_file_size = os.path.getsize(self.path)
            print("File Chunks")
            file_chunks = MusicFile.read_chunks(music_file, os_file_size)
            print("MOOV Chunks")
            moov_chunk = next(x for x in file_chunks if x[1] == "moov")
            moov_chunks = MusicFile.read_sub_chunks(moov_chunk)
            print("TRAK Chunks")
            trak_chunk = next(x for x in moov_chunks if x[1] == "trak")
            MusicFile.read_sub_chunks(trak_chunk)

    @staticmethod
    def read_sub_chunks(chunk: tuple):
        byte_stream = io.BytesIO(chunk[2])
        chunks = MusicFile.read_chunks(byte_stream, chunk[0])
        return chunks

    @staticmethod
    def read_chunks(stream, stream_size):
        read_stream_size = 0
        stream_chunks = list()
        while read_stream_size + 8 < stream_size:
            chunk = MusicFile.read_chunk(stream)
            print(chunk[:-1])
            stream_chunks.append(chunk)
            read_stream_size += chunk[0]
        return stream_chunks

    @staticmethod
    def read_chunk(music_file) -> tuple:
        """
        Reads a chunk from an M4A file.

        :param music_file: an open music file
        :return: a tuple defining this chunk
        """
        size = MusicFile._get_size(music_file)
        data_type = MusicFile._get_type(music_file)
        payload = MusicFile._get_payload(music_file, size - 8)
        return size, data_type, payload

    @staticmethod
    def _get_size(music_file) -> int:
        """
        Grabs the size of the current chunk from a file.

        :param music_file: an open music file
        :return: the size of the current chunk in bytes
        """
        size_raw = music_file.read(WORD_SIZE)
        size_decoded = struct.unpack(">i", size_raw)[0]
        return size_decoded

    @staticmethod
    def _get_type(music_file) -> str:
        """
        Grabs the type of payload from a file.

        :param music_file: an open music file
        :return: the type as a string
        """
        data_type = music_file.read(4)
        return data_type.decode("utf-8")

    @staticmethod
    def _get_payload(music_file, payload_size: int) -> bytes:
        """
        Grabs and returns the next payload_size bytes from a file.

        :param music_file: an open music file
        :param payload_size: the size to be read in bytes
        :return: the payload as a set of bytes
        """
        payload = music_file.read(payload_size)
        return payload
