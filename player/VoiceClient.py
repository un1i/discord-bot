import discord
from utils import objects


class VoiceClient:
    def __init__(self, ctx):
        self.vc = ctx.guild.voice_client
        self.__ctx = ctx
        self.guild_id = ctx.guild.id

    async def connect_bot(self) -> None:
        if not self.check_connect_bot():
            self.vc = await self.__ctx.user.voice.channel.connect()

    def check_connect_user(self) -> bool:
        if self.__ctx.user.voice:
            return True
        return False

    def check_connect_bot(self) -> bool:
        return self.vc and self.vc.is_connected()

    def play(self, link, object_after) -> None:
        self.vc.play(discord.FFmpegPCMAudio(source=link, **objects.Optionos.FFMPEG_OPTIONS),
                     after= lambda x:object_after.play(self))

    def is_playing(self) -> bool:
        return self.vc.is_playing()

    def is_paused(self) -> bool:
        return self.vc.is_paused()

    def pause(self) -> None:
        self.vc.pause()

    def skip(self) -> None:
        self.vc.stop()

    def resume(self) -> None:
        self.vc.resume()

    async def disconnect(self) -> None:
        await self.vc.disconnect()