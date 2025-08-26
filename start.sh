#!/bin/bash
apt-get update -y
apt-get install -y ffmpeg
pip install -r requirements.txt
python3 bot.py
