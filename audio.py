from youtube_dl import YoutubeDL, DownloadError

YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'noplaylist': 'False',
    'simulate': 'True',
    'key': 'FFmpegExtractAudio',
}


def check_url(text):
    if "https://" in text:
        return True
    return False


def get_audio(text):
    try:
        with YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(text, download=False)
        link = info['formats'][0]['url']
        name = info['title']
    except DownloadError:
        link, name = False, None

    return link, name


def get_track(text):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(f"ytsearch:{text}", download=False)['entries'][0]
    name = info['title']
    link = info['formats'][0]['url']
    return link, name

