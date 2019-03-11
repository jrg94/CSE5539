from musiviz.music_file_set import MusicFileSet
import os

SAMPLE_PATH = "E:\\Plex\\Music\\Glenn Miller Orchestra"


def main():
    music_set = MusicFileSet()
    for path, dirs, files in os.walk(SAMPLE_PATH):
        for file in files:
            if file.split(".")[-1] == "m4a":
                music_set.add(os.path.join(path, file))
    music_set.to_json("example.json")


if __name__ == '__main__':
    main()
