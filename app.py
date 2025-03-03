from flask import Flask, request, render_template, jsonify, send_file
import yt_dlp
import os

app = Flask(__name__)

# Ensure downloads directory exists
DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/download", methods=["POST"])
def download_video():
    data = request.get_json()  # Ensure the request is JSON
    video_url = data.get("url")

    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    output_path = os.path.join(DOWNLOAD_FOLDER, "video.%(ext)s")

    ydl_opts = {
        "outtmpl": output_path,
        "format": "best"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Find the downloaded file dynamically
        downloaded_file = next(f for f in os.listdir(DOWNLOAD_FOLDER) if f.startswith("video"))

        return jsonify({"file": f"/downloads/{downloaded_file}"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/downloads/<filename>")
def serve_download(filename):
    return send_file(os.path.join(DOWNLOAD_FOLDER, filename), as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

