from utils import objects, errors
from player import downloader as dw


class Guild:
    def __init__(self, id: int, text_channel):
        self.__id = id
        self.__queue = objects.Queue()
        self.__cur_track = None
        self.__text_channel = text_channel

    def play(self, vc) -> None:
        if not self.__queue.is_empty():
            track = self.__queue.pop()
            if not track.is_loaded():
                dw.Downloader.load_track(track)
            self.__cur_track = track.name
            vc.play(track.audio_link, object_after=self)
            self.preload()
        else:
            self.__cur_track = None

    def add_track(self, track: objects.Track) -> None:
        if not self.__queue.is_full():
            self.__queue.push(track)
        else:
            raise errors.FullQueue

    def add_playlist(self, tracks: list[objects.Track]) -> bool:
        for track in tracks:
            if not self.__queue.is_full():
                self.__queue.push(track)
            else:
                return False
        return True

    def get_queue(self) -> list[str]:
        MAX_MSG_SIZE = 2000
        message = ['']
        i = 0

        for index, track in enumerate(self.__queue, start=1):
            str_track = f"{index}. {track.name}\n"
            if len(message[i] + str_track) >= MAX_MSG_SIZE:
                message.append('')
                i += 1
            message[i] += str_track

        return message

    def clear_queue(self) -> None:
        self.__queue.clear()

    def get_cur_track(self):
        return self.__cur_track

    def preload(self):
        if not self.__queue.is_empty():
            next_track = self.__queue.top()
            if not next_track.is_loaded():
                dw.Downloader.load_track(next_track)

    @property
    def text_channel(self):
        return self.__text_channel


class Guilds:
    def __init__(self):
        self.__guilds = {}

    def __getitem__(self, item):
        return self.__guilds.get(item)

    def add(self, id: int, text_channel = None) -> Guild:
        if id not in self.__guilds:
            self.__guilds[id] = Guild(id, text_channel)
        return self.__guilds.get(id)


    def remove(self, id:int) -> None:
        self.__guilds.pop(id, None)





