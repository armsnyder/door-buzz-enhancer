__author__ = 'Adam Snyder'

import unittest
import os
import scipy.io.wavfile

import door_buzz_enhancer
import door_buzz_simple


class Test(unittest.TestCase):
    def test_get_sound(self):
        milliseconds = 100
        actual, _ = door_buzz_enhancer.get_sound(milliseconds)
        found_non_zero = False
        for bit in actual:
            if bit != 0:
                found_non_zero = True
                break
        self.assertTrue(found_non_zero)

    def test_distance(self):
        in_a = ([1, 2, 3, 4, 5], 0)
        in_b = ([-2, 7, 11, -9], 1)
        expected = 3+5+8+13
        actual_a = door_buzz_enhancer.get_sound_distance(in_a, in_b)
        actual_b = door_buzz_enhancer.get_sound_distance(in_b, in_a)
        self.assertEqual(actual_a[0], actual_b[0])
        self.assertEqual(actual_a[1], actual_b[1]*-1)
        self.assertEqual(expected, actual_b[0])
        self.assertEqual(1, actual_b[1])

    # def test_stimuli(self):
    #     def run_file(file_name, source_fingerprint_2):
    #         sr_2, sample = scipy.io.wavfile.read(file_name)
    #         num_samples = int(door_buzz_enhancer.WINDOW_SIZE * 1.0 / 1000.0 * sr_2)
    #         for i in range(0, len(sample)-num_samples, num_samples):
    #             subsample = sample[i:i+num_samples]
    #             subsample_fingerprint = door_buzz_enhancer.fingerprint_sound(subsample, sr_2)
    #             if door_buzz_enhancer.match(source_fingerprint_2, subsample_fingerprint):
    #                 return True, i
    #         return False, 0
    #
    #     source_stimuli = []
    #     for (_, _, file_names) in os.walk('source_stimuli'):
    #         source_stimuli.extend(file_names)
    #     source_stimuli = [str(x).split('.')[0] for x in source_stimuli if len(x) > 0 and x[0] != '.']
    #
    #     sample_stimuli = []
    #     for (_, _, file_names) in os.walk('sample_stimuli'):
    #         sample_stimuli.extend(file_names)
    #     sample_stimuli = [x for x in sample_stimuli if len(x) > 0 and x[0] != '.']
    #
    #     for source_stimulus in source_stimuli:
    #         sr, source_stimulus_array = scipy.io.wavfile.read('source_stimuli/'+source_stimulus+'.wav')
    #         self.assertEqual(48000, sr)
    #         source_fingerprint = door_buzz_enhancer.fingerprint_sound(source_stimulus_array, sr)
    #         pos_list = []
    #         neut_list = []
    #         for sample_stimulus in sample_stimuli:
    #             if source_stimulus in sample_stimulus:
    #                 pos_list.append(sample_stimulus)
    #             else:
    #                 neut_list.append(sample_stimulus)
    #         for pos in pos_list:
    #             result, sample_num = run_file('sample_stimuli/'+pos, source_fingerprint)
    #             self.assertTrue(result, 'False negative: '+pos)
    #         for neut in neut_list:
    #             result, sample_num = run_file('sample_stimuli/'+neut, source_fingerprint)
    #             if result:
    #                 print 'WARNING: False positive on '+source_stimulus+': '+neut+' at sample #'+str(sample_num)

    def test_onset_detect(self):
        sr, waveform = scipy.io.wavfile.read('sample_stimuli/posA_0.wav')
        actual, _ = door_buzz_simple.detect_onsets(waveform.tolist(), -16, sr, 16)
        self.assertEqual(2, len(actual))
        self.assertTrue(actual[0][0])
        self.assertFalse(actual[1][0])
        self.assertAlmostEqual(door_buzz_simple.time_sample(0, 62313, sr), actual[0][1], 3)
        self.assertAlmostEqual(door_buzz_simple.time_sample(0, 78175, sr), actual[1][1], 3)

    def test_onset_with_chunk(self):
        sr, waveform = scipy.io.wavfile.read('misc/tapping.wav')
        waveform = waveform.tolist()
        chunk_size = 1024
        actual = []
        start_time = 0.0
        sc = 0
        while len(waveform) > chunk_size:
            if len(actual):
                last_onset = actual[-1]
            else:
                last_onset = None
            onsets, sc = door_buzz_simple.detect_onsets(waveform[:chunk_size], -18, sr, 16, 200, start_time,
                                                        last_onset, sc)
            actual.extend(onsets)
            waveform = waveform[chunk_size:]
            start_time = door_buzz_simple.time_sample(start_time, chunk_size, sr)
        self.assertEqual(2, len(actual))
        self.assertTrue(actual[0][0])
        self.assertFalse(actual[1][0])
        self.assertAlmostEqual(door_buzz_simple.time_sample(0, 29360, sr), actual[0][1], 3)
        self.assertAlmostEqual(door_buzz_simple.time_sample(0, 132700, sr), actual[1][1], 3)

    def test_to_db(self):
        self.assertEqual(float('-inf'), door_buzz_simple.to_db(0, 8))
        self.assertEqual(0, door_buzz_simple.to_db(127, 8))
        self.assertEqual(0, door_buzz_simple.to_db(-128, 8))
