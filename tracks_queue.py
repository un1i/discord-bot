import discord

queue = {}
cur_track = {}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}


def play_track(vc, guild_id):

    if queue[guild_id]:
        link, cur_track[guild_id] = queue[guild_id].pop(0)
        vc.play(discord.FFmpegPCMAudio(source=link, **FFMPEG_OPTIONS), after=lambda x=None: play_track(vc, guild_id))
    else:
        cur_track[guild_id] = None


def add_queue(guild_id, link, name):
    max_queue_size = 20

    if guild_id in queue:
        if len(queue[guild_id]) > max_queue_size - 1:
            return False
        else:
            queue[guild_id].append((link, name))
    else:
        queue[guild_id] = [(link, name)]
    return True


def check_guild_in_queue(guild_id):
    return guild_id in queue


def get_queue(guild_id):
    message = ''
    if check_guild_in_queue(guild_id):
        for index, items in enumerate(queue[guild_id]):
            name = items[1]
            message += f"{index+1}. {name}\n"
    return message


def clear_queue(guild_id):
    if check_guild_in_queue(guild_id):
        queue[guild_id].clear()


def get_cur_track(guild_id):
    return cur_track.get(guild_id, None)
