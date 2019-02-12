import struct
import io
import os

HEADER_SIZE = 8


def decode(path: str) -> dict:
    with open(path, "rb") as music_file:
        os_file_size = os.path.getsize(path)
        file_chunks = _read_chunks(music_file, os_file_size)
        file_dict = _create_root_dict(path, file_chunks)
        _traverse_atoms(file_chunks, file_dict["data"])
    return file_dict


def _create_root_dict(path, file_chunks) -> dict:
    root_dict = dict()
    root_dict["source"] = path
    root_dict["data"] = _atom_mapping(file_chunks)
    root_dict["size"] = os.path.getsize(path)
    return root_dict


def _atom_mapping(atoms: list):
    atom_dict = dict()
    for atom in atoms:
        atom_dict[atom[1]] = {
            "size": atom[0]
        }
    return atom_dict


def _traverse_atoms(root_atoms: list, root_mapping: dict):
    """
    A recursive atom exploration function.

    :param root_atoms: a set of atoms
    :param root_mapping: an atom meta data JSON
    :return: None
    """
    for atom in root_atoms:
        parse_map = _get_parse_map()
        if atom[1] in parse_map:
            parse_map[atom[1]](atom, root_mapping[atom[1]])


def _mvhd(atom: tuple, atom_mapping: dict):
    stream = io.BytesIO(atom[2])
    atom_mapping["version"] = stream.read(1).decode()
    atom_mapping["flags"] = stream.read(3).decode()
    atom_mapping["creation_time"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["modification_time"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["time_scale"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["duration"] = struct.unpack(">i", stream.read(4))[0]
    #atom_mapping["preferred"]


def _ftyp(atom: tuple, atom_mapping: dict):
    """
    Parse ftyp fields.

    :param atom: the current atom
    :param atom_mapping: the current atom mapping
    :return: None
    """
    data = atom[2]
    atom_mapping["major_brand"] = data[:4].decode()
    atom_mapping["minor_version"] = struct.unpack(">i", data[4:8])[0]
    atom_mapping["compatible_brands"] = list()
    size = atom[0] - 16  # 8 for size and type and 8 for previous two reads
    bytes_read = 0
    while bytes_read < size:
        offset = 8 + bytes_read
        atom_mapping["compatible_brands"].append(data[offset: offset + 4].decode())
        bytes_read += 4


def _atom_parent(atom: tuple, atom_mapping: dict):
    """
    The default parse mode for atoms.

    :param atom: an atom tuple (size, type, data)
    :param root_mapping: the dict mapping at the current depth
    :return: None
    """
    chunks = _read_sub_chunks(atom)
    chunk_mapping = _atom_mapping(chunks)
    atom_mapping["children"] = chunk_mapping
    _traverse_atoms(chunks, chunk_mapping)


def _read_sub_chunks(chunk: tuple) -> list:
    """
    A special method for parsing a stream that isn't from the
    original file.

    :param chunk: a tuple containing atom data
    :return: a set of sub atoms
    """
    byte_stream = io.BytesIO(chunk[2])
    chunks = _read_chunks(byte_stream, chunk[0] - 8)
    return chunks


def _read_chunks(stream, stream_size: int) -> list:
    """
    Iterates over a stream extracting atoms.

    :param stream: a stream of bytes
    :param stream_size: the stream size
    :return: a list of atoms
    """
    read_stream_size = 0
    stream_chunks = list()
    while read_stream_size < stream_size:
        chunk = _read_chunk(stream)
        stream_chunks.append(chunk)
        read_stream_size += chunk[0]
    return stream_chunks


def _read_chunk(music_file: io.BytesIO) -> tuple:
    """
    Reads a chunk from an M4A file.

    :param music_file: an open music file
    :return: a tuple defining this chunk
    """
    size, data_type = _read_header(music_file)
    payload = b''
    if size != 0:
        payload = _get_payload(music_file, size - 8)
    return size, data_type, payload


def _read_header(music_file: io.BytesIO):
    """
    A helper method built for extracting 8 byte headers.

    :param music_file: a set of bytes
    :return: the size and data type of the header
    """
    header_raw = music_file.read(HEADER_SIZE)
    size = _get_size(header_raw[:4])
    data_type = ""
    if size != 0:
        data_type = _get_type(header_raw[4:])
    return size, data_type


def _get_size(header_size_raw: bytes) -> int:
    """
    Grabs the size of the current chunk from a file.

    :param header_size_raw: a set of bytes representing size
    :return: the size of the current chunk in bytes
    """
    size_decoded = struct.unpack(">i", header_size_raw)[0]
    return size_decoded


def _get_type(header_type_raw: bytes) -> str:
    """
    Grabs the type of payload from a file.

    :param header_type_raw: a set of bytes representing type
    :return: the type as a string
    """
    return header_type_raw.decode("utf-8")


def _get_payload(music_file: io.BytesIO, payload_size: int) -> bytes:
    """
    Grabs and returns the next payload_size bytes from a file.

    :param music_file: an open music file
    :param payload_size: the size to be read in bytes
    :return: the payload as a set of bytes
    """
    payload = music_file.read(payload_size)
    return payload


def _get_parse_map() -> dict:
    """
    Gets the parse map which contains all known atoms and a mapping
    to their parse function.

    :return: the parse map
    """
    return {
        "moov": _atom_parent,
        "trak": _atom_parent,
        "mdia": _atom_parent,
        "minf": _atom_parent,
        "stbl": _atom_parent,
        "udta": _atom_parent,
        "ftyp": _ftyp,
        "mvhd": _mvhd
    }
