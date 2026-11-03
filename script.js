const API_URL = "https://mono-bloom.onrender.com/convert";
// scattered stars: [left %, top %, size px, rotation deg]
const stars = [
  [8, 6, 34, 12],   [30, 4, 16, -8],  [88, 10, 14, 20],
  [3, 38, 40, -15], [93, 44, 36, 10], [12, 72, 22, 25],
  [80, 80, 30, -20],[96, 94, 26, 5],  [40, 94, 34, -12],
  [60, 3, 12, 30],  [5, 92, 28, 8],   [72, 62, 12, -25]
];

const sky = document.querySelector(".sky");
stars.forEach(([x, y, size, rot]) => {
  const s = document.createElement("div");
  s.className = "star";
  s.style.cssText = `left:${x}%;top:${y}%;width:${size}px;height:${size}px;transform:rotate(${rot}deg)`;
  sky.appendChild(s);
});
 
const fileInput = document.getElementById("fileInput");
const dropzone = document.getElementById("dropzone");
const result = document.getElementById("result");
const previewImg = document.getElementById("previewImg");
const video = document.getElementById("video");
const status = document.getElementById("status");
const download = document.getElementById("download");

["dragenter", "dragover"].forEach(e =>
  dropzone.addEventListener(e, ev => { ev.preventDefault(); dropzone.classList.add("over"); }));
["dragleave", "drop"].forEach(e =>
  dropzone.addEventListener(e, ev => { ev.preventDefault(); dropzone.classList.remove("over"); }));
dropzone.addEventListener("drop", ev => handleFile(ev.dataTransfer.files[0]));
fileInput.addEventListener("change", () => handleFile(fileInput.files[0]));

async function handleFile(file) {
  if (!file) return;
  result.hidden = false;
  download.hidden = true;
  previewImg.hidden = true;
  video.hidden = true;
  status.textContent = "converting… videos can take a while";

  const form = new FormData();
  form.append("file", file);

  try {
    const res = await fetch(API_URL, { method: "POST", body: form });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.error || "conversion failed");
    }
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    const ext = file.name.slice(file.name.lastIndexOf(".")).toLowerCase();

    if (file.type.startsWith("image/")) {
      previewImg.src = url;
      previewImg.hidden = false;
    } else {
      video.src = url;
      video.controls = true;
      video.hidden = false;
    }
    download.href = url;
    download.download = "mono-bloom" + ext;   // same extension as the original
    download.hidden = false;
    status.textContent = "done ✓";
  } catch (e) {
    status.textContent = "something went wrong: " + e.message;
  }
}