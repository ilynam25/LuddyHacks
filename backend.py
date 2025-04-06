import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS
from gemini_api.gemini_api import get_bot_response

app = Flask(__name__)

# Allow specific origin (your frontend on port 5173)
CORS(app, origins=lambda origin: True, supports_credentials=True)

@app.route("/process", methods=["POST", "OPTIONS"])
@app.route("/process", methods=["POST", "OPTIONS"])
def process_text():
    if request.method == "OPTIONS":
        response = app.make_default_options_response()
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:5173")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    data = request.get_json()
    text = data.get("text")
    state = data.get("state")

    if not text or not state:
        return jsonify({"error": "Missing 'text' or 'state'"}), 400

    ret_text, ret_state = asyncio.run(get_bot_response(text, state))  # <== Fix here
    return jsonify({"result": {
        "text": ret_text,
        "state": ret_state
    }})

def your_method(text, state):
    return f"Received: '{text}' with state '{state}'"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

