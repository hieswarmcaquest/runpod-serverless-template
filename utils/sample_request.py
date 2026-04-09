import requests
import numpy as np
import soundfile as sf
import io

# API_URL = "http://localhost:80/v1/audio/speech"
# HOST = "localhost"
HOST = "localhost"
PORT = 80
BASE_URL = f"http://{HOST}:{PORT}"
# BASE_URL = "https://kp8mtvc0stoyc0.api.runpod.ai"
API_URL = f"{BASE_URL}/v1/audio/speech"
HEALTH_URL = f"{BASE_URL}/ping"

def check_health():
    # Health check
    health_url = HEALTH_URL
    response = requests.get(health_url)
    print(response.json())


def convert_text_to_speech_using_api(text: str, voice: str, speed: float):
    """
    Convert text to speech using the Kokoro TTS API.
    
    Args:
        text: The text to convert to speech
        voice: The voice to use (e.g., "af_heart", "bm_george")
        speed: The speed of speech (0.5 to 2.0)
    
    Returns:
        A tuple of (sample_rate, audio_numpy_array) for Gradio audio output
    """
    payload = {
        "text": text,
        "voice": voice,
        "speed": speed
    }
    
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()  # Raise exception for bad status codes
        
        # Convert WAV bytes to numpy array
        audio_buffer = io.BytesIO(response.content)
        audio_data, sample_rate = sf.read(audio_buffer)
        
        return sample_rate, audio_data
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
        return None, None


if __name__ == "__main__":
    # # Test example
    # text = "The API layer makes this incredibly efficient."
    # voice = "bm_george"
    # speed = 1.5
    
    # sample_rate, audio_data = convert_text_to_speech_using_api(text, voice, speed)
    # if audio_data is not None:
    #     # Save to file for testing
    #     sf.write(f"api_output_{voice}.wav", audio_data, sample_rate)
    #     print(f"Audio saved to api_output_{voice}.wav")
    check_health()