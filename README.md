# NOiNA — noina.tv

Portfolio site for Noi Navve: a retro CRT television you change channels on.
Channel 00 is the station ID; channels 01–17 each play a project video.
The remote drags up and down, the decoder strip shows what's tuned in, and
SYS. INFO opens a terminal-style about page.

## Running it

It's a static site — no build step. Serve the directory:

```sh
python3 -m http.server 8000
# then open http://localhost:8000/
```

Opening `index.html` over `file://` will not work: the runtime fetches the
page's own source and the `<image-slot>` state sidecar over HTTP.

## How it's put together

`index.html` is a **Design Canvas document**, not hand-written HTML. It has two
halves:

- a `<x-dc>` template using `{{ }}` bindings, `<sc-if>` conditionals and
  `ref="{{ … }}"` callback refs;
- a `<script type="text/x-dc" data-dc-script>` holding a
  `class Component extends DCLogic` with React-style `state`, `setState` and
  lifecycle methods.

`support.js` is the runtime that makes that work. It loads React 18 UMD from
unpkg, compiles the template to React elements, and mounts the component into
a `#dc-root` div that replaces `<x-dc>`. It boots itself on `DOMContentLoaded`
— nothing else has to call it.

To edit the page, edit the template and the component class in `index.html`.
Do not hand-edit `support.js` or `image-slot.js`; both are generated upstream.

| File | Role |
|---|---|
| `index.html` | The page: template + component logic + SEO/schema head |
| `support.js` | Design Canvas runtime (generated — do not edit) |
| `image-slot.js` | `<image-slot>` custom element, used for the SYS. INFO photo (generated — do not edit) |
| `cms.html` | Channel line-up manager (a second Design Canvas document) |
| `projects-data.js` | Factory line-up the CMS seeds itself from |
| `coins-data.js` | The 37 client logos for the bouncing coin in the CLIENTS box |
| `assets/` | Artwork, fonts, audio, video — see `assets/README.md` |
| `assets/lottie/` | The remote's four button animations, and the four fingerprints left on the glass |
| `vendor/lottie_light.min.js` | Lottie player 5.12.2, self-hosted |

### Runtime dependencies

Fetched from the network at load time, so the page needs internet:

- React + ReactDOM 18.3.1 (unpkg, SRI-pinned)
- Google Fonts: Poppins, VT323, Jersey 10
- The channel videos, from the R2 bucket named by `VIDEO_BASE` in `index.html`

React can be self-hosted instead by setting `window.__resources` to a map of
CDN URL → local path in a script tag **before** `support.js` loads; the runtime
checks it and prefers the local copy.

## The channel videos

Each channel plays a plain MP4 from our own bucket, in the browser's own
`<video>` element — there is no third-party player. `VIDEO_BASE` in `index.html`
holds the bucket URL; each channel's `file` field holds its filename.

**The filename is data, not derived from the title.** Renaming a project must
never break its video, so the two are kept independent. The CMS has a *Video
file* field so a publish round-trip carries it.

A channel change is: load, wait for the file's index, seek to a random point,
play — and only then is the picture revealed. Seeking *before* playback matters:
start playing first and the browser fills its buffer from frame zero, then
throws all of it away the moment the playhead moves. One fill, not two, and no
visible jump. The screen stays black through the wait, which is the point.

Files are encoded 960x540, H.264, ~800 kbps, AAC 96 kbps, keyframes every 2s,
and **must** be exported "web optimized" (the index at the front of the file).
Without that the browser has to download the whole file before showing a frame.

## The channel line-up

Channels are defined by `CHANNELS_BUILTIN` in the component script. Channel
numbers are always derived from list order, so reordering the list renumbers
the dial.

The CMS at **`/cms.html`** overrides that line-up. It lets you reorder channels
by drag, hide them, edit every field, duplicate, delete and preview, then
Publish. The page reads `localStorage` key `noina_cms_projects_v1`, and if it
holds a non-empty array, that replaces the built-in project list. It also
listens for `storage` events, so publishing in another tab updates the dial
live. The station ID (00) always comes from the built-in list and can't be
overridden; entries marked `hidden: true` are dropped.

