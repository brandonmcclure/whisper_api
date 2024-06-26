import unittest
import io
import numpy
from scipy.io.wavfile import read
from mymod import perform_stt
class test_perform_stt(unittest.TestCase): 
    
    # Do a test that we can perform STT on an example wav file    
    def test_perform_stt_valid_input(self):
        valid_wav = read("./tests/mary_had_a_lamb.wav")
        output = perform_stt(valid_wav,'small.en')

        self.assertEqual(output,'I want to make sure that you have a good time. I want to make sure that you have a good time. I want to make sure that you have a good time. I want to make sure that you have a good time. I want to make sure that you have a good time.')

if __name__ == '__main__':
    unittest.main()