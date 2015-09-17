__author__ = 'Adam Snyder'

import math

from osx_lib import *
import wave
import struct

LIFT_DELAY = 20
SAMPLE_RATE = 8000
SAMPLE_SIZE = 8

actions_list = []
global_silence_counter = 0
wav_counter = 0


def main():
    begin_stream(listener)


def listener(data, sample_rate, sample_size, start_time):
    global actions_list, global_silence_counter
    if len(actions_list):
        last_onset = actions_list[-1]
    else:
        last_onset = None
    onsets, global_silence_counter = detect_onsets(data, -30, sample_rate, sample_size, LIFT_DELAY, start_time,
                                                   last_onset, global_silence_counter)
    actions_list.extend(onsets)
    for onset in onsets:
        if onset[0]:
            print ' ON ' + str(onset[1])
        else:
            print 'OFF '+str(onset[1])


def detect_onsets(waveform, volume_threshold, sample_rate=SAMPLE_RATE, sample_size=SAMPLE_SIZE, lift_delay=LIFT_DELAY,
                  start_time=0, last_onset=None, silence_counter=0):
    global wav_counter  # Debug
    result = []
    sample_counter = 0
    if last_onset and not last_onset[0]:
        silence_counter = 0
    lift_samples = int(float(sample_rate) / 1000 * lift_delay)
    db_waveform = [to_db(w, sample_size) for w in waveform]
    while len(db_waveform):
        if last_onset and last_onset[0]:
            sample = None
            for i in range(len(db_waveform)):
                if db_waveform[i] < volume_threshold:
                    silence_counter += 1
                else:
                    silence_counter = 0
                if silence_counter > lift_samples:
                    sample = i-silence_counter
                    silence_counter = 0
                    break
            if sample:
                sample_counter += sample
                result.append((False, time_sample(start_time, sample_counter, sample_rate)))
            else:
                break
        else:
            sample = None
            for i in range(len(db_waveform)):
                if db_waveform[i] > volume_threshold:
                    sample = i
                    break
            if sample:
                sample_counter += sample
                result.append((True, time_sample(start_time, sample_counter, sample_rate)))
            else:
                break
        try:
            db_waveform = db_waveform[sample:]
        except IndexError:
            db_waveform = []
        if len(result):
            last_onset = result[-1]
    # Debug:
    if len(result):
        f = wave.open("out_"+str(wav_counter)+'.wav', 'w')
        f.setparams((1, 2, sample_rate, 0, 'NONE', 'not compressed'))
        assert max(waveform) <= 127.0
        assert min(waveform) >= -128.0
        values = [struct.pack('h', v*(2**7.5)) for v in waveform]
        value_str = ''.join(values)
        f.writeframes(value_str)
        f.close()
        wav_counter += 1

    return result, silence_counter


def to_db(number, sample_size_in_bits):
    if number == 0:
        return float('-inf')
    else:
        number = float(number)
    cap = 2**(sample_size_in_bits-1)
    if number > 0:
        cap -= 1
    else:
        cap *= -1
    db = 20*math.log10(number/cap)
    return db


def time_sample(start_time, samples, sample_rate=SAMPLE_RATE):
    return start_time + sample_time(samples, sample_rate)


def sample_time(samples, sample_rate=SAMPLE_RATE):
    return float(samples) / sample_rate


if __name__ == '__main__':
    main()
