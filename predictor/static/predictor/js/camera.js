// camera.js
const showUploadBtn = document.getElementById("showUpload");
const showCameraBtn = document.getElementById("showCamera");
const uploadPanel = document.getElementById("uploadPanel");
const cameraPanel = document.getElementById("cameraPanel");

const leafInput = document.getElementById("leaf_input");
const uploadPreview = document.getElementById("uploadPreview");

const startCameraBtn = document.getElementById("startCamera");
const stopCameraBtn = document.getElementById("stopCamera");
const captureBtn = document.getElementById("captureBtn");
const video = document.getElementById("video");
const canvas = document.getElementById("canvas");
const cameraForm = document.getElementById("cameraForm");
const cameraInput = document.getElementById("camera_image");
const cameraPreview = document.getElementById("cameraPreview");

let stream = null;

showUploadBtn.addEventListener("click", () => {
  uploadPanel.classList.remove("hidden");
  cameraPanel.classList.add("hidden");
});
showCameraBtn.addEventListener("click", () => {
  uploadPanel.classList.add("hidden");
  cameraPanel.classList.remove("hidden");
});

// Upload preview
leafInput.addEventListener("change", (e) => {
  uploadPreview.innerHTML = "";
  const file = e.target.files && e.target.files[0];
  if (!file) return;
  const img = document.createElement("img");
  img.src = URL.createObjectURL(file);
  img.onload = () => URL.revokeObjectURL(img.src);
  uploadPreview.appendChild(img);
});

// Camera handling
async function startCamera() {
  try {
    stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" }, audio: false });
    video.srcObject = stream;
    video.play();
  } catch (err) {
    alert("Cannot access camera. Make sure you allowed permission.");
    console.error(err);
  }
}

function stopCamera() {
  if (stream) {
    stream.getTracks().forEach(t => t.stop());
    stream = null;
  }
  video.pause();
  video.srcObject = null;
}

startCameraBtn.addEventListener("click", (e) => {
  e.preventDefault();
  startCamera();
});

stopCameraBtn.addEventListener("click", (e) => {
  e.preventDefault();
  stopCamera();
});

captureBtn.addEventListener("click", (e) => {
  e.preventDefault();
  if (!stream) {
    alert("Start the camera first.");
    return;
  }
  const ctx = canvas.getContext("2d");
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  const dataUrl = canvas.toDataURL("image/jpeg", 0.9);
  cameraInput.value = dataUrl;

  // show preview
  cameraPreview.innerHTML = "";
  const img = document.createElement("img");
  img.src = dataUrl;
  cameraPreview.appendChild(img);

  // submit form
  cameraForm.submit();
});
