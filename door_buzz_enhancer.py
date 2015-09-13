__author__ = 'Adam Snyder'

import librosa
import pyaudio
import datetime


def main():
    sample_size = 1000
    similarity_threshold = 0.1
    buzz_cooldown = 10000
    last_buzz = datetime.datetime.now()
    while True:
        sound_sample = get_sound(sample_size)
        sample_fingerprint = fingerprint_sound(sound_sample)
        reference_fingerprint = get_reference_fingerprint()
        distance = get_sound_distance(sample_fingerprint, reference_fingerprint)
        if distance < similarity_threshold:
            now = datetime.datetime.now()
            if now - last_buzz > buzz_cooldown:
                buzz()
            last_buzz = now

def get_sound(milliseconds):
    """
    Gets an array representation on the waveform from the computer's microphone input
    :param milliseconds: length to listen for
    :return: waveform, sample rate
    """
    return [0, 0, 0, 0]

def fingerprint_sound(waveform):
    """
    Interprets a sound and returns a comparable value
    :param waveform: sound to process
    :return: fingerprint of sound
    """
    return [0, 0, 0, 0]

def get_sound_distance(fingerprint_a, fingerprint_b):
    """
    Calculates the distance (difference) between two sound fingerprints
    :param fingerprint_a:
    :param fingerprint_b:
    :return: value between 0 and 1 -- closer to 0 means more similar
    """
    return 0.5

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
    print "BUZZ!"

if __name__ == '__main__':
    main()
