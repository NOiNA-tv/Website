# Assets

Everything in this folder is the real artwork. The only stand-in left in the
project is `../coins-data.js` (see below).

## Referenced by the page

| File | Used for |
|---|---|
| `noina-logo.gif` | Animated logo on the station channel (00) — 648×200, 200 frames |
| `noina-logo-static.png` | Static logo under the TV bezel — 648×200, transparent |
| `profile-photo.png` | Portrait in the SYS. INFO panel, revealed by the pixel wipe |
| `terrazzo-random.png` | Floor + wall texture, tiled at 270px |
| `static-noise-tile.png` | CRT static grain over the screen, tiled at 180px |
| `og-share.png` | Social share card — 1200×630, as declared in the OG tags |
| `favicon-small.svg`, `favicon-16/32/48.png`, `apple-touch-icon.png` | Browser and app icons |
| `segment7.woff2` | 7-segment LCD face for the channel number in the decoder |
| `static-noise-transition.mp4` | Full-screen static burst entering/leaving SYS. INFO (0.250s @ 60fps) |
| `static-click.mp3` | Channel-change click |
| `loading-loop.mp3` | Loop while a Vimeo channel buffers |

Both logo files carry real alpha, which matters: the page renders them through
`brightness(0) invert(1)`, so any opaque background would come out as a solid
white box over the mark.

## Present but not referenced

`favicon.svg`, `icon-512.png`, `mute-screen-icon.svg` and
`terrazzo-pattern.svg` ship with the brand set but nothing in `index.html`
points at them. `icon-512.png` is the right size for a PWA manifest icon and
`terrazzo-pattern.svg` is the vector source for the floor texture, so they are
kept rather than dropped.

## Still a placeholder

`../coins-data.js` holds the client marks that bounce around the CLIENTS box on
the SYS. INFO page — currently typeset monograms (`KNS`, `BZB`, …) standing in
for the real logos. It exports `COINS: {viewBox, inner}[]`, where `inner` is raw
SVG markup rendered inside `<svg fill="currentColor">`, so the shapes must not
set their own `fill`.

## One thing worth fixing

**`static-noise-transition.mp4` is 4.55 MB for a quarter-second** — roughly
145 Mbps. The `<video>` carries `preload="auto"`, so every visitor downloads all
of it during load whether or not they ever open SYS. INFO. It is by a wide
margin the heaviest thing on the site.

Static noise is close to the worst case for a codec — every pixel changes every
frame — which is how a 0.25s clip got this big. Options, best first:

1. **Re-encode at a sane bitrate.** It is on screen for 250ms behind a
   channel-change flash; it does not need visually-lossless noise.
   `ffmpeg -i static-noise-transition.mp4 -c:v libx264 -crf 30 -preset slow -an out.mp4`
2. **Drop the audio track.** The player sets `el.muted = true` permanently (the
   click comes from `static-click.mp3` instead), so the mp4's AAC track is never
   heard — `-an` removes it.
3. **Halve the frame rate.** At 30fps the static still reads as motion over 250ms.
4. **Ship a WebM/VP9 alternate** alongside the mp4 for browsers that take it.

If it cannot be made small, change `preload="auto"` to `preload="none"` on the
`<video>` in `index.html` so the download stops competing with first paint.
