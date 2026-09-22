# Snekkers Games

A dark, responsive website for **Snekkers Games**, prepared for **https://snekkersgames.com**.

Static HTML and CSS, with a small JavaScript enhancement for press-kit image previews and section navigation. No framework, package installation, external fonts, or tracking.

## Preview locally

Open `index.html` in a browser, or serve this folder:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```
 
Then visit <http://localhost:8000>.

## Publish with GitHub Pages

Repository: [snekkers-game/snekkers-games](https://github.com/snekkers-game/snekkers-games).

1. Open the repository’s [**Settings → Pages**](https://github.com/snekkers-game/snekkers-games/settings/pages).
2. Under **Build and deployment**, select **Deploy from a branch**, then **main** and **/ (root)**. Save.
3. Under **Custom domain**, enter `snekkersgames.com` and save. The included `CNAME` file preserves the domain in the source; it does not replace this settings step.
4. Configure DNS as described below, then enable **Enforce HTTPS** when GitHub makes it available.

Subsequent pushes to `main` publish your changes automatically. No custom Actions workflow is needed.

To publish future edits after enabling Pages, run these commands from this folder:

```sh
git add .
git commit -m "Update Snekkers Games website"
git push
```

[GitHub’s publishing instructions](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site).

## Connect snekkersgames.com

Add the custom domain in GitHub Pages settings **before** changing DNS. At your domain’s DNS provider, set:

| Type | Host / name | Value |
| --- | --- | --- |
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `snekkers-game.github.io` |

The `www` CNAME points to the GitHub account’s domain without the repository name. Replace conflicting web-hosting records for `@` or `www`, preserving unrelated email and verification records.

GitHub redirects `www.snekkersgames.com` to `snekkersgames.com` when both are configured. DNS propagation and HTTPS availability can take up to 24 hours.

[GitHub’s custom-domain instructions](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site).

## Edit the site

- **Content and links:** `index.html`.
- **Colors and layout:** `styles.css`. The core colors are at the top in `:root`.
- **Game artwork:** `assets/nudge.png` and `assets/break-the-planet.png`.
- **Browser icon:** `assets/favicon.svg`.
- **Custom domain:** `CNAME`, the canonical/Open Graph URLs in `index.html`, and GitHub Pages settings.

Both game cards link to their press kits. Nudge also links to its Steam page. The header and footer link to `info@snekkersgames.com`, and the footer includes the studio’s YouTube and X accounts. The footer year is plain text in `index.html`.

## Press kits

- `/press-kit/nudge/` and `/press-kit/break-the-planet/` are complete static pages.
- Edit `press-kit/games.json` for facts, pitch, description, features, credits, trailer links, and asset collections. Nudge game details are sourced from its Steam page; its supplied screenshots, artwork, and logo are included; credits are stored but hidden. Break the Planet still uses mock details. Set `mock` to `false` only after replacing mock details and assets with approved content.
- Add media entries with `file` (repository-relative), `title`, and `alt` to `artwork`, `screenshots`, or `logos`. Trailer entries use `title` and `url`; add `youtube_id` and an optional `start` time in seconds for a responsive YouTube embed.
- Run `python3 scripts/build_press_kits.py` after changes. This regenerates both HTML pages and per-category/full asset ZIP downloads using only the Python standard library. Commit the generated files; hosting does not need Python.
- Shared layout and interactions: `press-kit/press-kit.css` and `press-kit/press-kit.js`. Images open in a keyboard-accessible dialog; original image links and all downloads also work without JavaScript.