The CMS must be served from the **same origin** as the site — `localStorage` is
per-origin, so a CMS on a different host writes a key the site never sees.

### Publishing, and the bucket

The line-up has three sources, in order of authority:

1. **`channels.json` in the bucket** — what every visitor sees.
2. **`localStorage`** — what *this* browser sees, from the CMS's Publish button.
3. **`CHANNELS_BUILTIN`** — the floor, if the fetch fails.

So Publish is a preview: it changes the publisher's own browser and nobody
else's. To change the site for everyone, use **↓ CHANNELS.JSON** in the CMS and
upload that file to the bucket. No deploy, no git — the next visitor gets it.

The fetch carries a per-minute timestamp, because R2 caches hard and an edit
that takes an hour to show is worse than none. Worst case the site is a minute
behind.

Slogans and client logos work the same way: the CMS publishes them to
`noina_cms_taglines_v1` and `noina_cms_coins_v1` for this browser, and
`channels.json` carries the slogans for everyone. Logo *artwork* is never stored
in either — that lives in `coins-data.js`, and the CMS only decides which are on
the shelf and in what order. A name it no longer recognises is dropped, so
deleting artwork can't leave a hole.

### The remote's buttons

The four buttons — mute, info, channel up, channel down — are Lottie clips, not
CSS. Each is loaded once from `assets/lottie/` and driven by frame range:

| Button | Behaviour | Segments |
|---|---|---|
| Mute | Toggle, idles at frame 0 (unmuted) or 60 (muted) | `[61,120]` to mute, `[1,60]` to unmute |
| Info | Toggle, idles at 0 (closed) or 60 (open) | `[61,120]` to open, `[1,60]` to close |
| Channel up / down | Momentary — starts and ends at idle | `[0,60]` |

The info segments are the reverse of what the frame labels suggest; the numbers
above were checked against the rendered animation.

Each button's clickable area is a plain `div` sized to the *hitbox*, with the
Lottie player centred inside it at its larger native size and set to
`pointer-events: none`. The clip is deliberately bigger than the button so
squash-and-stretch never clips, and the transparent margin must not steal
clicks from the button next to it.

Every press also runs `kickRemote()`, a small spring that dips the whole shell
and bounces back. It writes to its own wrapper element, because the outer shell's
`transform` is already owned by the open/close drag.

The player is **self-hosted** in `vendor/`. The buttons are the site's only
controls, so they don't depend on a third-party CDN staying up.

### The ambient glow, and its palette

The television casts light onto its own chassis. The layer sits *under* the
matte, so the picture hides its centre and only the spill reads, and it blends
with `screen`, so it adds light rather than tinting.

Its colour is **sampled from the picture itself**. The video is drawn to a 4×2
canvas about eleven times a second, each column averaged, the result saturated
back up and eased toward, then written as a gradient. Add `?debug=glow` to the
URL for a badge saying which source is live.

That needs two things at once: CORS headers on the bucket *and* `crossOrigin`
on the `<video>`. Setting `crossOrigin` against a host that sends no headers
makes the video fail to load outright, so the page sends a one-byte range
request first and only opts in if that comes back with the headers. If it does
not — or the canvas ends up tainted anyway — the glow falls back to the palette
below, and the picture still plays.

**So the bucket's CORS policy must list every origin the site is served from:
`https://noina.tv` and any Vercel preview URL.** Miss one and the glow quietly
drops to the palette there.

Each channel can also carry a `palette` of **up to four hex colours**, set per
channel in the CMS, used as that fallback:

| Colours | What the glow does |
|---|---|
| 2–4 | Drifts through them in a seamless loop |
| 1 | Steady wash in that colour |
| none | Falls back to the station's own wash |

The drift slides `background-position` across a gradient — no images, no canvas,
no per-frame JavaScript. Values are validated against a strict six-digit hex
before they reach CSS.

Each CMS swatch has a **screen eyedropper** beside it. That is the browser's own
`EyeDropper` API: a manual, one-shot sample taken by clicking anywhere on
screen, including a playing video. It returns a single colour at that instant
and never updates. It works because the *browser* reads the pixel and hands over
only the result — the page never gets pixel access. Chromium only; elsewhere the
button is disabled and the colour input beside it is used instead.

