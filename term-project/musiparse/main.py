from musiparse.music_file_set import MusicFileSet

SAMPLE_PATH = "E:\\Plex\\Music"


def main():
    music_set = MusicFileSet()
    music_set.add_all(SAMPLE_PATH, limit=5, genre="Jazz")
    music_set.to_json("..\\data\\jazz_5.json")


if __name__ == '__main__':
    main()
