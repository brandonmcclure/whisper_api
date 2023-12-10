import gradio as gr
import argparse
import speech_recognition as sr
import numpy as np
import io
import os
import soundfile as sf
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s || %(levelname)s || %(name)s.%(funcName)s:%(lineno)d || %(message)s')

parser = argparse.ArgumentParser(description='Basic Whisper API server')
parser.add_argument(
    '-m', '--model', default=os.environ.get('WHISPER_SERVICE_MODEL','small.en'),
    help='The open AI whisper model to use to detect speech')

args = parser.parse_args()

r = sr.Recognizer()

def performSTT(audio, state=""):
    logging.info(audio)
    logging.info(audio[1])
    audio_bytes = audio[1].tobytes()
    audio_array = np.frombuffer(audio_bytes, dtype=np.int16)
    with io.BytesIO() as wav_io:
        with sf.SoundFile(wav_io, mode='w', format='wav', samplerate=audio[0], channels=1) as file:
            file.write(audio_array)
        wav_io.seek(0)
        with sr.AudioFile(wav_io) as source:
            audio_data = r.record(source)

    state += r.recognize_whisper(audio_data, model=args.model).strip() + " "
    return state, state
with gr.Blocks(analytics_enabled=False) as grBlock:
    state = gr.State(value="")
    gr.Markdown(
        """
        # Local Whisper STT

        Upload a .mp3 or .wav file and press the button to convert it to text.
        """)
    audio_object = gr.Audio(label="Speech", streaming=True)
    textbox = gr.Textbox()
    audio_object.stream(
            fn=performSTT,
            inputs=[audio_object, state],
            outputs=[textbox, state]
        )
    # output_text = gr.Textbox(label="Text")
    # btn = gr.Button("Convert Speech to text")
    # btn.click(fn=performSTT, inputs=[audio_object], outputs=[output_text])
grBlock.launch(server_name = '0.0.0.0', server_port = 7861)   