import requests
from django.conf import settings


def generate_with_ollama(prompt):

    try:
        response = requests.post(
            f"{settings.OLLAMA_URL}/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            },
            timeout=90
        )

        response.raise_for_status()

        data = response.json()
        return data.get("response", "").strip()

    except Exception as e:
        print("❌ OLLAMA FAILURE:", e)
        return None
