// CDP state screenshot driver for the web app — pure Node, no deps.
// Usage: node cdp-webapp-shots.js <index.html path> <out dir>
// Loads the page once, then evaluates state changes and screenshots
// each screen: wifi, vpn, progress, device, error, unsupported.
const http = require('http');
const net = require('net');
const crypto = require('crypto');
const fs = require('fs');

const [,, htmlPath, outDir] = process.argv;
if (!htmlPath || !outDir) { console.error('usage: node cdp-webapp-shots.js <index.html> <outdir>'); process.exit(2); }
fs.mkdirSync(outDir, { recursive: true });

function httpJson(method, path) {
  return new Promise((resolve, reject) => {
    const req = http.request({ host: '127.0.0.1', port: 9222, path, method }, res => {
      let d = '';
      res.on('data', c => d += c);
      res.on('end', () => { try { resolve(JSON.parse(d)); } catch (e) { reject(new Error('bad json: ' + d.slice(0, 200))); } });
    });
    req.on('error', reject);
    req.end();
  });
}
function wsConnect(wsUrl) {
  return new Promise((resolve, reject) => {
    const m = wsUrl.match(/^ws:\/\/([^:/]+):(\d+)(\/.*)$/);
    const [, host, port, path] = m;
    const key = crypto.randomBytes(16).toString('base64');
    const sock = net.connect(Number(port), host, () => {
      sock.write(`GET ${path} HTTP/1.1\r\nHost: ${host}:${port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: ${key}\r\nSec-WebSocket-Version: 13\r\n\r\n`);
    });
    let handshakeDone = false, buf = Buffer.alloc(0), frag = [];
    const handlers = { message: null };
    sock.on('data', chunk => {
      buf = Buffer.concat([buf, chunk]);
      if (!handshakeDone) {
        const idx = buf.indexOf('\r\n\r\n');
        if (idx === -1) return;
        if (!buf.slice(0, idx).toString().includes('101')) return reject(new Error('WS handshake failed'));
        handshakeDone = true; buf = buf.slice(idx + 4);
        resolve({ send, onMessage: fn => { handlers.message = fn; } });
      }
      while (true) {
        if (buf.length < 2) break;
        const fin = (buf[0] & 0x80) !== 0, op = buf[0] & 0x0f;
        let len = buf[1] & 0x7f, off = 2;
        if (len === 126) { if (buf.length < 4) break; len = buf.readUInt16BE(2); off = 4; }
        else if (len === 127) { if (buf.length < 10) break; len = Number(buf.readBigUInt64BE(2)); off = 10; }
        if (buf.length < off + len) break;
        const payload = buf.slice(off, off + len);
        buf = buf.slice(off + len);
        if (op === 0x9) sendRaw(0xA, payload);
        else if (op === 0x1 || op === 0x0) {
          frag.push(payload);
          if (fin) { const msg = Buffer.concat(frag).toString('utf8'); frag = []; if (handlers.message) handlers.message(msg); }
        } else if (op === 0x8) sock.end();
      }
    });
    function sendRaw(op, payload) {
      const mask = crypto.randomBytes(4);
      let header;
      const len = payload.length;
      if (len < 126) header = Buffer.from([0x80 | op, 0x80 | len]);
      else if (len < 65536) { header = Buffer.alloc(4); header[0] = 0x80 | op; header[1] = 0x80 | 126; header.writeUInt16BE(len, 2); }
      else { header = Buffer.alloc(10); header[0] = 0x80 | op; header[1] = 0x80 | 127; header.writeBigUInt64BE(BigInt(len), 2); }
      const masked = Buffer.alloc(len);
      for (let i = 0; i < len; i++) masked[i] = payload[i] ^ mask[i % 4];
      sock.write(Buffer.concat([header, mask, masked]));
    }
    function send(obj) { sendRaw(0x1, Buffer.from(JSON.stringify(obj))); }
    sock.on('error', reject);
  });
}

