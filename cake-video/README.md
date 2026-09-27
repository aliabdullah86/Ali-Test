# Crémé Dorée · Tres Leches promo video

`cremedoree-tres-leches.mp4` is a 23-second vertical promo (1080×1920, 30 fps) for Instagram Reels, TikTok, WhatsApp Status and YouTube Shorts. The cuts, flashes and text hits land on the beat of a 120 BPM music track.

| Time | Scene |
|---|---|
| 0–3s | Glitter burst and shockwave as the gold "CD" monogram lands on spinning sunburst rays, the brand name drops in letter by letter, then "by Rija presents" |
| 3–6s | Beat-cut hook, one photo per beat: **SOFT. / SOAKED. / SINFUL.** in gold foil text |
| 6–10s | "THE 3-MILK MAGIC": milk drips down, the cake sits in a rotating gold medallion, and three numbered pills pop in (evaporated milk, condensed milk, fresh cream) |
| 10–14s | Split-screen of all three photos sliding in on diagonals: "HANDMADE with love, every single day", with piped cream rosettes |
| 14–17.5s | Gift photo with light leaks, falling rose petals and a spinning "PERFECT GIFT" sticker |
| 17.5–23s | "ORDER NOW" slam with confetti, flare and a shining gold "DM to order" button |

Transitions are whip pans, a whipped-cream wipe and white flashes.

## Changing the text (phone number, handle, etc.)

Edit `config.js`, then re-render:

```bash
npm i -g playwright          # once
pip install imageio-ffmpeg numpy
NODE_PATH=$(npm root -g) node render.js
```

Open `scene.html` in a browser to preview the animation live.

## Adding AI clips from free tools

These AI video tools have free daily credits. Upload one of the photos in `assets/` to any of them with the prompt below, then cut the clip into the video in CapCut (free):

- **Kling AI** (klingai.com): daily free credits, image-to-video
- **Hailuo / MiniMax** (hailuoai.video): free daily credits
- **Luma Dream Machine** (lumalabs.ai): free tier
- **Meta AI** (meta.ai or WhatsApp): free "animate" for images
- **Google Gemini / Veo**: limited free video generations in the Gemini app

Prompt:

> Luxury dessert commercial, vertical close-up. The clear dome lid is gently lifted off the tres leches cake cup. A piping bag swirls fresh glossy whipped cream on top, sweet condensed milk drizzles over and soaks into the golden sponge, and a light dusting of cinnamon falls. Slow cinematic push-in, soft warm golden lighting, shallow depth of field, blush-pink and gold tones.
