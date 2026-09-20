# Snekkers Games

A minimal, responsive one-page website for **Snekkers Games**, prepared for **https://snekkersgames.com**.

Plain HTML and CSS. No framework, package installation, build step, external fonts, JavaScript, or tracking.

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
- **Browser icon:** `assets/favicon.svg`.
- **Custom domain:** `CNAME`, the canonical/Open Graph URLs in `index.html`, and GitHub Pages settings.

Nudge links to its Steam page. Break the Planet has a non-clickable “Coming soon” label; replace that label with a game link when its store page is ready. The header and footer link to `info@snekkersgames.com`, and the footer includes the studio’s YouTube and X accounts. The footer year is plain text in `index.html`.
