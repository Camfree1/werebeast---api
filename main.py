from flask import Flask, request, jsonify

app = Flask(__name__)

# ----------------------------
# HEALTH CHECK (Render uses this)
# ----------------------------
@app.route("/")
def home():
    return "server is working"

# ----------------------------
# BUBBLE TEST ROUTE
# ----------------------------
@app.route("/generate-video", methods=["POST"])
def generate_video():
    try:
        data = request.get_json()

        # safety in case Bubble sends nothing
        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON received"
            }), 400

        prompt = data.get("prompt", "")

        print("PROMPT RECEIVED:", prompt)

        # TEMP RESPONSE (we connect Veo3 later)
        return jsonify({
            "success": True,
            "message": "Route is working",
            "promptReceived": prompt
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# ----------------------------
# REQUIRED FOR RENDER DEPLOY
# ----------------------------
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
