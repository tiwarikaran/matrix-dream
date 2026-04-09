#!/bin/bash
# Stop the moondream watcher

PID_FILE="/Users/ktay/Desktop/test/watcher.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if kill "$PID" 2>/dev/null; then
        echo "Watcher stopped (PID: $PID)"
        rm "$PID_FILE"
    else
        echo "Process not found, cleaning up PID file"
        rm "$PID_FILE"
    fi
else
    # Try to find and kill by process name
    pkill -f "moondream_watcher.py" && echo "Watcher stopped" || echo "Watcher not running"
fi
