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

q = {}

cur_track = None


def check_connect_user(ctx):
    if ctx.message.author.voice:
        return True
    return False


def check_queue(vc, guild_id):
    global cur_track

    if q[guild_id]:
        link, cur_track = q[guild_id].pop(0)
        vc.play(discord.FFmpegPCMAudio(source=link, **FFMPEG_OPTIONS), after=lambda x=None: check_queue(vc, guild_id))
    else:
        cur_track = None


def add_queue(guild_id, link, name):
    max_queue_size = 20

    if guild_id in q:
        if len(q[guild_id]) > max_queue_size - 1:
            return False
        else:
            q[guild_id].append((link, name))
    else:
        q[guild_id] = [(link, name)]
    return True


@client.command()
async def play(ctx, url):
    """Play audio from the Youtube link."""

    if not check_connect_user(ctx):
        await ctx.send(msg_connect_voice)
        return

    vc = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    if not (vc and vc.is_connected()):
        vc = await ctx.message.author.voice.channel.connect()
    guild_id = vc.guild.id

    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
    link = info['formats'][0]['url']
    name = info['title']

    global cur_track

    if vc.is_playing():
        if add_queue(guild_id, link, name):
            await ctx.send(msg_queue_add)
        else:
            await ctx.send(msg_max_queue)
    else:
        vc.play(discord.FFmpegPCMAudio(source=link, **FFMPEG_OPTIONS), after=lambda x=None: check_queue(vc, guild_id))
        cur_track = name


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
async def clear(ctx):
    """Clear the queue."""
    guild_id = ctx.message.guild.id
    q[guild_id].clear()
    await ctx.send(msg_queue_clear)


@client.command()
async def current(ctx):
    """Show playing track"""
    if cur_track:
        await ctx.send(f"Now playing: {cur_track}")
    else:
        await ctx.send(msg_nothing_playing)


@client.command()
async def queue(ctx):
    """Show tracks in queue"""
    message = ''
    guild_id = ctx.message.guild.id
    if guild_id in q:
        for index, items in enumerate(q[guild_id]):
            name = items[1]
            message += f"{index+1}. {name}\n"
    await ctx.send(msg_empty_queue if message == '' else message)


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
