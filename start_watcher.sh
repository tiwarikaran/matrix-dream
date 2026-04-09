#!/bin/bash
# Start the moondream watcher in the background

cd /Users/ktay/Desktop/test
source venv/bin/activate

# Check if already running
if pgrep -f "moondream_watcher.py" > /dev/null; then
    echo "Watcher is already running"
    exit 1
fi

# Start the watcher with unbuffered output
PYTHONUNBUFFERED=1 nohup python3 -u moondream_watcher.py > /Users/ktay/Desktop/test/watcher.log 2>&1 &

# Save PID
echo $! > /Users/ktay/Desktop/test/watcher.pid
echo "Watcher started (PID: $!)"
echo "Logs: /Users/ktay/Desktop/test/watcher.log"
echo ""
echo "Commands:"
echo "  ./watcher_status.sh  - Check status"
echo "  ./stop_watcher.sh    - Stop watcher"
echo "  tail -f watcher.log  - View live logs"
