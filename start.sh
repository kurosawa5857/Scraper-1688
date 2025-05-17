import os
from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, Render!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Renderが環境変数でPORTを指定してくる
    app.run(host="0.0.0.0", port=port)
