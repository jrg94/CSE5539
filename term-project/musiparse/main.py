from musiparse.music_file_set import MusicFileSet
import os

SAMPLE_PATH = "E:\\Plex\\Music"


def main():
    music_set = MusicFileSet()
    for path, dirs, files in os.walk(SAMPLE_PATH):
        for file in files:
            if file.split(".")[-1] == "m4a":
                print("Processing '%s'" % file)
                try:
                    music_set.add(os.path.join(path, file))
                except:
                    print("- Failed to process '%s'" % file)
    music_set.to_json("..\\data\\master.json")


if __name__ == '__main__':
    main()
