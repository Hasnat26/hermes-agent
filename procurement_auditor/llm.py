"""Optional local Ollama adapter.

The auditor does not require this module for deterministic checks. Ollama is
called through its local HTTP endpoint only; no paid API is required.
"""

import json
import urllib.request


def ollama_json(prompt: str, model: str = "qwen3:8b", base_url: str = "http://localhost:11434") -> dict:
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
    }).encode()
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        data = json.loads(response.read().decode("utf-8"))
    return json.loads(data["response"])
