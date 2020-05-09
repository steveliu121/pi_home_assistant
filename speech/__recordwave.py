#!/usr/bin/python

"""PyAudio example: Record a few seconds of audio and save to a WAVE file."""

import pyaudio
import wave


CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "output.wav"

def get_mic_pcm_data(rate, channels, bit_format, record_seconds, mic_buffer):
    pya = pyaudio.PyAudio()

    stream = pya.open(format=bit_format,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("* recording")

    for i in range(0, int(rate / CHUNK * record_seconds)):
        data = stream.read(CHUNK)
        mic_buffer.append(data)

    print("* done recording")

    stream.stop_stream()
    stream.close()
    pya.terminate()

if __name__ == "__main__":
    pya = pyaudio.PyAudio()

    mic_buffer = []
    get_mic_pcm_data(RATE, CHANNELS, FORMAT, RECORD_SECONDS, mic_buffer)
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(pya.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(mic_buffer))
    wf.close()
