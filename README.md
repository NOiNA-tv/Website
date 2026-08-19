# NOiNA — noina.tv

Portfolio site for Noi Navve: a retro CRT television you change channels on.
Channel 00 is the station ID; channels 01–17 each play a project from Vimeo.
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
| `assets/lottie/` | The remote's four button animations |
| `vendor/lottie_light.min.js` | Lottie player 5.12.2, self-hosted |

### Runtime dependencies

Fetched from the network at load time, so the page needs internet:

- React + ReactDOM 18.3.1 (unpkg, SRI-pinned)
- Vimeo Player API (`player.vimeo.com`)
- Google Fonts: Poppins, VT323, Jersey 10

React can be self-hosted instead by setting `window.__resources` to a map of
CDN URL → local path in a script tag **before** `support.js` loads; the runtime
checks it and prefers the local copy.

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

### Publishing is per-browser

This is the important limitation. **Publish writes to the publisher's own
browser and nothing else.** Visitors get whatever `CHANNELS_BUILTIN` says; they
do not see a published line-up. Treat the CMS as an authoring and preview tool.

To make a line-up permanent for everyone: use **Import / Export** in the CMS to
copy the JSON out, then bake it into the source.

### The remote's buttons

The four buttons — mute, info, channel up, channel down — are Lottie clips, not
CSS. Each is loaded once from `assets/lottie/` and driven by frame range:

| Button | Behaviour | Segments |
|---|---|---|
| Mute | Toggle, idles at frame 0 (muted) or 60 (unmuted) | `[61,120]` to mute, `[1,60]` to unmute |
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

The television casts light onto its own chassis. That layer is the poster image
itself — solid colour edge to edge, shaped like the tube and blurred hard —
sitting *under* the matte, so the picture hides its centre and only the spill
reads. It blends with `screen`, so it adds light rather than tinting.

Each channel can carry a `palette` of **up to four hex colours**, set per
channel in the CMS:

| Colours | What the glow does |
|---|---|
| 2–4 | Drifts through them in a seamless loop |
| 1 | Steady wash in that colour |
| none | Falls back to the channel's Vimeo poster frame |

The drift slides `background-position` across a gradient — no images, no canvas,
no per-frame JavaScript. Values are validated against a strict six-digit hex
before they reach CSS.

Each CMS swatch has a **screen eyedropper** beside it. That is the browser's own
`EyeDropper` API: a manual, one-shot sample taken by clicking anywhere on
screen, including a playing video. It returns a single colour at that instant
and never updates. It works because the *browser* reads the pixel and hands over
only the result — the page never gets pixel access. Chromium only; elsewhere the
button is disabled and the colour input beside it is used instead.

> A glow that tracks the video frame by frame is not possible while the player
> is a Vimeo `<iframe>`. Canvas sampling needs a `<video>` element, and there is
> no API that lets a page read pixels out of a cross-origin iframe. It would
> require self-hosting the video files.

### Two copies of the line-up

The project list currently lives in two places, and they must be kept in step:

- `CHANNELS_BUILTIN` in `index.html` — what visitors see
- `NOINA_PROJECTS_DEFAULT` in `projects-data.js` — what the CMS seeds from and
  what its "restore factory line-up" button resets to

They are identical today (verified field by field). When you bake in an exported
line-up, update **both**, or the CMS and the live site will drift apart.

## Status

Both pages are fully wired and verified in a browser: channel changes, the
Vimeo embeds, the description panel, mute, and the SYS. INFO page (typewriter,
pixel-reveal photo, bouncing client logos, BACK). The CMS round-trip is
verified too — hiding a channel and publishing drops it from the dial and
renumbers the remaining channels, and a palette set in the CMS reaches the glow
as a drifting gradient.

All of `assets/` is the real artwork and `coins-data.js` holds the 37 real
client logos. Nothing in the project is a placeholder any more.

`assets/README.md` has the full asset inventory.
