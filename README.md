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

## Example

```
my_photo.jpg          → my_photo.txt
trip_image.png        → trip_image.txt
vacation_2024.jpg     → vacation_2024.txt
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
