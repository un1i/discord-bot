import discord
from youtube_dl import YoutubeDL
from config import token
from discord.ext import commands
from msg import *

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': 'False',
    'simulate': 'True',
    'key': 'FFmpegExtractAudio',
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}
client = commands.Bot(command_prefix='-')

queue = {}


def check_queue(vc, guild_id):
    if queue[guild_id]:
        link = queue[guild_id].pop(0)
        vc.play(discord.FFmpegPCMAudio(source=link, **FFMPEG_OPTIONS), after=lambda x=None: check_queue(vc, guild_id))


@client.command()
async def play(ctx, url):
    """Play audio from the Youtube link."""
    vc = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    if not (vc and vc.is_connected()):
        vc = await ctx.message.author.voice.channel.connect()

    guild_id = vc.guild.id

    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
    link = info['formats'][0]['url']

    if vc.is_playing():
        if guild_id in queue:
            queue[guild_id].append(link)
        else:
            queue[guild_id] = [link]
        await ctx.send(msg_queue_add)

    else:
        vc.play(discord.FFmpegPCMAudio(source=link, **FFMPEG_OPTIONS), after=lambda x=None: check_queue(vc, guild_id))


@client.command()
async def pause(ctx):
    """Pause the playing audio."""
    server = ctx.message.guild
    vc = server.voice_client
    if vc.is_paused():
        await ctx.send(msg_already_pause)
    else:
        vc.pause()
        await ctx.send(msg_pause)

@client.command()
async def resume(ctx):
    """Continue audio playback."""
    server = ctx.message.guild
    vc = server.voice_client
    if vc.is_playing():
        await ctx.send(msg_already_play)
    else:
        vc.resume()
        await ctx.send(msg_resume)


@client.command()
async def skip(ctx):
    """Skip the current audio."""
    server = ctx.message.guild
    vc = server.voice_client
    vc.stop()


@client.command()
async def leave(ctx):
    """The bot exits the voice channel."""
    server = ctx.message.guild
    vc = server.voice_client
    await vc.disconnect()


@client.command()
async def commands(ctx):
    """More information about the commands"""
    await ctx.send(msg_help)


if __name__ == '__main__':
    client.run(token)
