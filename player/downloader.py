from utils import objects
from yt_dlp import YoutubeDL


class Downloader:
    @staticmethod
    def get_track(url: str) -> objects.Track:
        with YoutubeDL(objects.Optionos.YDL_OPTIONS_FOR_TRACK) as ydl:
            info = ydl.extract_info(url, download=False)

        link = info['formats'][3]['url']
        name = info['title']
        return objects.Track(name, url, link)

    @staticmethod
    def get_track_by_title(title: str,) -> objects.Track:
        with YoutubeDL(objects.Optionos.YDL_OPTIONS_FOR_TRACK) as ydl:
                info = ydl.extract_info(f"ytsearch:{title}", download=False)['entries'][0]
        name = info['title']
        url = f" https://www.youtube.com/watch?v={info['id']}"
        link = info['url']
        return objects.Track(name, url, link)

    @staticmethod
    async def get_playlist(url: str) -> tuple:
        track_list = []
        with YoutubeDL(objects.Optionos.YDL_OPTIONS_FOR_PLAYLIST) as ydl:
            info = ydl.extract_info(url, download=False)
        playlist_name = info['title']
        for element in info['entries']:
            track = objects.Track(element['title'], element['url'])
            track_list.append(track)
        return playlist_name, track_list

    @staticmethod
    def load_track(track: objects.Track):
        with YoutubeDL(objects.Optionos.YDL_OPTIONS_FOR_TRACK) as ydl:
            info = ydl.extract_info(track.url, download=False)
        link = info['formats'][3]['url']
        track.audio_link = link





