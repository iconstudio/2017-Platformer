from module.pico2d import *
from module.constants import *

import json

from module.framework import audio_get_volume_sfx_global, audio_get_volume_music_global

__all__ = [
    "audio_list",
    "audio_load", "audio_stream_load", "audio_get", "audio_json_loads",
    "audio_play", "audio_stream_play", "audio_stream_pause", "audio_stream_resume", "audio_stream_stop",
    "audio_volume", "audio_stream_volume"
]

audio_list: dict = {}
music_last: Music = None


def audio_load(filepaths, name = str("default")) -> Wav:
    global audio_list
    new = load_wav(filepaths)
    new.name = name
    audio_list[name] = new
    return new


def audio_stream_load(filepaths, name = str("default")) -> Music:
    global audio_list
    new = load_music(filepaths)
    new.name = name
    audio_list[name] = new
    return new


def audio_get(name: str) -> Wav or Music:
    global audio_list
    try:
        val = audio_list[name]
    except KeyError as e:
        raise RuntimeError("오디오 " + str(e) + " 는 존재하지 않습니다!")
    return val


def audio_play(name: str):
    sfx: Wav = audio_get(name)
    sfx.play()
    sfx.set_volume(audio_get_volume_sfx_global())


def audio_stream_play(name: str):
    sfx: Music = audio_get(name)
    global music_last
    music_last = sfx
    sfx.set_volume(audio_get_volume_music_global())
    sfx.repeat_play()


# 0 ~ 128
def audio_volume(name: str, v):
    sfx: Wav = audio_get(name)
    sfx.set_volume(v)


def audio_stream_volume(name: str, v):
    sfx: Music = audio_get(name)
    sfx.set_volume(v)


def audio_stream_pause():
    global music_last
    music_last.pause()


def audio_stream_resume():
    global music_last
    music_last.resume()


def audio_stream_stop():
    global music_last
    music_last.stop()


def audio_json_loads():
    try:
        with open(path_data + "audio.json") as wavfile:
            parsed = json.load(wavfile)

            for content in parsed:
                if content["muse"]:
                    audio_stream_load(content["path"], content["name"])
                else:
                    audio_load(content["path"], content["name"])

    except FileNotFoundError:
        pass
