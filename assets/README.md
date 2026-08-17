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
