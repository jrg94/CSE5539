from musiviz.music_file import MusicFile
import os

SAMPLE_PATH = "E:\\Plex\\Music\\Aaron West and The Roaring Twenties\\We Don't Have Each Other\\"

if __name__ == '__main__':
    curr = None
    for path, dirs, files in os.walk(SAMPLE_PATH):
        for file in files:
            curr = MusicFile(os.path.join(path, file))
            curr.load()

    curr.to_wav()
