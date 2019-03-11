from musiparse.music_file_set import MusicFileSet
import os

SAMPLE_PATH = "E:\\Plex\\Music"


def master_json_dump(limit: int, genre=None):
    """
    Dumps JSON of all songs meeting some genre up to some limit.

    :param limit: the maximum number of songs to store
    :param genre: the genre of songs to store
    :return: None
    """
    print("Begin: %d %s songs" % (limit, genre))
    music_set = MusicFileSet()
    if genre:
        path = "..\\data\\%s_%d.json" % (genre.lower(), limit)
    else:
        path = "..\\data\\master_%d.json" % limit
    if not os.path.exists(path):
        music_set.add_all(SAMPLE_PATH, limit=limit, genre=genre)
        music_set.to_json(path)


def dump_all_data():
    master_json_dump(5, "Jazz")
    master_json_dump(25, "Jazz")
    #master_json_dump(100, "Jazz")
    master_json_dump(5, "Rock")
    master_json_dump(25, "Rock")
    #master_json_dump(100, "Rock")
    master_json_dump(5, "Alternative")
    master_json_dump(25, "Alternative")
    #master_json_dump(100, "Alternative")
    master_json_dump(100)
    master_json_dump(500)
    master_json_dump(1000)


def main():
    dump_all_data()


if __name__ == '__main__':
    main()
