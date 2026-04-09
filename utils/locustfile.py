import os
import random
from locust import HttpUser, task, between, events
from dotenv import load_dotenv

# Load environment variables (API_KEY)
load_dotenv()

# Check for API key at start
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    print("Warning: API_KEY not found in environment variables. Ensure .env is set properly.")

# Sample texts for variety to emulate realistic inferences
SAMPLE_TEXTS = [
    "The API layer makes this incredibly efficient.",
    "Welcome to the load testing suite for our text to speech engine.",
    "This is a longer sentence intended to test how the model handles a bit more content.",
    "Short burst.",
    "Testing testing one two three.",
    "This model performs extremely well under concurrent loads."
]

VOICES = [
    "af_heart", 
    "bm_george"
]

class TTSUser(HttpUser):
    # Simulates a user waiting 1 to 5 seconds before making the next request
    wait_time = between(1, 5)

    # @task(1)
    # def check_ping(self):
    #     """
    #     A low-weight task to verify the endpoint is alive.
    #     """
    #     headers = {
    #         "Authorization": f"Bearer {API_KEY}"
    #     }
    #     # self.client automatically prefixes the path with the `--host` CLI parameter
    #     self.client.get("/ping", headers=headers, name="/ping")

    @task
    def test_tts_inference(self):
        """
        A high-weight task that generates speech using the Kokoro API endpoint.
        """
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "text": random.choice(SAMPLE_TEXTS),
            "voice": random.choice(VOICES),
            "speed": 1.0
        }

        # Submitting the request. It can take tens of seconds depending on queue & hardware.
        # We specify the name parameter so Locust aggregates stats cleanly.
        with self.client.post("/v1/audio/speech", json=payload, headers=headers, name="/v1/audio/speech", catch_response=True, timeout=120) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Failed with status {response.status_code}: {response.text[:100]}")

@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    print("====================================")
    print("Starting load test...")
    if environment.host:
        print(f"Target host: {environment.host}")
    else:
        print("Warning: No --host flag specified. You can configure it in the Locust Web UI.")
    print("For a max 5 users test, configure 5 peak concurrency in the Locust UI.")
    print("====================================")
