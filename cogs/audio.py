from discord import app_commands
from discord.ext import commands
from messages import message as ms, description as dsc
from player import medaiplayer as mp, VoiceClient
from utils import errors, guild


class Audio(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guilds = guild.Guilds()

    @app_commands.command(name='play', description=dsc.Description.play())
    @app_commands.describe(text='Ссылка или название')
    async def play(self, ctx, text: str):
        try:
            vc = VoiceClient.VoiceClient(ctx)
            if not vc.check_connect_user():
                await ctx.response.send_message(ms.Message.connect_to_channel())
                return
            await vc.connect_bot()
            text_channel = ctx.channel
            guild = self.guilds.add(vc.guild_id, text_channel)
            player = mp.AudioPlayer(vc, guild, ctx)
            await player.play_audio(text)
        except errors.FullQueue:
            await ctx.response.send_message(ms.Message.full_queue())
        except errors.FullQueueForPlaylist:
            await ctx.edit_original_response(content=ms.Message.full_queue_for_playlist())

    @app_commands.command(name='pause', description=dsc.Description.pause())
    async def pause(self, ctx):
        vc = VoiceClient.VoiceClient(ctx)
        if not vc.check_connect_bot():
            await ctx.response.send_message(ms.Message.start_play())
            return

        if vc.is_paused():
            await ctx.response.send_message(ms.Message.already_pause())
            pass
        else:
            vc.pause()
            await ctx.response.send_message(ms.Message.successful_pause())

    @app_commands.command(name='resume', description=dsc.Description.resume())
    async def resume(self, ctx):
        vc = VoiceClient.VoiceClient(ctx)
        text_channel = ctx.channel
        guild = self.guilds.add(vc.guild_id, text_channel)
        if not vc.check_connect_bot() or guild.get_cur_track() is None:
            await ctx.response.send_message(ms.Message.start_play())
            return

        if vc.is_playing():
            await ctx.response.send_message(ms.Message.already_play())
            pass
        else:
            vc.resume()
            await ctx.response.send_message(ms.Message.successful_resume())


    @app_commands.command(name='skip', description=dsc.Description.skip())
    async def skip(self, ctx):
        vc = VoiceClient.VoiceClient(ctx)
        if not vc.check_connect_bot():
            await ctx.response.send_message(ms.Message.start_play())
            return
        vc.skip()
        await ctx.response.send_message(ms.Message.successful_skip())

    @app_commands.command(name='clear', description=dsc.Description.clear())
    async def clear(self, ctx):
        guild_id = ctx.guild_id
        text_channel = ctx.channel
        guild = self.guilds.add(guild_id, text_channel)
        guild.clear_queue()
        await ctx.response.send_message(ms.Message.queue_cleared())

    @app_commands.command(name='current', description=dsc.Description.current())
    async def current(self, ctx):
        guild_id = ctx.guild_id
        text_channel = ctx.channel
        guild = self.guilds.add(guild_id, text_channel)
        cur_track = guild.get_cur_track()
        if cur_track:
            await ctx.response.send_message(ms.Message.now_playing(cur_track))
        else:
            await ctx.response.send_message(ms.Message.nothing_is_playing())

    @app_commands.command(name='queue', description=dsc.Description.queue())
    async def queue(self, ctx):
        guild_id = ctx.guild_id
        text_channel = ctx.channel
        guild = self.guilds.add(guild_id, text_channel)
        messages = guild.get_queue()
        if not messages[0]:
            await ctx.response.send_message(ms.Message.empty_queue())
            return
        await ctx.response.send_message(messages[0])
        for i in range(1, len(messages)):
            await ctx.followup.send(messages[i])

    @app_commands.command(name='leave', description=dsc.Description.leave())
    async def leave(self, ctx):
        vc = VoiceClient.VoiceClient(ctx)
        guild_id = ctx.guild_id
        if vc.check_connect_bot():
            await vc.disconnect()
            self.guilds.remove(guild_id)
            await ctx.response.send_message(ms.Message.leave_channel())
        else:
            await ctx.response.send_message(ms.Message.not_connected())

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        vc = member.guild.voice_client
        if vc is not None and len(vc.channel.members) == 1:
            guild_id = member.guild.id
            await vc.disconnect()
            text_channel = self.guilds[guild_id].text_channel
            await text_channel.send(ms.Message.disconnect_message())
            self.guilds.remove(guild_id)

    @commands.command()
    async def sync(self, ctx):
        fmt = await ctx.bot.tree.sync()
        await ctx.send(len(fmt))









async def setup(bot):
    await bot.add_cog(Audio(bot))