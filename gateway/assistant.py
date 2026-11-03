"""Opt-in local text assistant adapter (Ollama only; no device-side speech).

Nothing runs unless an explicit --ollama-model is supplied. The endpoint is
restricted to a fixed loopback destination, preventing arbitrary proxy access.
Model output is returned as text, never executed as a hardware command.
"""
import json
from urllib.request import Request, urlopen


class LocalAssistant:
    def __init__(self, model: str):
        if not model or len(model) > 100:
            raise ValueError("Ollama model must be 1..100 characters")
        self.model = model

    def respond(self, text: str) -> str:
        text = text.strip()
        if not 1 <= len(text) <= 300:
            raise ValueError("text must be 1..300 characters")
        payload = {
            "model": self.model,
            "prompt": "You are Open Mochi, a friendly concise animated prototype. "
                      "Respond naturally in at most 35 words. Never claim to control hardware "
                      "or disclose capabilities you do not have. User: " + text,
            "stream": False,
            "options": {"num_predict": 100},
        }
        request = Request("http://127.0.0.1:11434/api/generate",
                          data=json.dumps(payload).encode(),
                          headers={"Content-Type": "application/json"}, method="POST")
        with urlopen(request, timeout=45) as response:
            body = json.loads(response.read(131072))
        return str(body.get("response", ""))[:1000]
