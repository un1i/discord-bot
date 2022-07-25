from youtube_dl import YoutubeDL, DownloadError
from tracks_queue import get_max_queue_size, get_available_space
max_queue_size = get_max_queue_size()

YDL_OPTIONS = {
    'quiet': False,
    'format': 'bestaudio/best',
    'yesplaylist': True,
    'playliststart': 1,
    'playlistend': max_queue_size,
    'simulate': 'True',
    'key': 'FFmpegExtractAudio',
    'agelimit': 30,
}


def check_url(text):
    if "https://" in text:
        return True
    return False


def get_audio(text):
    check_playlist = False  # Flag to see if you need to upload playlists

    if 'https://www.youtube.com/playlist' in text:
        check_playlist = True
        YDL_OPTIONS['playlistend'] = 1
        try:
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(text, download=False)['entries'][0]
            link = info['formats'][0]['url']
            name = info['title']
        except DownloadError:
            link, name = False, None
        finally:
            YDL_OPTIONS['playlistend'] = max_queue_size
    else:
        try:
            with YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(text, download=False)
            link = info['formats'][0]['url']
            name = info['title']
        except DownloadError:
            link, name = False, None

    return link, name, check_playlist


def get_audio_by_name(text):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(f"ytsearch:{text}", download=False)['entries'][0]
    name = info['title']
    link = info['formats'][0]['url']
    return link, name


def get_playlist(url, guild_id):
    YDL_OPTIONS['playliststart'] = 2
    YDL_OPTIONS['playlistend'] = get_available_space(guild_id) + 1
    track_list = []
    try:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)['entries']
        for track in info:
            link = track['formats'][0]['url']
            name = track['title']
            track_list.append((link, name))
    except DownloadError:
        pass
    finally:
        YDL_OPTIONS['playliststart'] = 1
        YDL_OPTIONS['playlistend'] = max_queue_size

    return track_list
