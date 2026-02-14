import io
import os

import numpy as np
import soundfile as sf
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from kokoro import KPipeline
from pydantic import BaseModel

print("Loading Kokoro Model... please wait.")
# lang_code='a' is American English.
pipeline = KPipeline(lang_code="a")
print("Model Loaded! System ready.")


def generate_audio_numpy(text, voice, speed):
    """
    Helper function used by both API and UI.
    Returns: (sample_rate, audio_numpy_array)
    """
    generator = pipeline(text, voice=voice, speed=speed, split_pattern=r"\n+")
    all_audio = []
    for _, _, audio in generator:
        all_audio.append(audio)

    if not all_audio:
        return None

    return 24000, np.concatenate(all_audio)


app = FastAPI(title="Kokoro TTS API")


class TTSRequest(BaseModel):
    text: str
    voice: str = "af_heart"
    speed: float = 1.0


@app.post("/v1/audio/speech")
async def api_generate_audio(request: TTSRequest):
    result = generate_audio_numpy(request.text, request.voice, request.speed)
    if not result:
        raise HTTPException(status_code=500, detail="No audio generated")

    sample_rate, audio_data = result

    # Convert to WAV in-memory
    buffer = io.BytesIO()
    sf.write(buffer, audio_data, sample_rate, format="WAV")
    buffer.seek(0)
    return Response(content=buffer.read(), media_type="audio/wav")


# Health check endpoint; required for Runpod to monitor worker health
@app.get("/ping")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 80))
    uvicorn.run(app, host="0.0.0.0", port=port)
