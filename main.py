import gradio as gr
import argparse
import speech_recognition as sr
import numpy as np
import io
import pydub
import subprocess
import soundfile as sf
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s || %(levelname)s || %(name)s.%(funcName)s:%(lineno)d || %(message)s')

parser = argparse.ArgumentParser(description='Basic Whisper API server')
parser.add_argument(
    '-m', '--model', default='small.en',
    help='The open AI whisper model to use to detect speech')

args = parser.parse_args()

r = sr.Recognizer()

def downloadYT(url):
    logging.info(f'downloading audio from {url}')
    command = f"yt-dlp -f m4a --write-subs --write-auto-subs -o '/tmp/ytdl' '{url}'"
    result = subprocess.check_output(["/bin/bash", "-c", command]).decode("utf-8").strip().split()
    return performSTT(read('/tmp/ytdl'))

def read(f, normalized=False):

    """audio file to numpy array"""
    a = pydub.AudioSegment.from_file(f)
    y = np.array(a.get_array_of_samples())
    if a.channels == 2:
        y = y.reshape((-1, 2))
    if normalized:
        return a.frame_rate, np.float32(y) / 2**15
    else:
        return a.frame_rate, y
def DecideOnTypeOfInput(audioupload = None,microphone = None,url = None):
    if audioupload != None:
        logging.info('doing audio upload')
        logging.debug(audioupload)
        return performSTT(audioupload)
    if microphone != None:
        logging.info('doing microphone upload')
        logging.debug(microphone)
        return performSTT(microphone)
    if url != None:
        logging.info('doing url upload')
        return downloadYT(url)            
    raise "Must pass either an audio upload, your microphone, or a url"
            
    
def performSTT(audio):
     logging.debug(f'audio: {audio[1]}')
     audio_bytes = audio[1].tobytes()
     expectedDTYpe = audio[1].dtype
     logging.info(f'expected dtype: {expectedDTYpe}')
     audio_array = np.frombuffer(audio_bytes, dtype=expectedDTYpe)
     with io.BytesIO() as wav_io:
         with sf.SoundFile(wav_io, mode='w', format='wav', samplerate=audio[0], channels=1) as file:
             file.write(audio_array)
         wav_io.seek(0)
         with sr.AudioFile(wav_io) as source:
             audio_data = r.record(source)
     return r.recognize_whisper(audio_data, model=args.model).strip()
with gr.Blocks(analytics_enabled=False) as grBlock:
    gr.Markdown(
        """
        # Local Whisper STT

        Can convert English speech to text. Choose to upload a mp3 or other media file, record your microphone, or select a url (still experimental) to download and transcribe.

        Use the tabs at the top to select one way to input the audio, then click the **Convert Speech to text** button below.
        """)
    with gr.Tab("Upload a file"):
        audio_object = gr.Audio(label="Upload a file")
    with gr.Tab("Use your microphone"):
        mic_object = gr.Microphone(label="use your mic", type='numpy')
    with gr.Tab("Download from url"):
        url = gr.Textbox(label="url")
    output_text = gr.Textbox(label="Text")
    btn = gr.Button("Convert Speech to text")
    btn.click(fn=DecideOnTypeOfInput, inputs=[audio_object,mic_object], outputs=[output_text])

grBlock.launch(server_name = '0.0.0.0', server_port = 7862)   