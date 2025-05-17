#!/usr/bin/env bash
pip install --upgrade pip
pip install playwright

# Playwrightブラウザキャッシュが消えていても再インストール
if [ ! -f /opt/render/.cache/ms-playwright/chromium-*/*/chrome-linux/headless_shell ]; then
  echo ">>> Chromium not found. Installing again..."
  python -m playwright install chromium
else
  echo ">>> Chromium already present."
fi
