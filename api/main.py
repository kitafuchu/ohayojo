from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process_url():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400

    try:
        result = selenium_process(url)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success", "data": result})

def selenium_process(url):
    # WebDriverの設定
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # ヘッドレスモード
    options.add_argument("--no-sandbox")  # サンドボックス無効化
    options.add_argument("--disable-dev-shm-usage")  # /dev/shmの共有メモリ制限対応
    options.add_argument("--disable-gpu")  # GPU無効化（必要に応じて）
    options.add_argument("--remote-allow-origins=*")  # オリジンエラー対応

    # ドライバを/tmpに保存
    service = Service(ChromeDriverManager(path="/tmp").install())

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    title = driver.title
    driver.quit()
    return {"title": title}

if __name__ == "__main__":
    app.run(debug=True)
