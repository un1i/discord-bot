import discord
import discord.components
from player import downloader as dw
from utils import errors
from messages import message as ms


class TrackSelect(discord.ui.Select):
    def __init__(self, tracks: dict, vc, guild):
        super().__init__()
        self.options = [discord.SelectOption(label=track) for track in tracks]
        self.placeholder = 'Выберите трек'
        self.tracks = tracks
        self.vc = vc
        self.guild = guild

    async def callback(self, ctx):
        self.disabled = True
        track_id = self.tracks[self.values[0]]
        track = dw.Downloader.get_track_by_title(track_id)
        await ctx.response.edit_message(view=self.view)
        try:
            self.guild.add_track(track)
        except errors.FullQueue:
            await ctx.followup.send(ms.Message.full_queue())
            return

        is_playing = self.vc.is_playing()
        is_paused = self.vc.is_paused()
        if not is_playing and not is_paused:
            self.guild.play(self.vc)
            await ctx.followup.send(ms.Message.now_playing(track.name))
        else:
            await ctx.followup.send(ms.Message.added_to_queue(track.name))



class TrackSelectView(discord.ui.View):
    def __init__(self, tracks: list, *, vc, guild, timeout=100):
        super().__init__(timeout=timeout)
        self.add_item(TrackSelect(tracks, vc=vc, guild=guild))



