__author__ = 'Adam Snyder'

import pyaudio
import numpy
import time

streaming = False


def begin_stream(listener):
    global streaming

    fmt = pyaudio.paInt8
    rate = 8000
    chunk = 1024

    audio = pyaudio.PyAudio()
    stream = audio.open(format=fmt, channels=1, rate=rate, input=True, frames_per_buffer=chunk)
    streaming = True

    while streaming:
        start_time = time.time()
        data = stream.read(chunk)
        decoded = numpy.fromstring(data, 'int8')
        listener(decoded.tolist(), rate, 8, start_time)
    stream.stop_stream()
    stream.close()
    audio.terminate()


def end_stream():
    global streaming
    streaming = False
