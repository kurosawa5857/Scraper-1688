from flask import Flask, request, render_template_string, send_file
from playwright.sync_api import sync_playwright
from googletrans import Translator
import csv
import time
import re
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<title>Scraper-1688</title>
<h1>1688 商品情報取得ツール（Playwright版）</h1>
<form method=post>
  商品ページのURLを入力してください:<br>
  <input type=text name=url size=100>
  <input type=submit value="取得">
</form>
{% if download_url %}
  <p>CSVダウンロード: <a href="{{ download_url }}">こちら</a></p>
{% endif %}
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    download_url = None
    if request.method == 'POST':
        url = request.form['url']
        if url:
            filename = scrape_1688_with_playwright(url)
            if filename:
                download_url = f"/download/{filename}"
    return render_template_string(HTML_TEMPLATE, download_url=download_url)

@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

def scrape_1688_with_playwright(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=15000, wait_until='load')
        page.wait_for_timeout(5000)  # 5秒待機

        title = page.title()

        try:
            meta_tag = page.locator("meta[name='description']")
            description = meta_tag.first.get_attribute("content") or ""
        except:
            description = ""

        html = page.content()
        image_urls = list(set(re.findall(r'https://cbu01\\.alicdn\\.com/.*?\\.jpg', html)))

        translator = Translator()
        title_ja = translator.translate(title, src='zh-cn', dest='ja').text
        description_ja = translator.translate(description, src='zh-cn', dest='ja').text

        filename = f"1688_output_{int(time.time())}.csv"
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(["商品名", "商品説明", "画像URL1", "画像URL2"])
            writer.writerow([
                title_ja,
                description_ja,
                image_urls[0] if len(image_urls) > 0 else '',
                image_urls[1] if len(image_urls) > 1 else ''
            ])

        browser.close()
        return filename
    
    if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

