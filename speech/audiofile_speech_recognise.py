#!/usr/bin/python

# encoding: utf-8

from __future__ import print_function
import os
import sys
import time
import socket
from pocketsphinx import AudioFile, Pocketsphinx, get_model_path
from __playwave import playwave

sys_model_path = get_model_path()
voice_path = os.path.join(os.getcwd(), 'voice')
usr_model_path = os.path.join(os.getcwd(), 'model')

config = {
    'hmm': os.path.join(sys_model_path, 'en-us'),
    'lm': os.path.join(usr_model_path, '4767.lm'),
    'dict': os.path.join(usr_model_path, '4767.dic')
}

ps = Pocketsphinx(**config)

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

def turn_on_the_light():
    #TODO
    print("do: turn on the light")

def turn_off_the_light():
    #TODO
    print("do: turn off the light")

def null_func():
    pass

switch_funcs = {"light on": turn_on_the_light, "light off": turn_off_the_light, "null": null_func}

def do_baidu_speech_recognise(speech_file):
    return "null"

def do_sphinx_speech_recognise(speech_file):
    ps.decode(
        audio_file=os.path.join(voice_path, speech_file),
        buffer_size=2048,
        no_search=False,
        full_utt=False
    )

    best_result = ps.best(count=10)
    speech = []

    for phrase in best_result:
        speech.append(phrase[0])

    if ("TURN ON THE LIGHT" in speech):
        playwave(os.path.join(voice_path, 'beep_lo.wav'))
        print("turn on the light")
        return "light on"
    elif ("TURN OFF THE LIGHT" in speech):
        playwave(os.path.join(voice_path, 'beep_lo.wav'))
        print("turn off the light")
        return "light off"
    else:
        return "null"

if __name__ == "__main__":
    ps.decode(
        audio_file=os.path.join(voice_path, "baby.wav"),
        buffer_size=2048,
        no_search=False,
        full_utt=False
    )

    best_result = ps.best(count=10)
    speech = []

    for phrase in best_result:
        speech.append(phrase[0])

    time.sleep(3)

    while True:
        if "HI BABY" in speech:
            print("recognise right")

        playwave(os.path.join(voice_path, 'beep_hi.wav'))

        time.sleep(3)

        net_status = is_net_ok(('www.baidu.com',443))
        recognise_result = ""
        if net_status:
            print("######baidu recognise")
            recognise_result = do_baidu_speech_recognise("light_on.wav")
        else:
            print("######sphinx recognise")
            recognise_result = do_sphinx_speech_recognise("light_on.wav")

        print(recognise_result)
        func = switch_funcs[recognise_result]
        func()
        break
