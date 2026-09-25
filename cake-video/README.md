# Crémé Dorée · Tres Leches promo video

`cremedoree-tres-leches.mp4` is a 26-second vertical promo (1080×1920, 30 fps, with music) for Instagram Reels, TikTok, WhatsApp Status and YouTube Shorts.

| Time | Scene |
|---|---|
| 0–4.6s | Gold "CD" logo draws itself in, then *Crémé Dorée by Rija presents Tres Leches* |
| 4.6–9.6s | Top-down photo with slow zoom, milk dripping in from the top: "Three milks. One unforgettable bite." |
| 9.6–14.8s | Side photo, a piping bag pipes cream rosettes, cinnamon falls: "Soaked. Whipped. Perfected." |
| 14.8–19.8s | Gift-wrapped photo with falling rose petals: "Wrapped with love, perfect for gifting" |
| 19.8–26s | Call to action: "Order yours today" plus a gold "DM to order" button |

Between scenes, piped whipped-cream rosettes fill the screen and then sweep away.

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
