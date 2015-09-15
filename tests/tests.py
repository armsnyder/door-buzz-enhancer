__author__ = 'Adam Snyder'

import unittest
import os
import scipy.io.wavfile

import door_buzz_enhancer


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

    def test_stimuli(self):
        def run_file(file_name, source_fingerprint_2):
            sr_2, sample = scipy.io.wavfile.read(file_name)
            num_samples = int(door_buzz_enhancer.WINDOW_SIZE * 1.0 / 1000.0 * sr_2)
            for i in range(0, len(sample)-num_samples, num_samples):
                subsample = sample[i:i+num_samples]
                subsample_fingerprint = door_buzz_enhancer.fingerprint_sound(subsample, sr_2)
                if door_buzz_enhancer.match(source_fingerprint_2, subsample_fingerprint):
                    return True, i
            return False, 0

        source_stimuli = []
        for (_, _, file_names) in os.walk('source_stimuli'):
            source_stimuli.extend(file_names)
        source_stimuli = [str(x).split('.')[0] for x in source_stimuli if len(x) > 0 and x[0] != '.']

        sample_stimuli = []
        for (_, _, file_names) in os.walk('sample_stimuli'):
            sample_stimuli.extend(file_names)
        sample_stimuli = [x for x in sample_stimuli if len(x) > 0 and x[0] != '.']

        for source_stimulus in source_stimuli:
            sr, source_stimulus_array = scipy.io.wavfile.read('source_stimuli/'+source_stimulus+'.wav')
            self.assertEqual(48000, sr)
            source_fingerprint = door_buzz_enhancer.fingerprint_sound(source_stimulus_array, sr)
            pos_list = []
            neut_list = []
            for sample_stimulus in sample_stimuli:
                if source_stimulus in sample_stimulus:
                    pos_list.append(sample_stimulus)
                else:
                    neut_list.append(sample_stimulus)
            for pos in pos_list:
                result, sample_num = run_file('sample_stimuli/'+pos, source_fingerprint)
                self.assertTrue(result, 'False negative: '+pos)
            for neut in neut_list:
                result, sample_num = run_file('sample_stimuli/'+neut, source_fingerprint)
                if result:
                    print 'WARNING: False positive on '+source_stimulus+': '+neut+' at sample #'+str(sample_num)