> Sampling was impossible while the player was a cross-origin `<iframe>` — no
> API can read pixels out of one. It only became available once the channels
> became our own `<video>` elements.

### Two copies of the line-up

The project list currently lives in two places, and they must be kept in step:

- `CHANNELS_BUILTIN` in `index.html` — what visitors see
- `NOINA_PROJECTS_DEFAULT` in `projects-data.js` — what the CMS seeds from and
  what its "restore factory line-up" button resets to

They are identical today (verified field by field). When you bake in an exported
line-up, update **both**, or the CMS and the live site will drift apart.

## Interaction

| Key | Does |
|---|---|
| ↑ / ↓ | Change channel |
| Space | Raise or lower the remote |
| i | Open / close the description drawer |
| m | Mute |

Tapping the SYS. INFO portrait plays a short clip over it, with sound, and the
still returns when the clip ends. The video is mounted with the page and
pre-decoded, and `play()` is called straight from the click — both because the
tap should be answered instantly and because iOS only allows a video with sound
to start inside the gesture itself.

The page is pinned to the viewport — `position:fixed`, `overflow:hidden`,
`touch-action:none` — and pinch gestures are refused outright, because iOS
stopped honouring `user-scalable` years ago. A television does not pan or zoom,
and the document scrolling underneath was what stole the drag from the SYS. INFO
panel. The two places that genuinely scroll, that panel and the description
drawer, opt back in with `touch-action:pan-y` and contain their own overscroll.

Tapping the chassis knocks the set from the side you hit — only the dominant
axis moves, so the edge you touch decides whether it rocks side to side or up
and down — and breaks the picture while it wobbles.

That break is an SVG filter (`#tv-glitch`), not the usual CSS glitch. The CSS
technique duplicates its content into `::before`/`::after` and slices the copies
with `clip-path`, which cannot work here: the content is a playing `<video>` and
a pseudo-element cannot hold one. An SVG filter applies to whatever it is put
on, and is the only route to a real channel split rather than a coloured
overlay. `feTurbulence` runs at low frequency across x and high down y, so the
noise barely varies along a row but jumps between rows — that is what tears the
picture into shifted bands instead of smearing it. The picture is then separated
into red and cyan, pushed apart and screen-blended back; at zero offset that
recombines to the original, so the filter is free when idle.

It is driven by the knock's own spring — by its *energy*, which starts full at
the impact and only falls. Position and velocity both cross zero on every swing,
which made the picture heal and break again four times over.

Tapping the glass leaves a fingerprint at that point: one of the four clips in
`assets/lottie/`, at a random angle, screen-blended because the exported
gradient runs white to black rather than to transparent. If the file isn't
there the tap is simply inert.

Every one of these has a sound, and they all **ignore the mute button** on
purpose. That button is the television's volume; these are the sounds of the
room — the set knocked (`assets/tv-knock.mp3`), a finger on the glass
(`assets/screen-tap-0N.mp3`), and each remote button's own click
(`assets/remote-*.mp3`, named for the button it belongs to). They answer to the
visitor's device volume instead.

### Picture brightness

`--screen-lift` and `--scanline` in the stylesheet are the two knobs. Measured
against a flat grey card behind the whole effect stack: it used to pass 81% of
the light at the centre and 76% at the edges; it now passes 98% and 84%. Raise
`--screen-lift` for a brighter tube, set it to 1 and `--scanline` to 0.25 for
exactly the old look.

## Status

Both pages are fully wired and verified in a browser: channel changes, the
video player, the description panel, mute, and the SYS. INFO page (typewriter,
pixel-reveal photo, bouncing client logos, BACK). The CMS round-trip is
verified too — hiding a channel and publishing drops it from the dial and
renumbers the remaining channels, and a palette set in the CMS reaches the glow
as a drifting gradient.

All of `assets/` is the real artwork and `coins-data.js` holds the 37 real
client logos. Nothing in the project is a placeholder any more.

`assets/README.md` has the full asset inventory.
