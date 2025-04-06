import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS
from gemini_api.gemini_api import get_bot_response

app = Flask(__name__)

# ✅ Enable CORS for all origins (dev-safe with credentials)
CORS(app, origins=lambda origin: True, supports_credentials=True)

@app.route("/process", methods=["POST"])
def process_text():
    data = request.get_json()
    text = data.get("text")
    state = data.get("state")

    if not text or not state:
        return jsonify({"error": "Missing 'text' or 'state'"}), 400

    print(f"📥 Received POST: text='{text}', state='{state}'")

    ret_text, ret_state = asyncio.run(get_bot_response(text, state))

    return jsonify({"result": {
        "text": ret_text,
        "state": ret_state
    }})

def your_method(text, state):
    return f"Received: '{text}' with state '{state}'"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
