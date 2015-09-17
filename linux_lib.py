__author__ = 'Adam Snyder'

import alsaaudio
import numpy
import time

streaming = False


def begin_stream(listener):
    global streaming

    fmt = alsaaudio.PCM_FORMAT_S8
    rate = 8000
    period = 1024

    card = alsaaudio.cards()[1]
    stream = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NORMAL, card)
    stream.setchannels(1)
    stream.setrate(rate)
    stream.setformat(fmt)
    stream.setperiodsize(period)
    streaming = True

    while streaming:
        start_time = time.time()
        l, data = stream.read()
        if l:
            decoded = numpy.fromstring(data, 'int8')
            listener(decoded.tolist(), rate, 8, start_time)


def end_stream():
    global streaming
    streaming = False
