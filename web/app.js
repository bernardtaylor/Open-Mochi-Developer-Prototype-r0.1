const FACES = ['neutral', 'happy', 'surprised', 'sleepy', 'listening', 'talking', 'sad'];
const $ = id => document.getElementById(id);
let gpsId = null;
let lastGpsSentAt = 0;
let lastGpsSpeed = null;
let pttDown = false;
const output = message => {
  const now = new Date().toLocaleTimeString();
  $('log').textContent = `[${now}] ${message}\n` + $('log').textContent.slice(0, 6000);
};
function render(state) {
  $('mochi').className = `mochi ${FACES.includes(state.expression) ? state.expression : 'neutral'}`;
  $('faceValue').textContent = state.expression;
  $('speedValue').textContent = `${Number(state.speed_kmh || 0).toFixed(1)} km/h`;
  for (const button of document.querySelectorAll('[data-face]')) {
    button.classList.toggle('active', button.dataset.face === state.expression);
  }
  $('ptt').classList.toggle('active', !!state.ptt);
}
let pendingCommand = Promise.resolve();
function send(command) {
  const result = pendingCommand.then(() => sendNow(command), () => sendNow(command));
  pendingCommand = result.then(() => undefined, () => undefined);
  return result;
}
async function sendNow(command) {
  try {
    const response = await fetch('/api/command', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({command})});
    const result = await response.json();
    if (!response.ok) throw new Error(result.detail || result.reply || `HTTP ${response.status}`);
    output(`${command} → ${result.reply}`);
    render(result.state);
    return true;
  } catch (err) { output(`ERROR: ${err.message}`); return false; }
}
for (const name of FACES) {
  const b = document.createElement('button'); b.textContent = name[0].toUpperCase() + name.slice(1); b.dataset.face = name;
  b.addEventListener('click', () => send(`E:${name}`)); $('faces').appendChild(b);
}
for (const button of document.querySelectorAll('[data-command]')) {
  button.addEventListener('click', () => send(button.dataset.command));
}
$('assistantForm').addEventListener('submit', async event => {
  event.preventDefault(); const text = $('askText').value.trim(); if (!text) return;
  $('assistantReply').textContent = 'Generating locally…';
  try {
    const response = await fetch('/api/assistant', {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({text})});
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || `HTTP ${response.status}`);
    $('assistantReply').textContent = data.response;
    await send('E:talking');
    if ('speechSynthesis' in window && data.response) {
      const voice = new SpeechSynthesisUtterance(data.response);
      voice.rate = 1.06;
      voice.onend = () => send('E:neutral');
      window.speechSynthesis.speak(voice);
    } else await send('E:neutral');
  } catch (err) { $('assistantReply').textContent = err.message; output(`AI: ${err.message}`); }
});
$('manualForm').addEventListener('submit', async event => {
  event.preventDefault(); const command = $('command').value.trim(); if (command) await send(command);
});
$('speed').addEventListener('input', () => {$('manualSpeed').textContent = `${$('speed').value} km/h`;});
$('sendSpeed').addEventListener('click', () => send(`V:${$('speed').value}`));
$('hello').addEventListener('click', async () => {
  await send('E:happy'); await send('S:1');
  if ('speechSynthesis' in window) {
    const voice = new SpeechSynthesisUtterance('Hello! I am an Open Mochi prototype.');
    voice.rate = 1.06; window.speechSynthesis.speak(voice);
    output('Browser speech demo (audio on this device only)');
  } else output('Browser speech synthesis unavailable');
});
// Pointer controls: PTT is command-only in r0. No microphone capture or voice stream.
const hold = $('ptt');
async function setPTT(enabled) {
  if (pttDown === enabled) return;
  pttDown = enabled;
  await send(enabled ? 'P:1' : 'P:0');
}
hold.addEventListener('pointerdown', event => {event.preventDefault(); hold.setPointerCapture(event.pointerId); setPTT(true);});
hold.addEventListener('pointerup', () => setPTT(false));
hold.addEventListener('pointercancel', () => setPTT(false));
hold.addEventListener('lostpointercapture', () => setPTT(false));
window.addEventListener('blur', () => setPTT(false));
$('clear').addEventListener('click', () => {$('log').textContent = '';});
$('startGPS').addEventListener('click', () => {
  if (!navigator.geolocation) { output('Geolocation not supported'); return; }
  if (gpsId !== null) return;
  gpsId = navigator.geolocation.watchPosition(position => {
    const mps = position.coords.speed;
    if (typeof mps !== 'number' || !Number.isFinite(mps)) {
      $('gpsState').textContent = 'GPS active, speed unavailable'; return;
    }
    const kmh = Math.max(0, Math.min(250, mps * 3.6));
    $('gpsState').textContent = `GPS speed ${kmh.toFixed(1)} km/h`;
    // Do not flood the serial/BLE bridge with high-frequency GPS updates.
    const now = Date.now();
    if (now - lastGpsSentAt >= 1000 && (lastGpsSpeed === null || Math.abs(kmh - lastGpsSpeed) >= 0.3)) {
      lastGpsSentAt = now; lastGpsSpeed = kmh;
      send(`V:${kmh.toFixed(1)}`);
    }
  }, error => { output(`GPS error: ${error.message}`); stopGPS(); }, {enableHighAccuracy: true, maximumAge: 1200, timeout: 12000});
  $('startGPS').disabled = true; $('stopGPS').disabled = false; $('gpsState').textContent = 'Requesting GPS…';
});
function stopGPS() {
  if (gpsId !== null) navigator.geolocation.clearWatch(gpsId);
  gpsId = null; lastGpsSpeed = null; lastGpsSentAt = 0; $('startGPS').disabled = false; $('stopGPS').disabled = true;
  $('gpsState').textContent = 'GPS inactive';
}
$('stopGPS').addEventListener('click', stopGPS);
async function init() {
  try {
    const response = await fetch('/api/state'); if (!response.ok) throw new Error('gateway unavailable');
    const data = await response.json(); render(data.state);
    $('connect').textContent = data.backend; $('connect').classList.add('online');
    output(`Connected to ${data.backend}`);
  } catch (err) { $('connect').textContent = 'Offline'; output(err.message); }
  const scheme = location.protocol === 'https:' ? 'wss:' : 'ws:';
  const websocket = new WebSocket(`${scheme}//${location.host}/api/events`);
  websocket.onmessage = event => {
    try { const payload = JSON.parse(event.data); if (payload.state) render(payload.state); }
    catch { /* malformed development event */ }
  };
  websocket.onclose = () => output('Event socket disconnected; HTTP commands may still work');
}
init();
