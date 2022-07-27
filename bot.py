import asyncio
from config import token
from discord.ext import commands
from msg import *
from tracks_queue import play_track, add_queue, get_queue, clear_queue, get_cur_track, add_playlist_to_queue, \
    check_activity
from audio import check_url, get_audio, get_audio_by_name, get_playlist

client = commands.Bot(command_prefix='-')
client.remove_command('help')


def check_connect_user(ctx):
    if ctx.message.author.voice:
        return True
    return False


def check_connect_bot(vc):
    if vc is None:
        return False
    return True


@client.event
async def on_ready():
    time_sleep = 60
    while True:
        asyncio.run_coroutine_threadsafe(check_activity(), client.loop)
        await asyncio.sleep(time_sleep)


@client.command()
async def play(ctx,  *, text):
    """Play audio from the Youtube link."""

    if not check_connect_user(ctx):
        await ctx.send(msg_connect_voice)
        return

    vc = ctx.message.guild.voice_client
    if not (vc and vc.is_connected()):
        vc = await ctx.message.author.voice.channel.connect()
    guild_id = vc.guild.id

    if check_url(text):
        link, name, check_playlist = get_audio(text)
        if not link:
            await ctx.send(msg_invalid_url)
            return
    else:
        check_playlist = False
        link, name = get_audio_by_name(text)

    res_add = add_queue(guild_id, link, name)
    if vc.is_playing():
        if not check_playlist:
            if res_add:
                await ctx.send(msg_queue_add)
            else:
                await ctx.send(msg_max_queue)
    else:
        res_add = False  # used to compile the total amount of tracks added from the playlist
        play_track(vc, guild_id)

    if check_playlist:
        res, playlist_size = add_playlist_to_queue(guild_id, get_playlist(text, guild_id), res_add)
        await ctx.send(msg_playlist_add(playlist_size) if res else msg_incomplete_playlist_add(playlist_size))


@client.command()
async def pause(ctx):
    """Pause the playing audio."""
    server = ctx.message.guild
    vc = server.voice_client
    if not check_connect_bot(vc):
        await ctx.send(msg_start_play)
        return
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
    if not check_connect_bot(vc):
        await ctx.send(msg_start_play)
        return
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
    if not check_connect_bot(vc):
        await ctx.send(msg_start_play)
        return
    vc.stop()


@client.command()
async def clear(ctx):
    """Clear the queue."""
    guild_id = ctx.message.guild.id
    clear_queue(guild_id)
    await ctx.send(msg_queue_clear)


@client.command()
async def current(ctx):
    """Show playing track"""
    guild_id = ctx.message.guild.id
    cur_track = get_cur_track(guild_id)
    if cur_track:
        await ctx.send(f"Now playing: {cur_track}")
    else:
        await ctx.send(msg_nothing_playing)


@client.command()
async def queue(ctx):
    """Show tracks in queue"""
    guild_id = ctx.message.guild.id
    messages = get_queue(guild_id)
    for message in messages:
        await ctx.send(msg_empty_queue if message == '' else message)


@client.command()
async def leave(ctx):
    """The bot exits the voice channel."""
    server = ctx.message.guild
    vc = server.voice_client
    if not check_connect_bot(vc):
        await ctx.send(msg_no_connect)
        return
    await vc.disconnect()


@client.command()
async def help(ctx):
    await ctx.send(msg_help)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(msg_invalid_command)

if __name__ == '__main__':
    client.run(token)
