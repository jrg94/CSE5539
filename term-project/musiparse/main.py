from musiparse.music_file_set import MusicFileSet

SAMPLE_PATH = "E:\\Plex\\Music"


def genre_json_dump(limit: int, genre: str):
    music_set = MusicFileSet()
    music_set.add_all(SAMPLE_PATH, limit=limit, genre=genre)
    music_set.to_json("..\\data\\%s_%d.json" % (genre.lower(), limit))


def main():
    genre_json_dump(5, "Jazz")
    genre_json_dump(5, "Rock")
    genre_json_dump(5, "Alternative")


if __name__ == '__main__':
    main()
