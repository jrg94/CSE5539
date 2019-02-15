import json
import os
import pathlib

from musiviz import m4a_parse


class MusicFile:

    def __init__(self, path: str):
        self.path = path
        self._raw_json = None
        self.genre = None
        self.title = None
        self.artist = None
        self.album = None
        self.track_number = None
        self.total_tracks = None
        self.content_rating = None
        self.sample_rate = None
        self.length = None
        self.owner = None
        self.purchase_date = None
        self._chunk_offset_table = None
        self._sample_to_chunk_table = None
        self._sample_size_table = None
        self._time_to_sample_table = None

    def __str__(self):
        output = (
                    "Title: %s\n"
                    "Artist: %s\n"
                    "Album: %s\n"
                    "Genre: %s\n"
                    "Track Number: %s / %s\n"
                    "Sample Rate: %s Hz\n"
                    "Length: %s\n"
                    "Content Rating: %s\n"
                    "Owner: %s\n"
                    "Purchase Date: %s"
                  )
        formatting = (
            self.title,
            self.artist,
            self.album,
            self.genre,
            self.track_number,
            self.total_tracks,
            self.sample_rate,
            self.length,
            self.content_rating,
            self.owner,
            self.purchase_date
        )
        return output % formatting

    def load(self):
        """
        Loads a music file into a dictionary, populates the various
        MusicFile fields, and outputs the results to a json file.

        :return: None
        """
        self._raw_json = m4a_parse.decode(self.path)
        self._populate_fields()
        self._output_parse()
        print("*********")
        print(self)

    def _output_parse(self):
        """
        A helper method which dumps the raw json to a file.

        :return: None
        """
        data_dir = "data\\" + "\\".join(self.path.split("\\")[-3:-1])
        json_name = self.path.split("\\")[-1].replace(".m4a", ".json")
        pathlib.Path(data_dir).mkdir(parents=True, exist_ok=True)
        with open(os.path.join(data_dir, json_name), "w") as f:
            print(json.dumps(self._raw_json, indent=2, sort_keys=True, ensure_ascii=False), file=f)

    def _populate_fields(self):
        """
        A helper method which maps raw json data to various song fields.

        :return: None
        """
        self._extract_meta_data()
        self._extract_technical_data()
        self._extract_sample_tables()

    def _extract_sample_tables(self):
        sample_tables = self._raw_json["data"]["moov"]["children"]["trak"]["children"]["mdia"]["children"]["minf"]["children"]["stbl"]["children"]
        self._chunk_offset_table = sample_tables["stco"]["entries"]
        self._sample_to_chunk_table = sample_tables["stsc"]["entries"]
        self._sample_size_table = sample_tables["stsz"]["entries"]
        self._time_to_sample_table = sample_tables["stts"]["entries"]
        print(self._time_to_sample_table)

    def _extract_technical_data(self):
        """
        Extracts technical data from the movie header.

        :return: None
        """
        movie_header = self._raw_json["data"]["moov"]["children"]["mvhd"]
        self.sample_rate = movie_header["time_scale"]
        duration = movie_header["duration"]
        self.length = MusicFile._calculate_duration(duration, self.sample_rate)

    @staticmethod
    def _calculate_duration(duration: int, sample_rate: int) -> str:
        """
        A helper function which outputs a HH:MM:SS string given
        some duration in time scale units and sample rate in Hz.

        :param duration: length of song in time scale units
        :param sample_rate: sample rate of song in Hz
        :return: the length of the song as a string
        """
        length_in_seconds = duration / sample_rate
        m, s = divmod(length_in_seconds, 60)
        h, m = divmod(m, 60)
        return "%02d:%02d:%02d" % (h, m, s)

    def _extract_meta_data(self):
        """
        Extracts meta data from the json data.

        :return: None
        """
        entries = self._raw_json["data"]["moov"]["children"]["udta"]["children"]["meta"]["children"]["ilst"]["entries"]
        self.genre = MusicFile._get_meta_value(entries, "gnre", "tag")
        self.title = MusicFile._get_meta_value(entries, "©nam")
        self.artist = MusicFile._get_meta_value(entries, "©ART")
        self.album = MusicFile._get_meta_value(entries, "©alb")
        self.owner = MusicFile._get_meta_value(entries, "ownr")
        self.content_rating = MusicFile._get_meta_value(entries, "rtng", "tag")
        self.purchase_date = MusicFile._get_meta_value(entries, "purd")
        track_number_data = MusicFile._get_meta_value(entries, "trkn")
        self.track_number = track_number_data[3]
        self.total_tracks = track_number_data[5]

    @staticmethod
    def _get_meta_value(entries: list, meta: str, key: str = "data"):
        """
        A helper function for retrieving the first instance of some meta key from a list.

        :param entries: a list of meta entries
        :param meta: a meta key such as genre or apID
        :param key: the key for retrieve data
        :return: the meta value
        """
        try:
            meta_data = next((entry for entry in entries if entry["meta_code"] == meta))
            return meta_data[key]
        except StopIteration:
            return None
