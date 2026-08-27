# Assets

Everything in this folder is the real artwork. The only stand-in left in the
project is `../coins-data.js` (see below).

## Referenced by the page

| File | Used for |
|---|---|
| `noina-logo.gif` | Animated logo on the station channel (00) — 648×200, 200 frames |
| `noina-logo-static.png` | Static logo under the TV bezel — 648×200, transparent |
| `portrait-1.png` | The SYS. INFO portrait, revealed by the pixel wipe |
| `portrait-anim.mp4` | Plays over the portrait when it is tapped — 640×852, 1.6s, with sound |
| `terrazzo-random.png` | Floor + wall texture, tiled at 270px |
| `static-noise-tile.png` | CRT static grain over the screen, tiled at 180px |
| `og-share.png` | Social share card — 1200×630, as declared in the OG tags |
| `favicon-small.svg` | Browser icon — the penguin, blinking on an 8s cycle |
| `favicon-16/32/48.png`, `apple-touch-icon.png` | Icon fallbacks for browsers that will not take an SVG |
| `segment7.woff2` | 7-segment LCD face for the channel number in the decoder |
| `static-noise-transition.mp4` | Full-screen static burst entering/leaving SYS. INFO (0.250s @ 60fps) |
| `static-click.mp3` | Channel-change click |
| `loading-loop.mp3` | Loop while a channel buffers |
| `tv-knock.mp3` | The set knocked on its chassis |
| `screen-tap-01..04.mp3` | A finger on the glass, picked at random |
| `remote-mute/info/channel-up/channel-down.mp3` | Each remote button's own click, named for its button |
| `lottie/fingerprint-01..04.json` | The four prints left on the glass, picked at random |
| `lottie/mute, info, channel-up, channel-down.json` | The remote's four buttons |

Both logo files carry real alpha, which matters: the page renders them through
`brightness(0) invert(1)`, so any opaque background would come out as a solid
white box over the mark.

## The icon set is two colourways

`favicon-small.svg` is a **dark penguin on cyan**; the PNG fallbacks are the
same penguin **inverted** — cyan on dark `#0d1418`. Browsers that accept an SVG
favicon therefore show one colourway and everything else shows the other. If
that should be consistent, rasterize `favicon-small.svg` to 16/32/48/180 and
replace the PNGs (or recolour the SVG to match them).

## Present but not referenced

`icon-512.png`, `mute-screen-icon.svg` and `terrazzo-pattern.svg` ship with the
brand set but nothing in `index.html` points at them. `icon-512.png` is the
right size for a PWA manifest icon and `terrazzo-pattern.svg` is the vector
source for the floor texture, so they are kept rather than dropped.

## Client logos

`../coins-data.js` holds the 37 client logos that bounce around the CLIENTS box
on the SYS. INFO page. It exports `COINS: {name, viewBox, inner}[]`, where
`inner` is raw SVG markup rendered inside `<svg fill="currentColor">` — the
shapes carry no `fill` of their own, which is what lets them pick up the
terminal's cyan.

## Page weight

`static-noise-transition.mp4` was re-encoded from 4.55 MB down to **1.47 MB**
(same 0.250s @ 60fps, 15 frames, H.264 Main). The `<video>` still carries
`preload="auto"`, so every visitor downloads it during load whether or not they
open SYS. INFO — it remains the single heaviest asset on the site.

If it needs to come down further:

- **Drop the audio track.** The clip still carries a 0.32s AAC track, and the
  player sets `el.muted = true` permanently (the click comes from
  `static-click.mp3` instead), so it is never heard. `ffmpeg -i in.mp4 -c copy -an out.mp4`
- **Halve the frame rate.** At 30fps the static still reads as motion over 250ms.
- **Ship a WebM/VP9 alternate** alongside the mp4 for browsers that take it.
- **Or set `preload="none"`** on the `<video>` in `index.html` so the download
  stops competing with first paint.
