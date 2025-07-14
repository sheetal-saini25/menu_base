import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="All-in-One Utilities", layout="wide")

html_code = """
<!DOCTYPE html>
<html>
<head>
  <title>All-in-One Web Tools</title>
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <style>
    body { font-family: Arial; padding: 20px; }
    h2 { color: #444; margin-top: 30px; }
    button { padding: 10px 15px; margin: 5px; border-radius: 6px; border: none; background-color: #2a9d8f; color: white; cursor: pointer; }
    input, textarea { width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ccc; border-radius: 4px; }
    video { width: 100%; max-width: 480px; border-radius: 8px; margin-top: 10px; }
    table { width: 100%; border-collapse: collapse; margin-top: 20px; }
    th, td { border: 1px solid #ccc; padding: 8px 10px; text-align: center; }
    th { background-color: #f9f9f9; }
    #image-container img { width: 150px; margin: 10px; cursor: pointer; border: 2px solid #ccc; border-radius: 8px; transition: 0.2s; }
    #image-container img:hover { transform: scale(1.05); border-color: #666; }
    #most-hovered { margin-top: 15px; font-weight: bold; color: #444; }
  </style>
</head>
<body>

<h2>📍 Get Your Current Location</h2>
<button onclick=\"getLocation()\">Get Location</button>
<p id=\"locationOutput\"></p>

<h2>🛒 Find Nearby Grocery Stores</h2>
<button onclick=\"findGroceryStores()\">Find Grocery Stores</button>

<h2>🚗 Route: Mansarovar ➡ Sitapura</h2>
<button onclick=\"openGoogleMapsRoute()\">Show Route</button>

<h2>📷 Camera Recorder</h2>
<video id=\"camera\" autoplay muted></video><br>
<button onclick=\"startCamera()\">Start Camera</button>
<button onclick=\"stopCamera()\">Stop Camera</button>

<h2>✉️ Send Email</h2>
<input type=\"email\" id=\"to\" placeholder=\"Recipient Email\">
<input type=\"text\" id=\"subject\" placeholder=\"Subject\">
<textarea id=\"body\" placeholder=\"Message Body\"></textarea>
<button onclick=\"sendEmail()\">Send Email</button>

<h2>📱 Send WhatsApp Message</h2>
<input type=\"text\" id=\"phone\" placeholder=\"+91xxxxxxxxxx\">
<textarea id=\"whatsappMessage\" placeholder=\"Your Message\"></textarea>
<button onclick=\"sendWhatsApp()\">Send WhatsApp</button>

<h2>🖼️ User Activity Tracker</h2>
<div id=\"image-container\"></div>
<button onclick=\"downloadActivityLog()\">Download Activity Log</button>
<p id=\"most-hovered\">Most hovered image: N/A</p>
<table><thead><tr><th>#</th><th>Event</th><th>Image</th><th>Details</th><th>Time</th></tr></thead><tbody id=\"log-body\"></tbody></table>

<h2>🎥 Record Laptop Camera</h2>
<video id=\"preview\" autoplay muted playsinline width=\"480\"></video><br><br>
<button onclick=\"startRecording()\">▶️ Start Recording</button>
<button onclick=\"stopRecording()\">⏹ Stop Recording</button>
<video id=\"playback\" controls width=\"480\"></video>

<script>
let camStream;
let mediaRecorder;
let recordedChunks = [];
const activityLog = [];
const hoverTimes = {};
const STAY_THRESHOLD_MS = 1000;
const images = ['3.jpg', '2.png', '1.jpg'];

function getLocation() {
  navigator.geolocation.getCurrentPosition(showPosition, showError);
}
function showPosition(pos) {
  const lat = pos.coords.latitude;
  const lon = pos.coords.longitude;
  document.getElementById("locationOutput").innerHTML = `Latitude: ${lat}<br>Longitude: ${lon}<br><a href='https://www.google.com/maps?q=${lat},${lon}' target='_blank'>View on Google Maps</a>`;
}
function showError(err) {
  alert("Error: " + err.message);
}
function findGroceryStores() {
  navigator.geolocation.getCurrentPosition(function(pos) {
    const lat = pos.coords.latitude;
    const lon = pos.coords.longitude;
    window.open(`https://www.google.com/maps/search/grocery+store/@${lat},${lon},15z`, '_blank');
  });
}
function openGoogleMapsRoute() {
  window.open("https://www.google.com/maps/dir/Mansarovar,+Jaipur/Sitapura,+Jaipur", "_blank");
}
async function startCamera() {
  try {
    camStream = await navigator.mediaDevices.getUserMedia({ video: true });
    document.getElementById("camera").srcObject = camStream;
  } catch (e) {
    alert("Camera error: " + e.message);
  }
}
function stopCamera() {
  if (camStream) {
    camStream.getTracks().forEach(track => track.stop());
    document.getElementById("camera").srcObject = null;
  }
}
function sendEmail() {
  const to = document.getElementById('to').value;
  const subject = document.getElementById('subject').value;
  const body = document.getElementById('body').value;
  window.location.href = `mailto:${to}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
}
function sendWhatsApp() {
  const phone = document.getElementById("phone").value;
  const msg = document.getElementById("whatsappMessage").value;
  window.open(`https://wa.me/${phone}?text=${encodeURIComponent(msg)}`, '_blank');
}
function startRecording() {
  navigator.mediaDevices.getUserMedia({ video: true, audio: true }).then(stream => {
    document.getElementById('preview').srcObject = stream;
    recordedChunks = [];
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = e => { if (e.data.size > 0) recordedChunks.push(e.data); };
    mediaRecorder.onstop = () => {
      const blob = new Blob(recordedChunks, { type: 'video/webm' });
      const url = URL.createObjectURL(blob);
      document.getElementById('playback').src = url;
      const a = document.createElement('a');
      a.href = url;
      a.download = 'video_recorded.webm';
      a.click();
    };
    mediaRecorder.start();
    alert("Recording started...");
  }).catch(err => alert("Error: " + err.message));
}
function stopRecording() {
  if (mediaRecorder && mediaRecorder.state !== "inactive") mediaRecorder.stop();
}
function logActivity(data) {
  activityLog.push(data);
  const row = document.createElement('tr');
  row.innerHTML = `<td>${activityLog.length}</td><td>${data.type}</td><td>${data.imageId}</td><td>${data.details}</td><td>${data.time}</td>`;
  document.getElementById('log-body').appendChild(row);
}
function updateMostHovered() {
  const sorted = Object.entries(hoverTimes).sort((a, b) => b[1] - a[1]);
  if (sorted.length > 0) {
    const [imgId, dur] = sorted[0];
    document.getElementById('most-hovered').innerText = `Most hovered image: ${imgId} for ${(dur / 1000).toFixed(2)} sec`;
  }
}
images.forEach((src, i) => {
  const img = document.createElement('img');
  img.src = src;
  img.dataset.id = `img${i}`;
  let hoverStart = null;
  img.addEventListener('click', e => logActivity({ type: 'click', imageId: img.dataset.id, details: `x=${e.clientX}, y=${e.clientY}`, time: new Date().toLocaleTimeString() }));
  img.addEventListener('mouseenter', () => {
    hoverStart = Date.now();
    logActivity({ type: 'mouseenter', imageId: img.dataset.id, details: 'Mouse entered', time: new Date().toLocaleTimeString() });
  });
  img.addEventListener('mouseleave', () => {
    if (!hoverStart) return;
    const duration = Date.now() - hoverStart;
    logActivity({ type: 'mouseleave', imageId: img.dataset.id, details: 'Mouse left', time: new Date().toLocaleTimeString() });
    if (duration >= STAY_THRESHOLD_MS) {
      logActivity({ type: 'hover_hold', imageId: img.dataset.id, details: `${(duration / 1000).toFixed(2)} sec`, time: new Date().toLocaleTimeString() });
      if (!hoverTimes[img.dataset.id] || duration > hoverTimes[img.dataset.id]) {
        hoverTimes[img.dataset.id] = duration;
        updateMostHovered();
      }
    }
    hoverStart = null;
  });
  img.onerror = () => { img.alt = 'Image not found'; img.style.border = '2px dashed red'; };
  document.getElementById('image-container').appendChild(img);
});
function downloadActivityLog() {
  const blob = new Blob([JSON.stringify(activityLog, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'activity_log.json';
  a.click();
  URL.revokeObjectURL(url);
}
</script>

</body>
</html>
"""

components.html(html_code, height=3000, scrolling=True)  # You can adjust the height as needed
