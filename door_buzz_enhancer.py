__author__ = 'Adam Snyder'

import librosa
import pyaudio
import datetime
import numpy
import math
import json
import smtplib


WINDOW_SIZE = 100


def main():
    similarity_threshold = 0.1
    buzz_cooldown = 10000
    last_buzz = datetime.datetime.now()
    while True:
        sound_sample, sr = get_sound(100)
        sample_fingerprint = fingerprint_sound(sound_sample, sr)
        reference_fingerprint = get_reference_fingerprint()
        distance = get_sound_distance(sample_fingerprint, reference_fingerprint)
        if distance < similarity_threshold:
            now = datetime.datetime.now()
            if now - last_buzz > buzz_cooldown:
                buzz()
            last_buzz = now


def get_sound(milliseconds):
    """
    Gets an array representation of the waveform from the computer's microphone input
    :param milliseconds: length to listen for
    :return: waveform, sample rate
    """
    format = pyaudio.paInt16
    channels = 1
    rate = 48000
    chunk = 1024

    audio = pyaudio.PyAudio()
    stream = audio.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)
    v_print('recording...')
    frames = []
    for i in range(int(rate/chunk*((milliseconds*1.0)/1000.0))):
        data = stream.read(chunk)
        frames.append(data)
    v_print('finished_recording')
    stream.stop_stream()
    stream.close()
    audio.terminate()

    decoded = numpy.fromstring(b''.join(frames), 'Float16')
    return decoded, rate


def fingerprint_sound(waveform, sample_rate):
    """
    Interprets a sound and returns a comparable value
    :param waveform: sound to process
    :return: fingerprint of sound
    """
    waveform = numpy.nan_to_num(waveform)
    mfcc = librosa.feature.mfcc(waveform, sample_rate)
    result = []
    for f in mfcc:
        total = 0.0
        for x in f:
            if not math.isnan(x):
                total += x
        total /= len(f)
        result.append(total)
    return result


def get_sound_distance(fingerprint_a, fingerprint_b):
    """
    Calculates the distance (difference) between two sound fingerprints
    :param fingerprint_a:
    :param fingerprint_b:
    :return: value between 0 and 1 -- closer to 0 means more similar
    """
    if len(fingerprint_a) < len(fingerprint_b):
        size = len(fingerprint_a)
    else:
        size = len(fingerprint_b)

    distance = 0.0
    for i in range(size):
        distance += abs(fingerprint_b[i]-fingerprint_a[i])

    return distance

def match(fingerprint_a, fingerprint_b):
    """
    Tests if two fingerprints are identical
    :param fingerprint_a:
    :param fingerprint_b:
    :return: True if the fingerprints match
    """
    threshold = 100
    return get_sound_distance(fingerprint_a, fingerprint_b) < threshold


def get_reference_fingerprint():
    """
    Returns the fingerprint that we are listening for
    :return: reference fingerprint
    """
    return [1, 1, 1, 1]


def buzz():
    """
    Activated when a buzz is detected
    :return:
    """
    message = "BUZZ at "+datetime.datetime.now().strftime('%H:%M:%S')
    v_print(message)
    with open('config.json') as config_file:
        config = json.load(config_file)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(config['login']['username'], config['login']['password'])
    for destination in config['destinations']:
        server.sendmail('Buzzer', destination, 'BUZZ')
    server.close()


def v_print(text):
    debug = True
    if debug:
        print text


if __name__ == '__main__':
    main()
