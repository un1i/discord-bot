import discord

max_queue_size = 50
queue = {}
cur_track = {}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}


def get_max_queue_size():
    return max_queue_size


def get_available_space(guild_id):
    return max_queue_size - len(queue[guild_id])


def play_track(vc, guild_id):

    if queue[guild_id]:
        link, cur_track[guild_id] = queue[guild_id].pop(0)
        vc.play(discord.FFmpegPCMAudio(source=link, **FFMPEG_OPTIONS), after=lambda x=None: play_track(vc, guild_id))
    else:
        cur_track[guild_id] = None


def add_queue(guild_id, link, name):
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
    message = ['']
    if check_guild_in_queue(guild_id):
        i = 0
        for index, items in enumerate(queue[guild_id]):
            name = items[1]
            track = f"{index+1}. {name}\n"
            if len(message[i] + track) >= 2000:
                message.append('')
                i += 1
            message[i] += track
    return message


def clear_queue(guild_id):
    if check_guild_in_queue(guild_id):
        queue[guild_id].clear()


def get_cur_track(guild_id):
    return cur_track.get(guild_id, None)


def add_playlist_to_queue(guild_id, playlist, additional_track):
    available_space = max_queue_size - len(queue.get(guild_id, 0))

    if guild_id in queue:
        queue[guild_id] += playlist[:available_space]
    else:
        queue[guild_id] = playlist[:available_space]

    playlist_size = len(playlist)
    if playlist_size != 0 and available_space >= playlist_size:
        if additional_track:
            playlist_size += 1
        return True, playlist_size
    else:
        if additional_track:
            available_space += 1
        return False, available_space