const SHOTS = [
  ["wifi", `S.networks=[{ssid:'HomeNet-5G',bssid:'aa:bb:cc:dd:ee:ff',rssi:-52,band:'5',security:'Secured'},{ssid:'Hotel_Guest',bssid:'aa:bb:cc:dd:ee:00',rssi:-67,band:'2.4',security:'Open'},{ssid:'CoffeeShop',bssid:'aa:bb:cc:dd:ee:01',rssi:-74,band:'5',security:'Secured'}];S.ssid='HomeNet-5G';S.step='wifi';S.error=null;render()`],
  ["vpn", `S.step='vpn';S.error=null;render()`],
  ["progress", `S.ssid='HomeNet-5G';S.progress=[{label:'USB link',state:'done'},{label:'Joining Wi-Fi',state:'active'},{label:'Internet check',state:'wait'},{label:'Starting VPN',state:'wait'}];S.step='progress';S.error=null;render()`],
  ["device", `S.info={model:'HomeSteadyLink Zero2W',serial:'HS-FAKE-001',fw:'1.4.0',state:'online'};S.status={state:'online',error:null,ssid:'HomeNet-5G',ip4:'10.64.0.42',vpn:true};S.exitNode='mullvad-us12';S.ssid='HomeNet-5G';S.step='device';S.error=null;render()`],
  ["error", `S.error={title:"The router couldn't join HomeNet-5G",summary:'Check the password and try again.',code:'error: wifi_auth_failed · state: wifi_auth_failed',detail:'ssid: HomeNet-5G · bssid: aa:bb:cc:dd:ee:ff · rssi: -52',next:'What to do next: re-enter the Wi-Fi password. The old config still works if one was saved.',retryLabel:'Re-enter Wi-Fi password',retry:()=>{}};render()`],
  ["unsupported", `S.step='unsupported';render()`],
];

(async () => {
  const targetUrl = 'file://' + htmlPath;
  const target = await httpJson('PUT', '/json/new?' + new URLSearchParams({ url: targetUrl }).toString());
  const ws = await wsConnect(target.webSocketDebuggerUrl);
  let id = 0;
  const pending = new Map(), events = [];
  ws.onMessage(msg => {
    let o; try { o = JSON.parse(msg); } catch { return; }
    if (o.id && pending.has(o.id)) { pending.get(o.id)(o); pending.delete(o.id); }
    else if (o.method) events.push(o);
  });
  const call = (method, params) => new Promise(res => { const i = ++id; pending.set(i, res); ws.send({ id: i, method, params }); });
  await call('Page.enable');
  await call('Runtime.enable');
  await call('Emulation.setDeviceMetricsOverride', { width: 1280, height: 800, deviceScaleFactor: 1, mobile: false });
  await call('Page.navigate', { url: targetUrl });
  const t0 = Date.now();
  while (Date.now() - t0 < 15000) {
    if (events.some(e => e.method === 'Page.loadEventFired')) break;
    await new Promise(r => setTimeout(r, 200));
  }
  await new Promise(r => setTimeout(r, 500));
  // Collect console errors.
  const errors = events.filter(e => e.method === 'Runtime.exceptionThrown' || (e.method === 'Runtime.consoleAPICalled' && e.params.type === 'error'));
  for (const [name, expr] of SHOTS) {
    const ev = await call('Runtime.evaluate', { expression: expr });
    if (ev.result && ev.result.exceptionDetails) console.error(name, 'EVAL ERR', JSON.stringify(ev.result.exceptionDetails).slice(0, 300));
    await new Promise(r => setTimeout(r, 300));
    const shot = await call('Page.captureScreenshot', { format: 'png' });
    const out = outDir + '/' + name + '.png';
    fs.writeFileSync(out, Buffer.from(shot.result.data, 'base64'));
    console.log('wrote', out, fs.statSync(out).size, 'bytes');
  }
  console.log('console errors:', errors.length);
  process.exit(0);
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
