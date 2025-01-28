from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/process", methods=["POST"])
def process_url():
    data = request.json
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL is required"}), 400

    # シンプルな処理: 入力されたURLをそのまま返す
    return jsonify({"status": "success", "received_url": url})

if __name__ == "__main__":
    app.run(debug=True)
