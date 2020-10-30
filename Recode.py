#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time

import pyaudio
from TTS import tts_
import wave
# !/usr/bin/env python
# coding: utf-8

# In[ ]:


import time

import pyaudio
import wave

def recode(text, num, seconds=3):
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 48000
    CHUNK = 1
    RECORD_SECONDS = seconds
    WAVE_OUTPUT_FILENAME = "file.wav"
    audio = pyaudio.PyAudio()
    print("audio = ", audio)
    # start Recording
    stream = audio.open(format=pyaudio.paInt16,

                        channels=CHANNELS,

                        rate=RATE,

                        input=True,

                        input_device_index=9,

                        frames_per_buffer=CHUNK)


    tts_(text, num) ####################
    text

    # text = text.replace(" ", 1)

    # time.sleep(len(text)*0.1)

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording")

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

