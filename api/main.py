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
    # WebDriverの設定とURL処理
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # キャッシュディレクトリを/tmpに指定
    service = Service(ChromeDriverManager(cache_valid_range=7, path="/tmp").install())

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    title = driver.title
    driver.quit()
    return {"title": title}

if __name__ == "__main__":
    app.run(debug=True)
