#!/bin/bash
set -e  # exit immediately if a command fails

# Install ffmpeg if not already present
if ! command -v ffmpeg >/dev/null 2>&1; then
    apt-get update
    apt-get install -y ffmpeg
fi

# Install Python dependencies
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

# Run the app
python app.py
