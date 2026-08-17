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
| `coins-data.js` | Client marks for the bouncing coin in the CLIENTS box |
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

A CMS can override the line-up: the page reads `localStorage` key
`noina_cms_projects_v1`, and if it holds a non-empty array, that replaces the
built-in project list. It also listens for `storage` events, so a CMS page
publishing in another tab updates the dial live. The station ID (00) always
comes from the built-in list and can't be overridden. Entries marked
`hidden: true` are dropped.

> The companion `Channels CMS.dc.html` that writes that key is not in this
> repo yet.

## Status

The page is fully wired and verified in a browser: channel changes, the Vimeo
embeds, the description panel, mute, and the SYS. INFO page (typewriter,
pixel-reveal photo, bouncing coin, BACK) all work.

All of `assets/` is the real artwork. The one stand-in left is `coins-data.js`,
whose client marks are typeset monograms rather than the real logos.

`assets/README.md` has the full inventory, and flags the 4.55 MB transition
video as the site's main page-weight problem.
