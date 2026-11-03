# mono bloom: Black & White Image and Video Converter

Turn any coloured photo or video into black and white. Upload a file, preview the result and download it in the same format. Videos keep their original audio untouched.

## 1. Methodology

```mermaid
flowchart LR
    A[File Upload] --> B[File Validation]
    B --> C[Photo / Video Conversion]
    C --> D[Download Result]
    D --> E[Auto Cleanup]
```

## 2. Description

- **Supported image types (7 extensions):** JPG, JPEG, PNG, BMP, WebP, TIF, TIFF
- **Supported video types (6 extensions):** MP4, MOV, M4V, MKV, WebM, AVI
- **Image conversion:** OpenCV converts the image to greyscale. PNG and WebP transparency is kept, and JPEG and WebP are saved at maximum quality.
- **Video conversion:** FFmpeg removes the colour (`hue=s=0` filter) and re-encodes the video at a very high quality setting. The audio track is copied without changes (`-c:a copy`), and the file keeps its original extension.
- **Technology:** Python, Flask, OpenCV, FFmpeg, Docker, HTML, CSS, JavaScript
- **Hosting:** the website runs on GitHub Pages and the conversion server runs on Render (free instance)
- **Other information:** uploads are limited to 200 MB. Files are processed in a temporary folder and deleted as soon as the result is sent back. The free server sleeps when idle, so the first upload after a quiet period can take about a minute.

## 3. Input / Output

| Original | Black & White |
|---|---|
| ![Original](original.jpg) | ![Black and white](greyscale.png) |

## 4. Live link

https://mono-bloom.onrender.com/



## 5. Run it locally

```bash
cd backend
pip install -r requirements.txt
python app.py
```

FFmpeg must be installed and available in your PATH. Then open `index.html` with a local server such as VS Code Live Server, and set `API_URL` in `script.js` to `http://127.0.0.1:5000/convert`.

## 6. Project structure

```
mono-bloom/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── fonts/
├── screenshots/
├── index.html
├── style.css
└── script.js
```
