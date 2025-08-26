#!/bin/bash
set -e

pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt
pip install imageio[ffmpeg]

python3 bot.py
