import os

from musiparse.music_file_set import MusicFileSet

SAMPLE_PATH = "E:\\Plex\\Music"


def main():
    music_set = MusicFileSet()
    music_set.add_all(SAMPLE_PATH)
    music_set.to_json("..\\data\\master.json")


if __name__ == '__main__':
    main()
