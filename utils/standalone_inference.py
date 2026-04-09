import numpy as np
import soundfile as sf
from kokoro import KPipeline

pipeline = KPipeline(lang_code="a")


def convert_text_to_speech(text, voice="af_heart"):
    generator = pipeline(text, voice=voice, speed=1, split_pattern=r"\n+")
    all_audio = []
    for _, _, audio in generator:
        all_audio.append(audio)

    if not all_audio:
        raise Exception(status_code=400, detail="No audio generated")

    final_audio = np.concatenate(all_audio)
    return final_audio


if __name__ == "__main__":
    audio = convert_text_to_speech("This is sample text for testing.")
    sf.write("output.wav", audio, 16000)
    print("Audio saved to output.wav")
