from flask import Flask, request, render_template, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download_video():
    video_url = request.form.get("url")

    if not video_url:
        return "Error: No URL provided."

    output_path = "downloads"
    os.makedirs(output_path, exist_ok=True)

    ydl_opts = {
        "outtmpl": f"{output_path}/video.%(ext)s",
        "format": "best"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    downloaded_file = next(f for f in os.listdir(output_path) if f.startswith("video"))

    return send_file(f"{output_path}/{downloaded_file}", as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
