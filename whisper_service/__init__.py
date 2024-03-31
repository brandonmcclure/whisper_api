import gradio as gr
import argparse
import speech_recognition as sr
import numpy as np
import io
import os
import soundfile as sf
import sys
import torch
import mymod
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s || %(levelname)s || %(name)s.%(funcName)s:%(lineno)d || %(message)s')

parser = argparse.ArgumentParser(description='Basic Whisper API server')
parser.add_argument(
    '-m', '--model', default=os.environ.get('WHISPER_SERVICE_MODEL','small.en'),
    help='The open AI whisper model to use to detect speech')
parser.add_argument(
    '--cpu', action="store_true",
    help='If true, this will allow the program to run on a CPU instead of your GPU using CUDA')
args = parser.parse_args()

if(not args.cpu and not torch.cuda.is_available()):
    logging.info('No cuda, bye')
    sys.exit()

with gr.Blocks(analytics_enabled=False) as grBlock:
    gr.Markdown(
        """
        # Local Whisper STT

        Upload a .mp3 or .wav file and press the button to convert it to text.
        """)
    audio_object = gr.Audio(label="Speech")
    output_text = gr.Textbox(label="Text")
    model = gr.Dropdown(info="The bigger the model the more VRAM you need. It will generally be slower and more accurate though", label="Whisper Model",choices=["tiny","tiny.en","base","base.en","small","small.en","medium",  "medium.en", "large"], value=args.model)
    btn = gr.Button("Convert Speech to text")
    btn.click(fn=mymod.performSTT, inputs=[audio_object,model], outputs=[output_text])
grBlock.queue(max_size=10)
grBlock.launch(server_name = '0.0.0.0', server_port = 7861)   