import runpod
from kokoro import KPipeline
import numpy as np
import soundfile as sf
import io
import base64
import torch

# ---------------------------------------------------
# Device setup (GPU if available)
# ---------------------------------------------------
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"[INIT] Using device: {DEVICE}")

# ---------------------------------------------------
# Load model once (important for performance)
# ---------------------------------------------------
try:
    pipeline = KPipeline(
        lang_code='a',
        repo_id='hexgrad/Kokoro-82M'  # avoids warning
    )
    print("[INIT] Kokoro model loaded successfully")
except Exception as e:
    print(f"[INIT ERROR] Failed to load model: {e}")
    raise e


# ---------------------------------------------------
# Handler function (Runpod entrypoint)
# ---------------------------------------------------
def handler(job):
    try:
        input_data = job.get("input", {})

        text = input_data.get("text", "Hello from Runpod")
        voice = input_data.get("voice", "af_heart")

        print(f"[JOB] Processing text: {text[:50]}... | voice: {voice}")

        # ---------------------------------------------------
        # Generate audio
        # ---------------------------------------------------
        generator = pipeline(text, voice=voice)

        audio_chunks = []
        for _, _, audio in generator:
            audio_chunks.append(audio)

        if not audio_chunks:
            return {"error": "No audio generated"}

        full_audio = np.concatenate(audio_chunks)

        # ---------------------------------------------------
        # Convert to WAV (in-memory)
        # ---------------------------------------------------
        buffer = io.BytesIO()
        sf.write(buffer, full_audio, 24000, format="WAV")
        buffer.seek(0)

        audio_base64 = base64.b64encode(buffer.read()).decode()

        print("[JOB] Audio generated successfully")

        return {
            "audio": audio_base64,
            "sample_rate": 24000
        }

    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return {"error": str(e)}


# ---------------------------------------------------
# Start Runpod serverless worker
# ---------------------------------------------------
runpod.serverless.start({"handler": handler})
