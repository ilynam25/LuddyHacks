import asyncio
from flask import Flask, request, jsonify, make_response
from gemini_api.gemini_api import get_bot_response

app = Flask(__name__)

# ✅ Explicit CORS preflight route
@app.route("/process", methods=["OPTIONS"])
def cors_preflight():
    print("🌐 Handling OPTIONS preflight request")
    response = make_response('', 204)
    response.headers["Access-Control-Allow-Origin"] = "https://msde-7.github.io"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "POST,OPTIONS"
    return response

# ✅ Main POST route
@app.route("/process", methods=["POST"])
def process_text():
    try:
        data = request.get_json()
        text = data.get("text")
        state = data.get("state")

        if not text or not state:
            response = jsonify({"error": "Missing 'text' or 'state'"})
            response.headers["Access-Control-Allow-Origin"] = "https://msde-7.github.io"
            response.headers["Access-Control-Allow-Credentials"] = "true"
            return response, 400

        print(f"📥 Received POST: text='{text}', state='{state}'")
        ret_text, ret_state = asyncio.run(get_bot_response(text, state))

        response = jsonify({
            "result": {
                "text": ret_text,
                "state": ret_state
            }
        })
        response.headers["Access-Control-Allow-Origin"] = "https://msde-7.github.io"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response

    except Exception as e:
        print("🔥 ERROR:", str(e))
        response = jsonify({"error": "Server error", "details": str(e)})
        response.headers["Access-Control-Allow-Origin"] = "https://msde-7.github.io"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        return response, 500

if __name__ == "__main__":
    app.run()
