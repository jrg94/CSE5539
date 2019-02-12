import struct
import os
import io
import json

HEADER_SIZE = 8

ATOMS = [
    "moov",
    "trak",
    "mdia",
    "minf",
    "stbl",
    "udta",
]


class MusicFile:
    def __init__(self, path: str):
        self.path = path

    def decode(self):
        with open(self.path, "rb") as music_file:
            os_file_size = os.path.getsize(self.path)
            file_chunks = MusicFile.read_chunks(music_file, os_file_size)
            file_dict = self.create_root_dict(file_chunks)
            MusicFile.traverse_atoms(file_chunks, file_dict["data"])
            with open("mapping.json", "w") as f:
                print(json.dumps(file_dict, indent=2, sort_keys=True), file=f)

    def create_root_dict(self, file_chunks) -> dict:
        root_dict = dict()
        root_dict["source"] = self.path
        root_dict["data"] = MusicFile.atom_mapping(file_chunks)
        root_dict["size"] = os.path.getsize(self.path)
        return root_dict

    @staticmethod
    def atom_mapping(atoms: list):
        atom_dict = dict()
        for atom in atoms:
            atom_dict[atom[1]] = {
                "size": atom[0]
            }
        return atom_dict

    @staticmethod
    def traverse_atoms(root_atoms: list, root_mapping: dict):
        """
        A recursive atom exploration function.

        :param root_atoms: a set of atoms
        :param root_mapping: an atom meta data JSON
        :return: None
        """
        for atom in root_atoms:
            if atom[1] in ATOMS:
                chunks = MusicFile.read_sub_chunks(atom)
                chunk_mapping = MusicFile.atom_mapping(chunks)
                root_mapping[atom[1]]["children"] = chunk_mapping
                MusicFile.traverse_atoms(chunks, chunk_mapping)

    @staticmethod
    def read_sub_chunks(chunk: tuple) -> list:
        """
        A special method for parsing a stream that isn't from the
        original file.

        :param chunk: a tuple containing atom data
        :return: a set of sub atoms
        """
        byte_stream = io.BytesIO(chunk[2])
        chunks = MusicFile.read_chunks(byte_stream, chunk[0] - 8)
        return chunks

    @staticmethod
    def read_chunks(stream, stream_size: int) -> list:
        """
        Iterates over a stream extracting atoms.

        :param stream: a stream of bytes
        :param stream_size: the stream size
        :return: a list of atoms
        """
        read_stream_size = 0
        stream_chunks = list()
        while read_stream_size < stream_size:
            chunk = MusicFile.read_chunk(stream)
            stream_chunks.append(chunk)
            read_stream_size += chunk[0]
        return stream_chunks

    @staticmethod
    def read_chunk(music_file: io.BytesIO) -> tuple:
        """
        Reads a chunk from an M4A file.

        :param music_file: an open music file
        :return: a tuple defining this chunk
        """
        size, data_type = MusicFile._read_header(music_file)
        payload = b''
        if size != 0:
            payload = MusicFile._get_payload(music_file, size - 8)
        return size, data_type, payload

    @staticmethod
    def _read_header(music_file: io.BytesIO):
        """
        A helper method built for extracting 8 byte headers.

        :param music_file: a set of bytes
        :return: the size and data type of the header
        """
        header_raw = music_file.read(HEADER_SIZE)
        size = MusicFile._get_size(header_raw[:4])
        data_type = ""
        if size != 0:
            data_type = MusicFile._get_type(header_raw[4:])
        return size, data_type

    @staticmethod
    def _get_size(header_size_raw: bytes) -> int:
        """
        Grabs the size of the current chunk from a file.

        :param header_size_raw: a set of bytes representing size
        :return: the size of the current chunk in bytes
        """
        size_decoded = struct.unpack(">i", header_size_raw)[0]
        return size_decoded

    @staticmethod
    def _get_type(header_type_raw: bytes) -> str:
        """
        Grabs the type of payload from a file.

        :param header_type_raw: a set of bytes representing type
        :return: the type as a string
        """
        return header_type_raw.decode("utf-8")

    @staticmethod
    def _get_payload(music_file: io.BytesIO, payload_size: int) -> bytes:
        """
        Grabs and returns the next payload_size bytes from a file.

        :param music_file: an open music file
        :param payload_size: the size to be read in bytes
        :return: the payload as a set of bytes
        """
        payload = music_file.read(payload_size)
        return payload
