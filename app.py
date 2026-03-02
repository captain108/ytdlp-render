import yt_dlp
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# 🔐 Set your API key here or use ENV variable
API_KEY = os.getenv("API_KEY", "pak_MGwYn3e5PnxMO3D6gOMVgSyMWjTCgHSQ")


def get_download_links(url):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "noplaylist": True,
        "ignoreerrors": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        if not info:
            raise Exception("Failed to extract video info")

        title = info.get("title", "Unknown Title")
        formats = info.get("formats", [])

        best_mp4 = None
        best_audio = None

        mp4_formats = [
            f for f in formats
            if f.get("ext") == "mp4"
            and f.get("vcodec") != "none"
            and f.get("acodec") != "none"
        ]

        if mp4_formats:
            best_mp4 = sorted(mp4_formats, key=lambda x: x.get("height", 0))[-1]

        audio_formats = [
            f for f in formats
            if f.get("vcodec") == "none"
            and f.get("acodec") != "none"
        ]

        if audio_formats:
            best_audio = sorted(audio_formats, key=lambda x: x.get("abr", 0))[-1]

        return {
            "title": title,
            "video_url": best_mp4["url"] if best_mp4 else None,
            "audio_url": best_audio["url"] if best_audio else None,
        }


@app.route("/api/anshapi")
def anshapi():
    key = request.args.get("key")
    url = request.args.get("url")

    if key != API_KEY:
        return jsonify({"error": "Invalid API Key"}), 403

    if not url:
        return jsonify({"error": "Missing URL"}), 400

    try:
        data = get_download_links(url)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return jsonify({"status": "API Running"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
