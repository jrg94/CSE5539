import base64
import io
import os
import struct

HEADER_SIZE = 8

MEDIA_TYPES = [
    "Movie",
    "Music",
    "AudioBook",
    "",
    "",
    "",
    "Music Video",
    "",
    ""
    "Movie",
    "TV Show",
    "Booklet",
    "",
    "",
    "Ringtone"
]

RATINGS = [
    "None",
    "Explicit",
    "Clean"
]

GENRES = [
    "Blues",
    "Classic Rock",
    "Country",
    "Dance",
    "Disco",
    "Funk",
    "Grunge",
    "Hip-Hop",
    "Jazz",
    "Metal",
    "New Age",
    "Oldies",
    "Other",
    "Pop",
    "R & B",
    "Rap",
    "Reggae",
    "Rock",
    "Techno",
    "Industrial",
    "Alternative",
    "Ska",
    "Death Metal",
    "Pranks",
    "Soundtrack",
    "Euro - Techno",
    "Ambient",
    "Trip - Hop",
    "Vocal",
    "Jazz + Funk",
    "Fusion",
    "Trance",
    "Classical",
    "Instrumental",
    "Acid",
    "House",
    "Game",
    "Sound Clip",
    "Gospel",
    "Noise",
    "AlternRock",
    "Bass",
    "Soul",
    "Punk",
    "Space",
    "Meditative",
    "Instrumental Pop",
    "Instrumental Rock",
    "Ethnic",
    "Gothic",
    "Darkwave",
    "Techno - Industrial",
    "Electronic",
    "Pop - Folk",
    "Eurodance",
    "Dream",
    "Southern Rock",
    "Comedy",
    "Cult",
    "Gangsta",
    "Top 40",
    "Christian Rap",
    "Pop / Funk",
    "Jungle",
    "Native American",
    "Cabaret",
    "New Wave",
    "Psychadelic",
    "Rave",
    "Showtunes",
    "Trailer",
    "Lo - Fi",
    "Tribal",
    "Acid Punk",
    "Acid Jazz",
    "Polka",
    "Retro",
    "Musical",
    "Rock & Roll",
    "Hard Rock"
]


def decode(path: str) -> dict:
    """
    The exposed decoding function which decodes a file at some path.

    :param path: the path to a file
    :return: the decoded file as a dictionary
    """
    with open(path, "rb") as music_file:
        os_file_size = os.path.getsize(path)
        file_atoms = _read_atoms(music_file, os_file_size)
        file_dict = _create_root_dict(path, file_atoms)
        _traverse_atoms(file_atoms, file_dict["data"])
    return file_dict


def _create_root_dict(path, file_atoms) -> dict:
    """
    Creates the root dictionary.

    :param path: the path to the files
    :param file_atoms: the list of top-level atoms.
    :return: a dictionary
    """
    root_dict = dict()
    root_dict["source"] = path
    root_dict["data"] = _atom_mapping(file_atoms)
    root_dict["size"] = os.path.getsize(path)
    return root_dict


def _atom_mapping(atoms: list) -> dict:
    """
    Maps atoms to a dictionary.

    :param atoms: a list of atoms
    :return: a dictionary mapping
    """
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


def _frma(atom: tuple, atom_mapping: dict):
    atom_mapping["data_format"] = atom[2].decode()


def _mdat(atom: tuple, atom_mapping: dict):
    """
    Extracts mdat data and encodes it using base64.

    :param atom: an mdat atom
    :param atom_mapping: an mdat atom mapping
    :return: None
    """
    atom_mapping["data"] = base64.encodebytes(atom[2]).decode("ascii")


def _stik(atom: tuple, atom_mapping: dict):
    """
    Parses a media type (stik) atom.

    :param atom: a stik atom
    :param atom_mapping: a stik atom mapping
    :return: None
    """
    stream = io.BytesIO(atom[2])
    atom_mapping["description"] = "Media Type"
    atom_mapping["data"] = struct.unpack(">B", stream.read())[0]
    atom_mapping["tag"] = MEDIA_TYPES[atom_mapping["data"]]


def _rtng(atom: tuple, atom_mapping: dict):
    """
    Parses a rating (rtng) atom.

    :param atom: an rtng atom
    :param atom_mapping: an rtng atom mapping
    :return: None
    """
    stream = io.BytesIO(atom[2])
    atom_mapping["description"] = "Explicit/Clean Label"
    atom_mapping["data"] = struct.unpack(">B", stream.read())[0]
    atom_mapping["tag"] = RATINGS[atom_mapping["data"]]


