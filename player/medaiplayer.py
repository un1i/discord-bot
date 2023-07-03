from utils import objects, errors
from player import downloader as dw
from youtube_search import YoutubeSearch
from player import message_components as mc
from messages import message as ms

class AudioPlayer:
    def __init__(self, vc, guild, ctx):
        self.__vc = vc
        self.__guild = guild
        self.__ctx = ctx

    async def play_audio(self, text):
        self.__text = text
        request_type = objects.UrlChecker.get_type(text)
        if request_type == 0:
            track, is_playing = self.__play_audio_by_link()
            if is_playing:
                await self.__ctx.response.send_message(ms.Message.added_to_queue(track))
            else:
                await self.__ctx.response.send_message(ms.Message.now_playing(track))

        elif request_type == 1:
            await self.__ctx.response.send_message(ms.Message.loading_playlist())
            playlist_name = await self.__play_audio_by_playlist()
            # await self.__ctx.response.send_message(ms.Message.added_playlist_to_queue(playlist_name))
            await self.__ctx.edit_original_response(content=ms.Message.added_playlist_to_queue(playlist_name))
        else:
            tracks = self.__play_audio_by_title()
            await self.__ctx.response.send_message('', view=mc.TrackSelectView(tracks, vc=self.__vc, guild=self.__guild))

    def __play_audio_by_link(self) -> (str, bool):
        track = dw.Downloader.get_track(self.__text)
        self.__guild.add_track(track)
        is_playing = self.__vc.is_playing()
        is_paused = self.__vc.is_paused()
        if not is_playing and not is_paused:
            self.__guild.play(self.__vc)
        return (track.name, is_playing)

    async def __play_audio_by_playlist(self) -> str:
        playlist_name, tracks = await dw.Downloader.get_playlist(self.__text)
        res = self.__guild.add_playlist(tracks)
        is_playing = self.__vc.is_playing()
        is_paused = self.__vc.is_paused()
        if not is_playing and not is_paused:
            self.__guild.play(self.__vc)
        else:
            self.__guild.preload()
        if not res:
            raise errors.FullQueueForPlaylist
        return playlist_name

    def __play_audio_by_title(self) -> dict():
        info = YoutubeSearch(self.__text, max_results=5).to_dict()
        tracks = {}
        for track in info:
            # Если id начинается с "-", то трек не ищется в поиске
            if track['id'][0] == '-':
                track['id'] = track['id'][1:]
            tracks[track['title']] = track['id']
        return tracks

