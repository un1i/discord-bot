import typing as tp



class Track:
    def __init__(self, name: str, url = None, audio_link = None):
        self.__name = name
        self.__url = url
        self.__audio_link = audio_link

    def is_loaded(self):
        return self.__audio_link != None

    @property
    def name(self):
        return self.__name

    @property
    def audio_link(self):
        return self.__audio_link

    @audio_link.setter
    def audio_link(self, link):
        self.__audio_link = link

    @property
    def url(self):
        return self.__url

class Queue:
    _MAX_SIZE = 50

    def __init__(self):
        self._queue = [None for _ in range(self._MAX_SIZE)]
        self._head = 0
        self._tail = 0
        self._size = 0
        self._iter = 0
        self._iter_counter = 0

    def __iter__(self):
        self._iter = self._head
        self._iter_counter = 0
        return self

    def __next__(self) -> any:
        if self._size == self._iter_counter:
            raise StopIteration
        elem = self._queue[self._iter]
        self._iter = self.__next_index(self._iter)
        self._iter_counter += 1
        return elem

    def __next_index(self, index) -> int:
        return (index + 1) % self._MAX_SIZE

    @classmethod
    def get_max_size(cls):
        return cls._MAX_SIZE

    def push(self, elem: any) -> None:
        self._queue[self._tail] = elem
        self._tail = self.__next_index(self._tail)
        self._size += 1

    def pop(self) -> any:
        elem = self._queue[self._head]
        self._head = self.__next_index(self._head)
        self._size -= 1
        return elem

    def top(self):
        return self._queue[self._head]

    def clear(self) -> None:
        self._head = 0
        self._tail = 0
        self._size = 0

    def get_queue(self) -> list:
        q = [i for i in self]
        return q

    def is_empty(self) -> bool:
        return not bool(self._size)

    def is_full(self) -> bool:
        return self._size == self._MAX_SIZE

class Optionos:
    YDL_OPTIONS_FOR_TRACK = {
        'quiet': False,
        'format': 'bestaudio/best',
        'ignoreerrors': True,
        'noplaylist': True,
        'simulate': 'True',
        'key': 'FFmpegExtractAudio',
        'agelimit': 30,
    }

    YDL_OPTIONS_FOR_PLAYLIST = {
        'quiet': False,
        'format': 'bestaudio/best',
        'ignoreerrors': True,
        'extract_flat': True,
        'yesplaylist': True,
        'playliststart': 1,
        'playlistend': 50,
        'simulate': 'True',
        'key': 'FFmpegExtractAudio',
        'agelimit': 30,
    }


    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

class UrlChecker:
    @staticmethod
    def __is_playlist_link(text: str) -> bool:
        if 'https://www.youtube.com/playlist' in text:
            return True
        return False

    @staticmethod
    def __is_link(text: str) -> bool:
        if "https://www.youtube.com/" in text:
            return True
        return False

    @staticmethod
    def get_type(text: str) -> int:
        """The method returns 0 if the text is a link to a video, 1 if it is a link to a playlist, 2 in all cases"""
        if UrlChecker.__is_playlist_link(text):
            return 1
        elif UrlChecker.__is_link(text):
            return 0
        else:
            return 2

