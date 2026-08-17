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
renumbers the remaining channels.

All of `assets/` is the real artwork and `coins-data.js` holds the 37 real
client logos. Nothing in the project is a placeholder any more.

`assets/README.md` has the full asset inventory.
