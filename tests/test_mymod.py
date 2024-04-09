import unittest
import io
import numpy
from scipy.io.wavfile import read
from mymod import perform_stt
class Testperform_stt(unittest.TestCase): 
    
    # Do a test that we can perform STT on an example wav file    
    def test_perform_stt_valid_input(self):
        valid_wav = read("./tests/mary_had_a_lamb.wav")
        valid_wav_as_array = numpy.array(valid_wav[1],dtype=float)    
        output = perform_stt(valid_wav,'small.en')

        self.assertEqual(output,'I want to make sure that you have a good time. I want to make sure that you have a good time. I want to make sure that you have a good time. I want to make sure that you have a good time. I want to make sure that you have a good time.')

if __name__ == '__main__':
    unittest.main()