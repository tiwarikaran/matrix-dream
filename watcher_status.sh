#!/bin/bash
# Check watcher status

if pgrep -f "moondream_watcher.py" > /dev/null; then
    echo "Watcher is running (PID: $(pgrep -f moondream_watcher.py))"
    echo "Recent logs:"
    tail -n 5 /Users/ktay/Desktop/test/watcher.log 2>/dev/null || echo "No logs yet"
else
    echo "Watcher is not running"
fi
