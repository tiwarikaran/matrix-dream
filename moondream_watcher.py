#!/usr/bin/env python3
"""
Folder watcher for /Users/ktay/Desktop/backup-photus/moondream
Monitors for new images and sends them to Ollama moondream model for description.
"""

import os
import sys
import time
import base64
import io
import requests
from pathlib import Path
from PIL import Image
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Configuration
WATCH_DIR = Path("/Users/ktay/Desktop/backup-photus/moondream")
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "moondream"
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}


def encode_image(image_path):
    """Encode image to base64 for Ollama API."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def resize_image_for_ollama(image_path, max_size=1024):
    """
    Resize image to reduce processing time while maintaining quality.
    Moondream internally resizes to ~378x378, so larger images waste bandwidth.
    Returns base64 encoded resized image.
    """
    with Image.open(image_path) as img:
        # Convert to RGB if necessary (handles PNG with transparency, etc.)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')

        # Get current dimensions
        width, height = img.size

        # Only resize if larger than max_size
        if width > max_size or height > max_size:
            # Calculate new dimensions maintaining aspect ratio
            ratio = min(max_size / width, max_size / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)

            print(f"  Resizing {width}x{height} → {new_width}x{new_height}", flush=True)
            img = img.resize((new_width, new_height), Image.LANCZOS)
        else:
            print(f"  Image already optimal size: {width}x{height}", flush=True)

        # Save to buffer as JPEG with good quality
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=90, optimize=True)
        buffer.seek(0)

        return base64.b64encode(buffer.getvalue()).decode("utf-8")


def describe_image(image_path):
    """Send image to Ollama moondream model and return description."""
    try:
        # Resize image before encoding (saves bandwidth and processing time)
        base64_image = resize_image_for_ollama(image_path, max_size=1024)

        payload = {
            "model": MODEL,
            "prompt": "Describe this image in detail.",
            "images": [base64_image],
            "stream": False
        }

        # First request may take time to load the model
        print(f"  Sending to Ollama {MODEL}...", flush=True)
        response = requests.post(OLLAMA_URL, json=payload, timeout=600)
        response.raise_for_status()

        result = response.json()
        return result.get("response", "No description generated")

    except requests.exceptions.ConnectionError:
        return f"Error: Could not connect to Ollama at {OLLAMA_URL}. Is Ollama running?"
    except requests.exceptions.Timeout:
        return "Error: Request to Ollama timed out."
    except Exception as e:
        return f"Error: {str(e)}"


def process_image(image_path):
    """Process a single image and save description."""
    image_path = Path(image_path)

    # Skip non-image files
    if image_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
        return

    # Skip if description already exists
    desc_path = image_path.with_suffix('.txt')
    if desc_path.exists():
        print(f"Skipping (already processed): {image_path.name}", flush=True)
        return

    print(f"Processing: {image_path.name}", flush=True)

    description = describe_image(image_path)

    with open(desc_path, 'w') as f:
        f.write(description)

    print(f"Saved description: {desc_path.name}", flush=True)


class ImageHandler(FileSystemEventHandler):
    """Handler for new image files."""

    def on_created(self, event):
        if event.is_directory:
            return

        # Wait a moment to ensure file is fully written
        time.sleep(0.5)
        process_image(event.src_path)

    def on_modified(self, event):
        # Only process on create, but handle cases where file is moved/renamed
        pass


def process_existing_images():
    """Process any existing images that don't have descriptions yet."""
    for ext in SUPPORTED_EXTENSIONS:
        for image_path in WATCH_DIR.glob(f"*{ext}"):
            desc_path = image_path.with_suffix('.txt')
            if not desc_path.exists():
                process_image(image_path)


def main():
    """Main entry point."""
    if not WATCH_DIR.exists():
        print(f"Error: Directory does not exist: {WATCH_DIR}")
        sys.exit(1)

    print(f"Watching: {WATCH_DIR}", flush=True)
    print(f"Supported formats: {', '.join(SUPPORTED_EXTENSIONS)}", flush=True)
    print(f"Ollama URL: {OLLAMA_URL}", flush=True)
    print("Press Ctrl+C to stop\n", flush=True)

    # Process any existing images first
    print("Checking for existing images without descriptions...", flush=True)
    process_existing_images()

    # Set up the observer
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, str(WATCH_DIR), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping watcher...")
        observer.stop()
    finally:
        observer.join()


if __name__ == "__main__":
    main()
