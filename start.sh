#!/usr/bin/env bash
echo ">>> Installing Chromium..."
python -m playwright install chromium

echo ">>> Starting Flask app"
python app.py
