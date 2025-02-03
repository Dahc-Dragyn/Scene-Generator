import requests
import os
from dotenv import load_dotenv

load_dotenv()

HUGGINGFACE_API_KEY = os.environ.get("HUGGINGFACE_API_KEY")
STABLE_DIFFUSION_ENDPOINT = os.environ.get(
    "STABLE_DIFFUSION_ENDPOINT", "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
)

def test_huggingface_api_connection():
    """Tests the connection to the Hugging Face API endpoint using a simple prompt."""

    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
    payload = {"inputs": "a cat riding a bicycle on the moon, concept art"}  # Simple test prompt

    try:
        response = requests.post(STABLE_DIFFUSION_ENDPOINT, headers=headers, json=payload, timeout=30) 
        response.raise_for_status()  # Raise an exception for bad status codes

        # Check if the response is an image (content type starts with "image/")
        if response.headers.get("Content-Type", "").startswith("image/"):
            print("Test Passed: Successfully connected to Hugging Face API and received an image response.")
            return True
        else:
            print(f"Test Failed: Unexpected response content type: {response.headers.get('Content-Type')}")
            print(f"Response body: {response.content}")  # Print the response body for debugging
            return False

    except requests.exceptions.ConnectionError as e:
        print(f"Test Failed: Connection error: {e}")
        return False
    except requests.exceptions.Timeout as e:
        print(f"Test Failed: Timeout error: {e}")
        return False
    except requests.exceptions.RequestException as e:
        print(f"Test Failed: Request error: {e}")
        print(f"Response status code: {response.status_code}")
        print(f"Response body: {response.content}")  # Print the response body for debugging
        return False
    except Exception as e:
        print(f"Test Failed: An unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    test_huggingface_api_connection()