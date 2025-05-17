#!/bin/bash
# Flask アプリを起動するためのシェルスクリプト

# Playwright のブラウザをインストール（必要なら）
playwright install

# Flask アプリを起動
python app.py
