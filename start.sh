#!/usr/bin/env bash
# Chromium（Playwright用ブラウザ）を起動時にインストール
python -m playwright install chromium

# Flaskアプリを起動
python app.py
