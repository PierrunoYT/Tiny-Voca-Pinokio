import os
from pathlib import Path

WEIGHTS = Path(__file__).resolve().parent / "weights"
CHECKPOINT = WEIGHTS / "tiny-voca.pt"
# dizione (the phonemizer) reads its data from here; must be set before it is imported.
os.environ.setdefault("DIZIONE_DATA", str(WEIGHTS / "phonemizer"))

import gradio as gr
import torch
from tiny_voca.infer import ENGLISH_ONLY, load_model, match_frontend, speak_text
from tiny_voca.text import NothingToPronounce

SEMITONE = 0.0578  # pitch_shift is added to log F0; ln(2) / 12 is one semitone

match_frontend(CHECKPOINT)
MODEL = load_model(CHECKPOINT)
SAMPLE_RATE = MODEL.config.sample_rate


def generate(text, voice, speed, pitch_semitones, pitch_range):
    if not text or not text.strip():
        raise gr.Error("Enter some text.")
    try:
        with torch.inference_mode():
            wave, _ = speak_text(MODEL, text, voice, speed, pitch_semitones * SEMITONE, pitch_range=pitch_range)
    except NothingToPronounce:
        raise gr.Error(ENGLISH_ONLY)
    except ValueError as error:
        raise gr.Error(str(error))
    return SAMPLE_RATE, wave.numpy()


with gr.Blocks(title="tiny-voca") as demo:
    gr.Markdown("# tiny-voca\n4.5M-parameter English text-to-speech. Two voices: F2 (female), M2 (male).")
    with gr.Row():
        with gr.Column():
            text = gr.Textbox(label="Text", lines=6, value="Hello! This is tiny voca, a small text to speech model.")
            voice = gr.Radio(["F2", "M2"], value="F2", label="Voice")
            speed = gr.Slider(0.5, 2.0, value=1.0, step=0.05, label="Speed")
            pitch = gr.Slider(-12, 12, value=0, step=0.5, label="Pitch shift (semitones)")
            pitch_range = gr.Slider(0.0, 2.0, value=1.0, step=0.05, label="Pitch range")
            button = gr.Button("Generate", variant="primary")
        with gr.Column():
            audio = gr.Audio(label="Speech", type="numpy")
    button.click(generate, [text, voice, speed, pitch, pitch_range], audio, api_name="generate")

demo.queue().launch()
