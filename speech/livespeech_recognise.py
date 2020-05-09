#!/usr/bin/python

# encoding: utf-8

from __future__ import print_function
import os
import socket
from pocketsphinx import LiveSpeech, get_model_path
from __playwave import playwave
from __baidu_speech_recognise import get_baidu_asr


sys_model_path = get_model_path()
voice_path = os.path.join(os.getcwd(), 'voice')
usr_model_path = os.path.join(os.getcwd(), 'model')

speech = LiveSpeech(
    verbose=False,
    sampling_rate=44100,
    buffer_size=4096,
    no_search=False,
    full_utt=False,
    hmm=os.path.join(sys_model_path, 'en-us'),
    lm=os.path.join(usr_model_path, '4767.lm'),
    dic=os.path.join(usr_model_path, '4767.dic')
)


def turn_on_the_light():
    #TODO
    print("do: turn on the light")

def turn_off_the_light():
    #TODO
    print("do: turn off the light")

def null_func():
    pass

switch_funcs = {"light on": turn_on_the_light, "light off": turn_off_the_light, "null": null_func}

def is_net_ok(testserver):
    s = socket.socket()
    s.settimeout(3)
    try:
        status = s.connect_ex(testserver)
        if status == 0:
            s.close()
            return True
        else:
            return False
    except Exception as e:
        return False

def do_baidu_speech_recognise():
    result_str = get_baidu_asr()
    if result_str == "turn on the light":
        playwave(os.path.join(voice_path, 'beep_lo.wav'))
        print("turn on the light")
        return "light on"
    elif result_str == "turn off the light":
        playwave(os.path.join(voice_path, 'beep_lo.wav'))
        print("turn off the light")
        return "light off"
    else:
        playwave(os.path.join(voice_path, 'sorry.wav'))
        return "null"

def do_sphinx_speech_recognise():
    for phrase in speech:
        if str(phrase) == "TURN ON THE LIGHT":
            playwave(os.path.join(voice_path, 'beep_lo.wav'))
            print("turn on the light")
            return "light on"
        elif str(phrase) == "TURN OFF THE LIGHT":
            playwave(os.path.join(voice_path, 'beep_lo.wav'))
            print("turn off the light")
            return "light off"
        else:
            playwave(os.path.join(voice_path, 'sorry.wav'))
            return "null"

if __name__ == "__main__":
    while True:
        for phrase in speech:
            if str(phrase) == "HI BABY":
                print("recognise right")
                playwave(os.path.join(voice_path, 'beep_hi.wav'))
                break
            else:
                continue

        net_status = is_net_ok(('www.baidu.com',443))
        net_status = False
        if net_status:
            # online speech recognise based on baidu AI
            recognise_result = do_baidu_speech_recognise()
        else:
            # offline speech recognise based on PocketSphinx
            recognise_result = do_sphinx_speech_recognise()

        func = switch_funcs[recognise_result]
        func()
