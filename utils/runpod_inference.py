import requests
import os
import requests
import numpy as np
import soundfile as sf
import io
import time
from dotenv import load_dotenv
load_dotenv()

def check_ping_status(base_url):
    headers = {
        "Authorization": f"Bearer {os.getenv('API_KEY')}",
    }
    response = requests.get(
        f"{base_url}/ping",
        headers=headers
    )
    return response.text


def convert_text_to_speech_using_api(text: str, voice: str, speed: float, base_url:str=None):
    """
    Convert text to speech using the Kokoro TTS API.
    
    Args:
        base_url: The base URL of the API endpoint
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

    headers = {
        "Authorization": f"Bearer {os.getenv('API_KEY')}",
        "Content-Type": "application/json"
    }

    if not base_url:
        base_url = os.getenv('RUNPOD_API_BASE_URL', None)

    API_URL = f"{base_url}/v1/audio/speech"
    start_time = time.time()
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers, timeout=120)
        print(f"API response status code: {response.status_code}")
        response.raise_for_status()  # Raise exception for bad status codes
        print("Total time taken for API call: {:.2f} seconds".format(time.time() - start_time))
        
        # Convert WAV bytes to numpy array
        audio_buffer = io.BytesIO(response.content)
        audio_data, sample_rate = sf.read(audio_buffer)
        
        return sample_rate, audio_data
    except requests.exceptions.RequestException as e:
        print(f"Error calling API: {e}")
        return None, None



if __name__ == "__main__":
    BASE_URL = "https://yfewmsmrx6gtxu.api.runpod.ai"
    text = "The API layer makes this incredibly efficient."
    voice = "bm_george"
    speed = 1.5
    
    sample_rate, audio_data = convert_text_to_speech_using_api(text, voice, speed, BASE_URL)
    if audio_data is not None:
        # Save to file for testing
        sf.write(f"api_output_{voice}.wav", audio_data, sample_rate)
        print(f"Audio saved to api_output_{voice}.wav") 