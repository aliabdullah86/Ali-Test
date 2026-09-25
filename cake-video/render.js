// Renders scene.html frame by frame into cremedoree-tres-leches.mp4 (1080x1920, 30 fps).
// Usage: node render.js   (needs: playwright, python3 with imageio-ffmpeg + numpy)
const { chromium } = require("playwright");
const { spawn, execFileSync } = require("child_process");
const path = require("path");

const FPS = 30;
const OUT = path.join(__dirname, "cremedoree-tres-leches.mp4");

(async () => {
  const ffmpeg = execFileSync("python3", ["-c", "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())"]).toString().trim();
  execFileSync("python3", [path.join(__dirname, "music.py")], { stdio: "inherit" });

  const browser = await chromium.launch({ args: ["--allow-file-access-from-files"] });
  const page = await browser.newPage({ viewport: { width: 540, height: 960 } });
  await page.goto("file://" + path.join(__dirname, "scene.html"));
  await page.evaluate(() => window.ready);
  const duration = await page.evaluate(() => window.DURATION);
  const frames = Math.round(duration * FPS);

  const ff = spawn(ffmpeg, [
    "-y", "-f", "image2pipe", "-framerate", String(FPS), "-c:v", "mjpeg", "-i", "-",
    "-i", path.join(__dirname, "music.wav"),
    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium",
    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", OUT,
  ], { stdio: ["pipe", "inherit", "inherit"] });

  for (let i = 0; i < frames; i++) {
    const data = await page.evaluate(t => { window.render(t); return document.getElementById("c").toDataURL("image/jpeg", 0.95); }, i / FPS);
    const buf = Buffer.from(data.split(",")[1], "base64");
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once("drain", r));
    if (i % 60 === 0) process.stdout.write(`frame ${i}/${frames}\n`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on("close", r));
  await browser.close();
  console.log("wrote", OUT);
})();
