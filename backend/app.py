import os
import shutil
import subprocess
import tempfile

import cv2
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # later, restrict this to your GitHub Pages address
app.config["MAX_CONTENT_LENGTH"] = 200 * 1024 * 1024  # 200 MB

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".bmp", ".webp", ".tif", ".tiff"}
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".mkv", ".webm", ".avi"}


def grey_image(src, dst, ext):
    img = cv2.imread(src, cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError("could not read image")

    if img.ndim == 3 and img.shape[2] == 4:      # keep transparency (PNG/WebP)
        grey = cv2.cvtColor(img[:, :, :3], cv2.COLOR_BGR2GRAY)
        out = cv2.merge([grey, grey, grey, img[:, :, 3]])
    elif img.ndim == 3:
        out = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        out = img                                 # already greyscale

    params = []
    if ext in (".jpg", ".jpeg"):
        params = [cv2.IMWRITE_JPEG_QUALITY, 100]
    elif ext == ".webp":
        params = [cv2.IMWRITE_WEBP_QUALITY, 100]
    cv2.imwrite(dst, out, params)


def grey_video(src, dst, ext):
    if ext == ".webm":
        video_codec = ["-c:v", "libvpx-vp9", "-crf", "10", "-b:v", "0"]
    else:
        video_codec = ["-c:v", "libx264", "-crf", "12", "-preset", "slow"]

    cmd = [
        "ffmpeg", "-y", "-i", src,
        "-map", "0:v:0", "-map", "0:a?",   # first video stream + all audio (if any)
        "-vf", "hue=s=0",                  # remove colour
        *video_codec,
        "-c:a", "copy",                    # audio untouched
        "-map_metadata", "0",
    ]
    if ext in (".mp4", ".mov", ".m4v"):
        cmd += ["-movflags", "+faststart"]
    cmd.append(dst)

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr[-400:])


@app.route("/convert", methods=["POST"])
def convert():
    file = request.files.get("file")
    if not file or not file.filename:
        return jsonify(error="no file received"), 400

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in IMAGE_EXT | VIDEO_EXT:
        return jsonify(error=f"{ext or 'this'} files are not supported"), 400

    folder = tempfile.mkdtemp()
    src = os.path.join(folder, "input" + ext)
    dst = os.path.join(folder, "output" + ext)
    file.save(src)

    try:
        if ext in IMAGE_EXT:
            grey_image(src, dst, ext)
        else:
            grey_video(src, dst, ext)
        with open(dst, "rb") as f:
            data = f.read()
    except Exception as e:
        return jsonify(error=str(e)), 500
    finally:
        shutil.rmtree(folder, ignore_errors=True)

    from io import BytesIO
    return send_file(BytesIO(data), download_name="mono-bloom" + ext, as_attachment=False)


if __name__ == "__main__":
    app.run(debug=True, port=5000)