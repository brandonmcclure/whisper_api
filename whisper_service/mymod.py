import logging
import argparse
import speech_recognition as sr
import numpy as np
import io
import os
import soundfile as sf
import sys
import torch

def perform_stt(audio,model):
    r = sr.Recognizer()
    logging.info(audio[1])
    audio_bytes = audio[1].tobytes()
    audio_array = np.frombuffer(audio_bytes, dtype=np.int16)
    with io.BytesIO() as wav_io:
        with sf.SoundFile(wav_io, mode='w', format='wav', samplerate=audio[0], channels=1) as file:
            file.write(audio_array)
        wav_io.seek(0)
        with sr.AudioFile(wav_io) as source:
            audio_data = r.record(source)
    return r.recognize_whisper(audio_data, model=model).strip()