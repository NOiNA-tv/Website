# Assets

The audio, font and video here are the real files. The **images are still
placeholders** generated to stand in for the real artwork — swap each one at
the same path and filename, nothing else needs to change.

## Real assets

| File | Used for |
|---|---|
| `segment7.woff2` | 7-segment LCD face for the channel number in the decoder |
| `static-noise-transition.mp4` | Full-screen static burst when entering/leaving SYS. INFO (0.250s @ 60fps) |
| `static-click.mp3` | Channel-change click |
| `loading-loop.mp3` | Loop while a Vimeo channel buffers |

> **`static-noise-transition.mp4` is 4.55 MB for a quarter-second** — roughly
> 145 Mbps. The `<video>` carries `preload="auto"`, so every visitor downloads
> all of it during load whether or not they ever open SYS. INFO. Re-encoding it
> would be the single biggest win available on page weight; see the note at the
> bottom of this file.

## Placeholders to replace

| File | Used for | Notes for the replacement |
|---|---|---|
| `noina-logo.gif` | Animated logo on the station channel (00) | The page applies `brightness(0) invert(96%)`, so it renders pure white whatever the source colour. Transparent background. |
| `noina-logo-static.png` | Static logo under the TV bezel | Same filter treatment (`brightness(0) invert(1)`), rendered at 16.5px tall. |
| `profile-photo.png` | Photo in the SYS. INFO panel | Shown in a 102×148 box, `object-fit: cover`, revealed by the pixel-wipe animation. Portrait crop. |
| `terrazzo-random.png` | Floor + wall texture | Must tile seamlessly; drawn at 270×270. |
| `static-noise-tile.png` | CRT static grain over the screen | Must tile seamlessly; drawn at 180×180, screen-blended at 0.2 opacity. |
| `og-share.png` | Social share card | Must be exactly 1200×630 (declared in the OG tags). |
| `favicon-small.svg`, `favicon-16.png`, `favicon-32.png`, `favicon-48.png`, `apple-touch-icon.png` | Browser/app icons | apple-touch-icon is 180×180. |
| `../coins-data.js` | Client logos bouncing in the CLIENTS box | Exports `COINS: {viewBox, inner}[]`, where `inner` is raw SVG markup rendered inside `<svg fill="currentColor">` — so shapes must not set their own `fill`. Currently typeset monograms; replace with the real vector marks. |

## Shrinking the transition video

Static noise is close to the worst case for a video codec — every pixel changes
every frame — which is why a 0.25s clip landed at 4.55 MB. Options, best first:

1. **Re-encode at a sane bitrate.** The clip is on screen for 250ms behind a
   channel-change flash; it does not need visually-lossless noise.
   `ffmpeg -i static-noise-transition.mp4 -c:v libx264 -crf 30 -preset slow -an out.mp4`
2. **Drop the audio track.** The player sets `el.muted = true` permanently (the
   click sound comes from `static-click.mp3` instead), so the mp4's AAC track is
   never heard — `-an` removes it.
3. **Halve the frame rate.** At 30fps instead of 60 the static still reads as
   motion over 250ms.
4. **Ship a WebM/VP9 alternate** alongside the mp4 for browsers that take it.

If it cannot be made small, consider dropping `preload="auto"` to `preload="none"`
so the download stops blocking first paint.

## Regenerating the placeholders

`tools/gen-placeholder-assets.py` (Pillow) produced every generated file here.
It is kept only so the stand-ins can be rebuilt or tweaked; it is not part of
the site and nothing at runtime depends on it.
