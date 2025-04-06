import asyncio
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from gemini_api.gemini_api import get_bot_response

app = Flask(__name__)

# ✅ Allow all origins dynamically and support credentials
CORS(app, supports_credentials=True)

@app.after_request
def apply_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = request.headers.get("Origin", "*")
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return response

@app.route("/process", methods=["POST", "OPTIONS"])
def process_text():
    if request.method == "OPTIONS":
        return make_response(jsonify({"message": "CORS preflight OK"}), 200)

    data = request.get_json()
    text = data.get("text")
    state = data.get("state")

    if not text or not state:
        return jsonify({"error": "Missing 'text' or 'state'"}), 400

    print(f"📥 Received POST: text='{text}', state='{state}'")

    ret_text, ret_state = asyncio.run(get_bot_response(text, state))

    return jsonify({
        "result": {
            "text": ret_text,
            "state": ret_state
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
