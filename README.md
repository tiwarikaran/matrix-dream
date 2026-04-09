# Moondream Image Watcher

A folder watcher that automatically sends new images to the local [Ollama](https://ollama.com/) moondream model for AI-powered description generation.

## Features

- **Real-time monitoring** - Watches a folder for new images (jpg, jpeg, png, gif, webp)
- **Smart resizing** - Automatically resizes large images to 1024px max before sending to Ollama (saves bandwidth, maintains quality)
- **Automatic descriptions** - Saves AI-generated descriptions as `.txt` files beside each image
- **Duplicate protection** - Skips images that already have descriptions
- **Background operation** - Runs continuously as a background process

## Requirements

- Python 3.8+
- [Ollama](https://ollama.com/) running locally with the `moondream` model installed
- macOS/Linux (uses shell scripts for process management)

## Setup

1. **Install dependencies:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install watchdog requests Pillow
   ```

2. **Install Ollama and moondream model:**
   ```bash
   # Install Ollama from https://ollama.com
   ollama pull moondream
   ```

3. **Configure the watch directory:**
   Edit `moondream_watcher.py` and update `WATCH_DIR` if needed (default: `/Users/ktay/Desktop/backup-photus/moondream`)

## Usage

### Start the watcher
```bash
./start_watcher.sh
```

### Check status
```bash
./watcher_status.sh
```

### Stop the watcher
```bash
./stop_watcher.sh
```

### View live logs
```bash
tail -f watcher.log
```

## How it works

1. Drop an image into the watched folder
2. The watcher detects the new file
3. If the image is larger than 1024px, it gets resized (maintaining aspect ratio)
4. The resized image is sent to Ollama's moondream model via API
5. The generated description is saved as a `.txt` file with the same name as the image

## Example File Structure

```
/Users/ktay/Desktop/backup-photus/moondream/
├── concert_photo.jpg           # Original image
├── concert_photo.txt           # Generated description ← NEW!
├── beach_sunset.png
├── beach_sunset.txt
└── family_dinner.webp
```

## Examples

### Starting the watcher

```bash
$ ./start_watcher.sh
Watcher started (PID: 31102)
Logs: /Users/ktay/Desktop/test/watcher.log

Commands:
  ./watcher_status.sh  - Check status
  ./stop_watcher.sh    - Stop watcher
  tail -f watcher.log  - View live logs
```

### Watching in action

Drop an image into the folder:

```bash
cp vacation_photo.jpg /Users/ktay/Desktop/backup-photus/moondream/
```

Watch the logs:

```bash
$ tail -f watcher.log
Watching: /Users/ktay/Desktop/backup-photus/moondream
Supported formats: .jpg, .jpeg, .png, .gif, .webp
Ollama URL: http://127.0.0.1:11434/api/generate

Processing: vacation_photo.jpg
  Resizing 5184x3456 → 1024x682
  Sending to Ollama moondream...
Saved description: vacation_photo.txt
```

### Generated description example

**Input:** `concert_photo.jpg`

**Output:** `concert_photo.txt`
```
The image depicts a band performing on stage, with two men playing musical
instruments and singing into microphones. One man is holding a guitar, while
the other is holding a microphone. The stage is set against a backdrop of a
large metal structure, possibly a tent or a stage curtain, which adds an
industrial feel to the scene.

The musicians are dressed in white shirts and blue jeans, suggesting a
casual and relaxed atmosphere for their performance.
```

### Checking status

```bash
$ ./watcher_status.sh
Watcher is running (PID: 31102)
Recent logs:
  Processing: IMG_20260406_001135424.jpg
    Resizing 3072x4080 → 771x1024
    Sending to Ollama moondream...
  Saved description: IMG_20260406_001135424.txt
```

### Batch processing

The watcher also processes existing images on startup:

```bash
$ ./start_watcher.sh
...
Checking for existing images without descriptions...
Processing: old_photo_1.jpg
  Resizing 4000x3000 → 1024x768
  Sending to Ollama moondream...
Saved description: old_photo_1.txt
Processing: old_photo_2.png
  Image already optimal size: 800x600
  Sending to Ollama moondream...
Saved description: old_photo_2.txt
```

## Configuration

Edit these constants in `moondream_watcher.py`:

| Constant | Default | Description |
|----------|---------|-------------|
| `WATCH_DIR` | `/Users/ktay/Desktop/backup-photus/moondream` | Folder to monitor |
| `OLLAMA_URL` | `http://127.0.0.1:11434/api/generate` | Ollama API endpoint |
| `MODEL` | `moondream` | Ollama model name |
| `max_size` | `1024` | Max pixel dimension for resizing |

## License

MIT
