# Assets

The site renders end-to-end with what is in this folder, but most of it is
**placeholder artwork generated to stand in for the real files**. Swap each one
for the real asset at the same path and filename — nothing else needs to change.

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

## Still missing

These are referenced by the page but not included. Each one degrades
gracefully — the site works without them, it just loses that flourish.

| File | Used for | What happens without it |
|---|---|---|
| `segment7.woff2` | 7-segment LCD face for the channel number in the decoder | Falls back to `monospace`; the number still reads correctly. The `<link rel="preload">` in the head 404s until the font is added. |
| `static-noise-transition.mp4` | Full-screen static burst when entering/leaving SYS. INFO | The transition still completes on its safety timer (~450ms), but flashes black instead of static. |
| `static-click.mp3` | Channel-change click | Silent. |
| `loading-loop.mp3` | Loop while a Vimeo channel buffers | Silent. |

## Regenerating the placeholders

`tools/gen-placeholder-assets.py` (Pillow) produced every generated file here.
It is kept only so the stand-ins can be rebuilt or tweaked; it is not part of
the site and nothing at runtime depends on it.
