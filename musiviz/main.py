from musiviz.music_file import MusicFile
import os

SAMPLE_PATH = "E:\\Plex\\Music\\Glenn Miller Orchestra"

if __name__ == '__main__':
    curr = None
    for path, dirs, files in os.walk(SAMPLE_PATH):
        for file in files:
            curr = MusicFile(os.path.join(path, file))
            curr.to_wav()
            #curr.load()
            #curr.persist()
