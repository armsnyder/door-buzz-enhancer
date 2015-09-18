__author__ = 'flame'

from linux_lib import *
import door_buzz_simple

waveform = []


def listener(w, rate, sw, start_time):
    global waveform
    if len(waveform) > 16000:
        end_stream()
    waveform.extend(w)


begin_stream(listener)

print max([door_buzz_simple.to_db(x, 8) for x in waveform])
