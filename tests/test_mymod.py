import unittest
import io
import numpy
from scipy.io.wavfile import read
from mymod import performSTT
class TestPerformSTT(unittest.TestCase): 
    
    # Do a test that we can perform STT on an example wav file    
    def test_perform_stt_valid_input(self):
        validWav = read("./tests/mary_had_a_lamb.wav")
        validWavAsArray = numpy.array(validWav[1],dtype=float)    
        output = performSTT(validWav,'small.en')

        self.assertEqual(output,'I want to make sure that you have a good time. I want to make sure that you have a good time. I want to make sure that you have a good time. I want to make sure that you have a good time. I want to make sure that you have a good time.')

if __name__ == '__main__':
    unittest.main()