def _gnre(atom: tuple, atom_mapping: dict):
    """
    Parses a genre (gnre) atom.

    :param atom: a grne atom
    :param atom_mapping: a grne atom mapping
    :return: None
    """
    stream = io.BytesIO(atom[2])
    atom_mapping["description"] = "Genre"
    atom_mapping["data"] = struct.unpack(">H", stream.read())[0]
    atom_mapping["tag"] = GENRES[atom_mapping["data"] - 1]


def _cpil(atom: tuple, atom_mapping: dict):
    """
    Parses a compilation (cpil) atom.

    :param atom: a cpil atom
    :param atom_mapping: a cpil atom mapping
    :return:
    """
    stream = io.BytesIO(atom[2])
    atom_mapping["description"] = "Compilation"
    atom_mapping["data"] = struct.unpack(">?", stream.read())[0]


def _meta_item_data(atom: tuple, atom_mapping: dict):
    """
    Parses a meta item data atom.

    :param atom: a meta item data atom
    :param atom_mapping: a meta item data atom mapping
    :return: None
    """
    stream = io.BytesIO(atom[2])
    atom_mapping["version"] = stream.read(1).decode()
    atom_mapping["flags"] = struct.unpack(">BBB", stream.read(3))[-1]
    atom_mapping["reserved"] = stream.read(4).decode()
    parse_map = _get_parse_map()
    remaining_size = atom[0] - 16
    if atom_mapping["flags"] == 1:  # text
        atom_mapping["data"] = stream.read().decode()
    elif atom_mapping["meta_code"] in parse_map:
        sub_atom = (remaining_size, atom_mapping["meta_code"], stream.read())
        parse_map[atom_mapping["meta_code"]](sub_atom, atom_mapping)
    else:
        atom_mapping["data"] = struct.unpack(">" + str(remaining_size) + "B", stream.read())


def _meta_item(atom: tuple, entries: list):
    """
    Parse a meta item atom.

    :param atom: a meta item atom
    :param entries: a meta item atom mapping
    :return: None
    """
    stream = io.BytesIO(atom[2])
    meta_data = dict()
    meta_data["meta_code"] = atom[1]
    meta_data["size"] = atom[0]
    data_atoms = _read_atoms(stream, atom[0] - 8)
    for data_atom in data_atoms:
        if meta_data["meta_code"] != "----":
            _meta_item_data(data_atom, meta_data)
    entries.append(meta_data)


def _ilst(atom: tuple, atom_mapping: dict):
    """
    Parses a meta data item list (ilst) atom.

    :param atom: an ilst atom
    :param atom_mapping: an ilst atom mapping
    :return: None
    """
    stream = io.BytesIO(atom[2])
    sub_atoms = _read_atoms(stream, atom[0] - 8)
    atom_mapping["entries"] = list()
    for sub_atom in sub_atoms:
        _meta_item(sub_atom, atom_mapping["entries"])


