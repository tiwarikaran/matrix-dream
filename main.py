import json
import sys
import time

import requests

MODELS = [
    "moondream",
]

PROMPT = "Describe this image in detail. Cover the main subjects, colors, background, and any notable elements."

OLLAMA_URL = "http://localhost:11434/api/generate"


def encode_image(image_path: str) -> str:
    import base64

    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def run_model(model: str, image_b64: str) -> float:
    print(f"\n{'=' * 60}")
    print(f"  Model: {model}")
    print(f"{'=' * 60}")

    payload = {
        "model": model,
        "prompt": PROMPT,
        "images": [image_b64],
        "stream": True,
    }

    start = time.time()

    try:
        with requests.post(OLLAMA_URL, json=payload, stream=True) as resp:
            resp.raise_for_status()
            for line in resp.iter_lines():
                if not line:
                    continue
                chunk = json.loads(line)
                token = chunk.get("response", "")
                print(token, end="", flush=True)
                if chunk.get("done"):
                    break
    except requests.exceptions.ConnectionError:
        print("[ERROR] Could not connect to Ollama. Is it running? Try: ollama serve")
        return -1
    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] HTTP error: {e}. Is the model pulled? Try: ollama pull {model}")
        return -1
    except Exception as e:
        print(f"[ERROR] {e}")
        return -1

    elapsed = time.time() - start
    print(f"\n\n  Time: {elapsed:.2f}s")
    return elapsed


def print_summary(results: list[tuple[str, float]]):
    print(f"\n{'=' * 60}")
    print(f"  Summary")
    print(f"{'=' * 60}")
    print(f"  {'Model':<30} {'Time':>10}")
    print(f"  {'-' * 30} {'-' * 10}")

    sorted_results = sorted([(m, t) for m, t in results if t >= 0], key=lambda x: x[1])
    failed = [(m, t) for m, t in results if t < 0]

    for model, elapsed in sorted_results:
        print(f"  {model:<30} {elapsed:>9.2f}s")
    for model, _ in failed:
        print(f"  {model:<30} {'FAILED':>10}")

    print(f"{'=' * 60}\n")


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <image_path>")
        print("Example: python main.py test.jpg")
        sys.exit(1)

    image_path = sys.argv[1]

    try:
        image_b64 = encode_image(image_path)
    except FileNotFoundError:
        print(f"[ERROR] Image not found: {image_path}")
        sys.exit(1)

    print(f"\nImage: {image_path}")
    print(f"Prompt: {PROMPT}")
    print(f"Models: {', '.join(MODELS)}")

    results = []
    for model in MODELS:
        elapsed = run_model(model, image_b64)
        results.append((model, elapsed))

    print_summary(results)


if __name__ == "__main__":
    main()
