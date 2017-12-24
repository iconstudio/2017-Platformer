from module.pico2d import *
from module.constants import *

import json

__all__ = [
    "audio_dict",
    "audio_load", "audio_stream_load", "audio_get", "audio_json_loads",
    "audio_play", "audio_stream_play", "audio_stream_pause", "audio_stream_resume", "audio_stream_stop",
    "audio_volume", "audio_stream_volume", "audio_get_volume_sfx_global", "audio_get_volume_music_global",
    "audio_set_volume_sfx_global", "audio_set_volume_music_global",
]

audio_list = set()
audio_dict: dict = {}
music_last: Music = None
volsfx, volmus = 10, 8


def audio_load(filepaths, name = str("default")) -> Wav:
    global audio_dict
    new = load_wav(filepaths)
    new.name = name
    audio_dict[name] = new
    return new


def audio_stream_load(filepaths, name = str("default")) -> Music:
    global audio_dict
    new = load_music(filepaths)
    new.name = name
    audio_dict[name] = new
    return new


def audio_get(name: str) -> Wav or Music:
    global audio_dict
    try:
        val = audio_dict[name]
    except KeyError as e:
        raise RuntimeError("오디오 " + str(e) + " 는 존재하지 않습니다!")
    return val


def audio_set_volume_sfx_global(v):
    global volsfx
    volsfx = min(max(v, 0), 10)


def audio_set_volume_music_global(v):
    global volmus
    volmus = min(max(v, 0), 10)


def audio_get_volume_sfx_global():
    global volsfx
    return volsfx


def audio_get_volume_music_global():
    global volmus
    return volmus


def audio_play(name: str) -> Wav:
    sfx: Wav = audio_get(name)
    sfx.set_volume(audio_get_volume_sfx_global() / 10 * 128)
    sfx.play()

    global audio_list
    audio_list.add(sfx)
    return sfx


def audio_stream_play(name: str) -> Music:
    sfx: Music = audio_get(name)
    global music_last
    music_last = sfx
    sfx.set_volume(audio_get_volume_music_global() / 10 * 128)
    sfx.repeat_play()

    global audio_list
    audio_list.add(sfx)
    return sfx


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
                if content["muse"] is true:
                    audio_stream_load(content["path"], content["name"])
                else:
                    audio_load(content["path"], content["name"])

    except FileNotFoundError:
        pass
