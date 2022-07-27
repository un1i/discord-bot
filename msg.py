msg_help = """
-play "youtube link" 
The bot connects to the voice channel and turns on the audio via the youtube link or by the track name, if the audio is\
 already playing, the bot adds the track to the queue.
 
-pause
Pause the playing audio.

-resume
Continue audio playback.

-skip
Skip the current audio.

-leave
The bot exits the voice channel

-clear
Clear the queue.
"""

msg_queue_add = "This audio has been added to the queue!"

msg_already_pause = "Playback is already on pause!"

msg_pause = "Playback is paused!"

msg_nothing_playing = "Nothing is playing right now!"

msg_already_play = "Audio is already playing!"

msg_resume = "Playback has resumed!"

msg_queue_clear = "The queue cleared!"

msg_max_queue = "You can't add a track. The maximum queue size is 50."

msg_empty_queue = "No tracks in the queue."

msg_connect_voice = "Connect to the voice channel first!"

msg_start_play = "Run the track to use this command!"

msg_no_connect = "The bot is not connected to the voice channel!"

msg_invalid_url = "The link is not valid!"

msg_invalid_command = "This command does not exist.\nUse -help to view the available commands."

msg_error = "Something went wrong..."


def msg_playlist_add(playlist_size):
    if playlist_size > 1:
        msg = f"{playlist_size} tracks added to the queue."
    else:
        msg = f"{playlist_size} track added to the queue."
    return msg


def msg_incomplete_playlist_add(playlist_size):
    if playlist_size > 1:
        msg = f"Only {playlist_size} tracks have been added because the maximum queue size is 50."
    elif playlist_size == 1:
        msg = f"Only {playlist_size} track have been added because the maximum queue size is 50."
    else:
        msg = "You can't add a track. The maximum queue size is 50."

    return msg



