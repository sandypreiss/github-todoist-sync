#!/bin/bash

SCRIPT_PATH="src/github_todoist_sync/main.py"
LOG_FILE="logs/github_todoist_sync.log"
LOG_DIR=$(dirname "$LOG_FILE")

# Create log directory and file with appropriate permissions if they don't exist
if [ ! -d "$LOG_DIR" ]; then
  mkdir -p "$LOG_DIR"
  chmod +rw "$LOG_DIR"
fi

if [ ! -f "$LOG_FILE" ]; then
  touch "$LOG_FILE"
  chmod +rw "$LOG_FILE"
fi

timestamp() {
  date +"%Y-%m-%d %H:%M:%S"
}

echo "=== Sync started at $(timestamp) ===" >> $LOG_FILE
uv run $SCRIPT_PATH >> $LOG_FILE
echo "=== Sync completed at $(timestamp) ===" >> $LOG_FILE
echo "" >> $LOG_FILE