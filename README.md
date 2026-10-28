# Zare Growth Pods landing page

A static, single-page site. Plain HTML, CSS and a few lines of vanilla JavaScript; no framework and no build step.

```
public/                 Everything that gets deployed
  index.html            The page
  styles.css            All styles; brand tokens are CSS variables at the top
  script.js             Booking link constant, scroll fade-in
  fonts/                Self-hosted Montserrat (300 to 800), SIL Open Font License
  assets/               Web-sized logo and Open Graph share image
  favicon.svg, favicon.ico, favicon-32.png, apple-touch-icon.png, icon-512.png
brand/                  Originals: brand guidelines PDF, full-size logos, the approved
                        single-file design (approved-index.html). Not deployed.
scripts/optimize_images.py   Regenerates public/assets and the favicons from brand/
```

## Run locally

Any static file server works. With Python:

```bash
python3 -m http.server 8000 --directory public
```

Then open http://localhost:8000.

## Deploy

**Vercel:** import the repository and deploy. `vercel.json` sets `public/` as the output directory and adds cache headers. No build command is needed.

**Netlify:** import the repository and deploy. `netlify.toml` sets `public/` as the publish directory and adds cache headers. Leave the build command empty.

**Any other static host:** upload the contents of `public/`.

## Common edits

- **Booking link:** change `BOOKING_URL` at the top of `public/script.js`. The `href` on the two booking buttons in `index.html` is a fallback for visitors without JavaScript, so update it too.
- **Brand colors:** the CSS variables in `:root` at the top of `public/styles.css`.
- **Switching to Gotham:** put the licensed `.woff2` files in `public/fonts/`, add `@font-face` rules for them at the top of `styles.css`, and move `"Gotham"` to the front of `--font`. Update the two `<link rel="preload">` tags in `index.html` to point at the Gotham files.
- **Logos and icons:** replace the originals in `brand/` and run `python3 scripts/optimize_images.py` (needs `pip install Pillow`). `public/favicon.svg` uses the paths from `brand/bolt-navy.svg` and switches to the white colorway (`bolt-white.svg`) when the browser is in dark mode; update its paths if the mark changes.

## Site URL

The page currently points its canonical link, `og:url`, `og:image` and `twitter:image` at `https://zare-growth-pod.vercel.app/`. When you move to a custom domain, replace that URL in the `<head>` of `public/index.html` (four places).
