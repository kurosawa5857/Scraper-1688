from flask import Flask, request, render_template_string, send_file
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from googletrans import Translator
import csv
import re
import time
import os

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<title>Scraper-1688</title>
<h1>1688 商品情報取得ツール</h1>
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
            filename = scrape_1688(url)
            if filename:
                download_url = f"/download/{filename}"
    return render_template_string(HTML_TEMPLATE, download_url=download_url)

@app.route('/download/<filename>')
def download(filename):
    return send_file(filename, as_attachment=True)

def scrape_1688(url):
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)

    title = driver.title
    source = driver.page_source
    images = re.findall(r'https://cbu01\\.alicdn\\.com/.*?\\.jpg', source)
    translator = Translator()
    title_ja = translator.translate(title, src='zh-cn', dest='ja').text

    filename = f"1688_output_{int(time.time())}.csv"
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(["商品名", "画像URL1", "画像URL2"])
        writer.writerow([title_ja, images[0] if images else '', images[1] if len(images) > 1 else ''])

    driver.quit()
    return filename

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
