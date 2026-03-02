import subprocess
import os
from flask import Flask, request, jsonify

app = Flask(__name__)
PORT = int(os.environ.get("PORT", 10000))

@app.route("/")
def home():
    return jsonify({"status": "yt-dlp API running"})

@app.route("/stream")
def stream():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    cmd = [
        "yt-dlp",
        "-f", "bestaudio",
        "-g",
        url
    ]

    process = subprocess.run(cmd, capture_output=True, text=True)

    if process.returncode != 0:
        return jsonify({"error": process.stderr}), 500

    return jsonify({"stream_url": process.stdout.strip()})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
