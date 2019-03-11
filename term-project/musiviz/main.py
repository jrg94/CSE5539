from musiviz.music_file import MusicFile
import os

SAMPLE_PATH = "E:\\Plex\\Music\\Glenn Miller Orchestra"

if __name__ == '__main__':
    curr = None
    for path, dirs, files in os.walk(SAMPLE_PATH):
        for file in files:
            if file.split(".")[-1] == "m4a":
                curr = MusicFile(os.path.join(path, file))
                curr.load()
                print("**********")
                print(curr.as_json_text())
