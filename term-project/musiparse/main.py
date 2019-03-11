import os

from musiparse.music_file_set import MusicFileSet
from musiparse import m4a_parse

OUT_PATH = "..\\data\\%s_%d.json"
SAMPLE_PATH = "E:\\Plex\\Music"
GENRE_TIERS = [5, 25, 100]
MASTER_TIERS = [100, 500, 1000, 5000]


def master_json_dump(limit: int):
    """
    Dumps JSON of all songs meeting some genre up to some limit.

    :param limit: the maximum number of songs to store
    :return: None
    """
    print("*** %d songs ***" % limit)
    path = OUT_PATH % ("master", limit)
    if not os.path.exists(path):
        music_set = MusicFileSet()
        music_set.add_all(SAMPLE_PATH, limit=limit)
        music_set.to_json(path)
        generate_genre_samples(music_set)


def generate_genre_samples(music_set: MusicFileSet):
    """
    From a music file set, we dump all the associated subset to files.

    :param music_set: a set of music files data
    :return: None
    """
    for genre in m4a_parse.GENRES:
        genre_set = music_set.filter_by_genre(genre)
        for tier in GENRE_TIERS:
            sub_genre_set = genre_set.truncate(tier)
            path = OUT_PATH % (genre.lower(), tier)
            if len(sub_genre_set.collection) == tier:
                sub_genre_set.to_json(path)


def dump_all_data():
    """
    A convenience function for dumping json data of music.

    :return: None
    """
    for tier in MASTER_TIERS:
        master_json_dump(tier)


def main():
    dump_all_data()


if __name__ == '__main__':
    main()