def _meta_hdlr(atom: tuple, atom_mapping: dict):
    """
    Parses a meta handler (hdlr) atom. Apparently, these
    are different from the regular hdlr atoms.

    :param atom: a hdlr atom
    :param atom_mapping: a hdlr atom mapping
    :return: None
    """
    stream = io.BytesIO(atom[2])
    atom_mapping["version"] = stream.read(1).decode()
    atom_mapping["flags"] = stream.read(3).decode()
    atom_mapping["predefined"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["handler_type"] = stream.read(4).decode()
    atom_mapping["manufacturer"] = stream.read(4).decode()
    atom_mapping["reserved_2"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["reserved_3"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["component_type"] = stream.read(1).decode()
    atom_mapping["component_name"] = stream.read(1).decode()


def _meta(atom: tuple, atom_mapping: dict):
    """
    Parses the meta atom

    :param atom: a meta atom
    :param atom_mapping: a meta atom mapping
    :return: None
    """
    stream = io.BytesIO(atom[2])
    size = struct.unpack(">Q", stream.read(8))[0]
    data_type = stream.read(4).decode()
    data = stream.read(size - 8)
    hdlr_atom = (size, data_type, data)
    remaining_size = atom[0] - size - 12
    sub_atoms = _read_atoms(stream, remaining_size)
    sub_atoms.append(hdlr_atom)
    children = _atom_mapping(sub_atoms)
    atom_mapping["children"] = children
    sub_atoms.remove(hdlr_atom)
    _traverse_atoms(sub_atoms, children)
    _meta_hdlr(hdlr_atom, children["hdlr"])


def _tkhd(atom: tuple, atom_mapping: dict):
    """
    Parses a track header (tkhd) atom.

    :param atom: a tkhd atom
    :param atom_mapping: a tkhd atom mapping
    :return: None
    """
    stream = io.BytesIO(atom[2])
    atom_mapping["version"] = stream.read(1).decode()
    atom_mapping["flags"] = stream.read(3).decode()
    atom_mapping["creation_time"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["modification_time"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["track_id"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["reserved_1"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["duration"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["reserved_2"] = struct.unpack(">q", stream.read(8))[0]
    atom_mapping["layer"] = struct.unpack(">H", stream.read(2))[0]
    atom_mapping["alternate_group"] = struct.unpack(">H", stream.read(2))[0]
    volume = struct.unpack(">bb", stream.read(2))
    atom_mapping["volume"] = str(volume[0]) + "." + str(volume[1])
    atom_mapping["reserved_3"] = struct.unpack(">H", stream.read(2))[0]
    atom_mapping["matrix_structure"] = stream.read(36).decode()
    atom_mapping["track_width"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["track_height"] = struct.unpack(">i", stream.read(4))[0]


def _stts(atom: tuple, atom_mapping: dict):
    stream = io.BytesIO(atom[2])
    atom_mapping["version"] = stream.read(1).decode()
    atom_mapping["flags"] = stream.read(3).decode()
    atom_mapping["number_of_entries"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["entries"] = list()
    i = 0
    while i < atom_mapping["number_of_entries"]:
        time_to_sample_row = dict()
        time_to_sample_row["sample_count"] = struct.unpack(">i", stream.read(4))[0]
        time_to_sample_row["sample_duration"] = struct.unpack(">i", stream.read(4))[0]
        atom_mapping["entries"].append(time_to_sample_row)
        i += 1


def _stsz(atom: tuple, atom_mapping: dict):
    """
    Parses a sample size (stsz) atom.

    :param atom: an stsz atom
    :param atom_mapping: an stsz atom mapping
    :return: None
    """
    stream = io.BytesIO(atom[2])
    atom_mapping["version"] = stream.read(1).decode()
    atom_mapping["flags"] = stream.read(3).decode()
    atom_mapping["sample_size"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["number_of_entries"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["entries"] = list()
    i = 0
    while i < atom_mapping["number_of_entries"]:
        atom_mapping["entries"].append(struct.unpack(">i", stream.read(4))[0])
        i += 1


def _esds(atom: tuple, atom_mapping: dict):
    """
    Parses an elementary stream descriptor (esds) atom.

    :param atom: an esds atom
    :param atom_mapping: an esds atom mapping
    :return: None
    """
    stream = io.BytesIO(atom[2])
    atom_mapping["version"] = stream.read(1).decode()
    atom_mapping["flags"] = stream.read(3).decode()
    # TODO: atom_mapping["elementary_stream_descriptor"] = stream.read().decode()
    # https://raw.githubusercontent.com/OpenAnsible/rust-mp4/master/docs/ISO_IEC_14496-14_2003-11-15.pdf


def _stsd(atom: tuple, atom_mapping: dict):
    """
    Parses a standard description (stds) atom.

    :param atom: an stds atom
    :param atom_mapping: an stds atom mapping
    :return: None
    """
    stream = io.BytesIO(atom[2])
    atom_mapping["version"] = stream.read(1).decode()
    atom_mapping["flags"] = stream.read(3).decode()
    atom_mapping["number_of_entries"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["entries"] = list()
    i = 0
    while i < atom_mapping["number_of_entries"]:
        sample_description = dict()
        sample_description["size"] = struct.unpack(">i", stream.read(4))[0]
        sample_description["data_format"] = stream.read(4).decode()
        sample_description["reserved"] = stream.read(6).decode()
        sample_description["data_reference_index"] = struct.unpack(">H", stream.read(2))[0]
        sample_description["version"] = struct.unpack(">H", stream.read(2))[0]
        if sample_description["version"] == 0:
            _stsd_version_one(stream, sample_description)
            sub_atoms = _read_atoms(stream, sample_description["size"] - 36)
            sample_description["children"] = _atom_mapping(sub_atoms)
            _traverse_atoms(sub_atoms, sample_description["children"])
        atom_mapping["entries"].append(sample_description)
        i += 1


def _stsd_version_one(stream: io.BytesIO, sample_description: dict):
    """
    Parses the sound description based on version one format.

    :param stream:
    :param sample_description:
    :return:
    """
    sample_description["revision_level"] = struct.unpack(">h", stream.read(2))[0]
    sample_description["vendor"] = struct.unpack(">i", stream.read(4))[0]
    sample_description["number_of_channels"] = struct.unpack(">h", stream.read(2))[0]
    sample_description["sample_size"] = struct.unpack(">h", stream.read(2))[0]
    sample_description["compression_id"] = struct.unpack(">h", stream.read(2))[0]
    sample_description["packet_size"] = struct.unpack(">h", stream.read(2))[0]
    sample_description["sample_rate"] = struct.unpack(">HH", stream.read(4))[0]


def _stsc(atom: tuple, atom_mapping: dict):
    """
    Parse sample-to-chunk (stsc) atoms.

    :param atom: an stsc atom
    :param atom_mapping: an stsc atom mapping
    :return: None
    """
    stream = io.BytesIO(atom[2])
    atom_mapping["version"] = stream.read(1).decode()
    atom_mapping["flags"] = stream.read(3).decode()
    atom_mapping["number_of_entries"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["entries"] = list()
    i = 0
    while i < atom_mapping["number_of_entries"]:
        sample_to_chunk = dict()
        sample_to_chunk["first_chunk"] = struct.unpack(">i", stream.read(4))[0]
        sample_to_chunk["samples_per_chunk"] = struct.unpack(">i", stream.read(4))[0]
        sample_to_chunk["sample_description_id"] = struct.unpack(">i", stream.read(4))[0]
        atom_mapping["entries"].append(sample_to_chunk)
        i += 1


def _stco(atom: tuple, atom_mapping: dict):
    """
    Parses chunk offset (stco) atoms.

    :param atom: an stco atom
    :param atom_mapping: an stco atom mapping
    :return: None
    """
    stream = io.BytesIO(atom[2])
    atom_mapping["version"] = stream.read(1).decode()
    atom_mapping["flags"] = stream.read(3).decode()
    atom_mapping["number_of_entries"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["entries"] = list()
    i = 0
    while i < atom_mapping["number_of_entries"]:
        atom_mapping["entries"].append(struct.unpack(">i", stream.read(4))[0])
        i += 1


def _smhd(atom: tuple, atom_mapping: dict):
    """
    Parse sound media information header (smhd) atoms.

    :param atom: an smhd atom
    :param atom_mapping: an smhd atom mapping
    :return: None
    """
    stream = io.BytesIO(atom[2])
    atom_mapping["version"] = stream.read(1).decode()
    atom_mapping["flags"] = stream.read(3).decode()
    atom_mapping["balance"] = struct.unpack(">H", stream.read(2))[0]
    atom_mapping["reserved"] = struct.unpack(">H", stream.read(2))[0]


def _dref(atom: tuple, atom_mapping: dict):
    """
    Parses data reference (dref) atoms.

    :param atom: a dref atom
    :param atom_mapping: a dref atom mapping
    :return: None
    """
    stream = io.BytesIO(atom[2])
    atom_mapping["version"] = stream.read(1).decode()
    atom_mapping["flags"] = stream.read(3).decode()
    atom_mapping["number_of_entries"] = struct.unpack(">i", stream.read(4))[0]
    sub_atoms = _read_atoms(stream, atom[0] - 16)
    atom_mapping["entries"] = list()
    for atom in sub_atoms:
        stream = io.BytesIO(atom[2])
        entry_mapping = dict()
        entry_mapping[atom[1]] = dict()
        sub_atom_mapping = entry_mapping[atom[1]]
        sub_atom_mapping["size"] = atom[0]
        sub_atom_mapping["version"] = stream.read(1).decode()
        sub_atom_mapping["flags"] = stream.read(3).decode()
        sub_atom_mapping["data"] = stream.read().decode()
        atom_mapping["entries"].append(entry_mapping)


def _mdhd(atom: tuple, atom_mapping: dict):
    """
    Parses the media header (mdhd) fields.

    :param atom: the mdhd atom
    :param atom_mapping: the mdhd atom mapping
    :return: None
    """
    stream = io.BytesIO(atom[2])
    atom_mapping["version"] = stream.read(1).decode()
    atom_mapping["flags"] = stream.read(3).decode()  # Should be 0
    atom_mapping["creation_time"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["modification_time"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["time_scale"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["duration"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["language"] = struct.unpack(">H", stream.read(2))[0]
    atom_mapping["quality"] = struct.unpack(">H", stream.read(2))[0]


def _hdlr(atom: tuple, atom_mapping: dict):
    """
    Parses the handler (hdlr) fields.

    :param atom: the hdlr atom
    :param atom_mapping: the hdlr atom mapping
    :return: None
    """
    stream = io.BytesIO(atom[2])
    atom_mapping["version"] = stream.read(1).decode()
    atom_mapping["flags"] = stream.read(3).decode()  # Should be 0
    atom_mapping["component_type"] = stream.read(4).decode()
    atom_mapping["component_subtype"] = stream.read(4).decode()
    atom_mapping["component_manufacturer"] = struct.unpack(">i", stream.read(4))[0]  # Should be 0
    atom_mapping["component_flags"] = struct.unpack(">i", stream.read(4))[0]  # Should be 0
    atom_mapping["component_flags_mask"] = struct.unpack(">i", stream.read(4))[0]  # Should be 0
    atom_mapping["component_name"] = stream.read().decode()  # Reads what's left


def _mvhd(atom: tuple, atom_mapping: dict):
    """
    Parse the movie header (mvhd) fields.

    :param atom: the mvhd atom
    :param atom_mapping: the mvhd atom mapping
    :return: None
    """
    stream = io.BytesIO(atom[2])
    atom_mapping["version"] = stream.read(1).decode()
    atom_mapping["flags"] = stream.read(3).decode()
    atom_mapping["creation_time"] = struct.unpack(">I", stream.read(4))[0]
    atom_mapping["modification_time"] = struct.unpack(">I", stream.read(4))[0]
    atom_mapping["time_scale"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["duration"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["preferred_rate"] = struct.unpack(">HH", stream.read(4))
    atom_mapping["preferred_volume"] = struct.unpack(">BB", stream.read(2))
    atom_mapping["reserved"] = stream.read(10).decode()
    atom_mapping["matrix_structure"] = stream.read(36).decode()
    atom_mapping["preview_time"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["preview_duration"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["poster_time"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["selection_time"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["selection_duration"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["current_time"] = struct.unpack(">i", stream.read(4))[0]
    atom_mapping["next_track_id"] = struct.unpack(">I", stream.read(4))[0]


def _ftyp(atom: tuple, atom_mapping: dict):
    """
    Parses the file type (ftyp) fields.

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
    :param atom_mapping: the dict mapping at the current depth
    :return: None
    """
    sub_atoms = _read_sub_atoms(atom)
    sub_atom_mapping = _atom_mapping(sub_atoms)
    atom_mapping["children"] = sub_atom_mapping
    _traverse_atoms(sub_atoms, sub_atom_mapping)


def _read_sub_atoms(atom: tuple) -> list:
    """
    A special method for parsing a stream that isn't from the
    original file.

    :param atom: a tuple containing atom data
    :return: a set of sub atoms
    """
    byte_stream = io.BytesIO(atom[2])
    atoms = _read_atoms(byte_stream, atom[0] - 8)
    return atoms


def _read_atoms(stream, stream_size: int) -> list:
    """
    Iterates over a stream extracting atoms.

    :param stream: a stream of bytes
    :param stream_size: the stream size
    :return: a list of atoms
    """
    read_stream_size = 0
    stream_atoms = list()
    while read_stream_size < stream_size:
        atom = _read_atom(stream)
        stream_atoms.append(atom)
        read_stream_size += atom[0]
    return stream_atoms


def _read_atom(music_file: io.BytesIO) -> tuple:
    """
    Reads an atom from an M4A file.

    :param music_file: an open music file
    :return: a tuple defining this atom
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
    Grabs the size of the current atom from a file.

    :param header_size_raw: a set of bytes representing size
    :return: the size of the current atom in bytes
    """
    size_decoded = struct.unpack(">I", header_size_raw)[0]
    return size_decoded


def _get_type(header_type_raw: bytes) -> str:
    """
    Grabs the type of payload from a file.

    :param header_type_raw: a set of bytes representing type
    :return: the type as a string
    """
    return header_type_raw.decode("latin-1")


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
        "dinf": _atom_parent,
        "pinf": _atom_parent,
        "schi": _atom_parent,
        "ftyp": _ftyp,
        "mvhd": _mvhd,
        "hdlr": _hdlr,
        "mdhd": _mdhd,
        "dref": _dref,
        "smhd": _smhd,
        "stco": _stco,
        "stsc": _stsc,
        "stsd": _stsd,
        "esds": _esds,
        "stsz": _stsz,
        "stts": _stts,
        "tkhd": _tkhd,
        "meta": _meta,
        "ilst": _ilst,
        "cpil": _cpil,
        "gnre": _gnre,
        "rtng": _rtng,
        "stik": _stik,
        "mdat": _mdat,
        "frma": _frma
    }
