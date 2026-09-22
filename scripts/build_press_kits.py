"""Generate static press kits and ZIP downloads: python3 scripts/build_press_kits.py."""
from pathlib import Path
import json
import html
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'press-kit/games.json'
esc = html.escape

def icon(kind='download'):
    paths = {'download': 'M12 3v12m-5-5 5 5 5-5M4 16v5h16v-5', 'arrow': 'M7 17 17 7M7 7h10v10', 'close': 'm6 6 12 12M6 18 18 6', 'image': 'M4 4h16v16H4zM4 16l5-5 4 4 3-3 4 4'}
    return f'<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="{paths[kind]}"/></svg>'

def link(label, href, cls='text-link', download=False):
    return f'<a class="{cls}" href="{esc(href, quote=True)}"'+(' download' if download else '')+f'>{esc(label)} {icon("download" if download else "arrow")}</a>'

def build(game):
    slug, name = game['slug'], game['name']
    dest = ROOT / 'press-kit' / slug
    dest.mkdir(parents=True, exist_ok=True)
    collections = {key: game.get(key, []) for key in ['artwork', 'screenshots', 'logos']}
    assets = [a for group in collections.values() for a in group]
    def archive(filename, items):
        with zipfile.ZipFile(dest / filename, 'w', zipfile.ZIP_DEFLATED) as z:
            unique = {a['file']: a for a in items}
            for asset_path in unique:
                z.write(ROOT / asset_path, asset_path)
        size = (dest / filename).stat().st_size / 1024 / 1024
        return f'{size:.1f} MB' if size >= .1 else f'{size * 1024:.0f} KB'
    total = archive('press-assets.zip', assets)
    def gallery(key, label):
        items = collections[key]
        if not items:
            return f'<h3>{label}</h3><p class="unannounced">{label} have not been released yet. Contact us for media requests.</p>'
        size = archive(key + '.zip', items)
        cards = ''
        for a in items:
            url = '../../' + a['file']
            cards += f'<figure class="press-asset"><a class="asset-preview" href="{esc(url)}" data-preview aria-label="Preview {esc(a["title"])}"><img src="{esc(url)}" alt="{esc(a["alt"])}" loading="lazy"/><span class="preview-hint">{icon("image")} Preview</span></a><figcaption><span>{esc(a["title"])}</span>{link("Download", url, "asset-download", True)}</figcaption></figure>'
        return f'<div class="asset-heading"><h3>{label}</h3>{link(f"Download ZIP · {size}", key+".zip", "text-link", True)}</div><div class="asset-grid asset-grid-{key}">{cards}</div>'
    facts = [('Developer & publisher', link('Snekkers Games', '../../index.html')), ('Platforms', game.get('platforms', 'Not announced')), ('Release status', game.get('status', 'Not announced')), ('Release date', game.get('release_date', 'Not announced')), ('Genres', game.get('genres', 'Not announced')), ('Price', game.get('price', 'Not announced'))]
    facts.extend((label, game[key]) for key, label in [('languages', 'Languages'), ('players', 'Players'), ('controller_support', 'Controller support')] if game.get(key))
    facts_html = ''.join(f'<div><dt>{esc(k)}</dt><dd>{v if k == "Developer & publisher" else esc(v)}</dd></div>' for k,v in facts)
    store = link('View on Steam', game['steam'], 'button primary-button') if game.get('steam') else ''
    features = '<ul class="feature-list">'+''.join(f'<li>{esc(f)}</li>' for f in game['features'])+'</ul>' if game.get('features') else '<p class="unannounced">Gameplay features will be shared when announced.</p>'
    trailers = ''
    for trailer in game.get('trailers', []):
        if trailer.get('youtube_id'):
            video_id = trailer['youtube_id']
            if len(video_id) != 11 or not all(c.isalnum() or c in '-_' for c in video_id):
                raise ValueError('Invalid YouTube video ID')
            start = max(0, int(trailer.get('start', 0)))
            trailers += f'<div class="trailer-embed"><iframe src="https://www.youtube-nocookie.com/embed/{video_id}?start={start}" title="{esc(trailer["title"], quote=True)}" width="560" height="315" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe></div>'
        trailers += f'<p>{link(trailer["title"] + " on YouTube", trailer["url"])}</p>'
    trailers = trailers or '<p class="unannounced">No public trailers yet.</p>'
    nav = ''.join(f'<a href="#{id}">{title}</a>' for id,title in [('factsheet','Factsheet'),('descriptions','Descriptions'),('media','Media'),('contact','Contact')])
    if game.get('mock') and not game.get('trailers'):
        trailers = '<div class="trailer-placeholder">'+icon('image')+'<strong>Announcement trailer</strong><span>Video placeholder · trailer coming soon</span></div>'
    description = game.get('description') or 'More game details will be shared when announced. For interviews, coverage, or additional information, please contact Snekkers Games.'
    cover = game.get('cover', game['artwork'][0])
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/><meta name="color-scheme" content="dark"/><meta name="theme-color" content="#09090c"/>
<title>{esc(name)} Press Kit — Snekkers Games</title><meta name="description" content="Official {esc(name)} press kit: game information, artwork, downloads, and press contact."/><link rel="canonical" href="https://snekkersgames.com/press-kit/{slug}/"/><meta property="og:title" content="{esc(name)} — Press Kit"/><meta property="og:image" content="https://snekkersgames.com/{cover['file']}"/><meta property="og:type" content="website"/><link rel="icon" href="../../assets/favicon.svg" type="image/svg+xml"/><link rel="stylesheet" href="../../styles.css"/><link rel="stylesheet" href="../press-kit.css"/><script src="../press-kit.js" defer></script></head>
<body><a class="skip-link" href="#main">Skip to content</a><header class="site-header"><div class="header-inner"><a class="brand" href="../../index.html" aria-label="Snekkers Games home"><img class="brand-symbol" src="../../assets/logo.svg" alt="" width="34" height="34" /><span>snekkers<span class="brand-light">games</span></span></a><nav aria-label="Main navigation"><a href="../../index.html#games">Our games</a><a class="contact-link" href="mailto:info@snekkersgames.com">Say hello {icon('arrow')}</a></nav></div></header>
<main id="main" class="container press-main"><div class="press-intro"><div><p class="eyebrow section-eyebrow">SNEKKERS GAMES / PRESS KIT</p><h1>{esc(name)}</h1><p class="press-deck">{esc(game['pitch'])}</p></div><div class="press-actions">{store}{link(f'Download press kit · {total}', 'press-assets.zip', 'button game-button', True)}</div></div>
<img class="press-cover" src="../../{cover['file']}" alt="{esc(cover['alt'])}" width="1232" height="706" fetchpriority="high"/>
<div class="press-layout"><aside class="press-sidebar"><p class="eyebrow section-eyebrow">IN THIS KIT</p><nav aria-label="Press kit sections">{nav}</nav>{link('Download all assets', 'press-assets.zip', 'text-link', True)}</aside><div class="press-content">
<section id="factsheet"><p class="section-number">01 / AT A GLANCE</p><h2>Factsheet</h2><dl class="facts-grid">{facts_html}<div><dt>Website</dt><dd>{link('snekkersgames.com', 'https://snekkersgames.com/')}</dd></div></dl></section>
<section id="descriptions"><p class="section-number">02 / THE GAME</p><h2>Descriptions</h2><h3>Pitch</h3><p>{esc(game['pitch'])}</p><h3>Description</h3><p>{esc(description)}</p><h3>Features</h3>{features}</section>
<section id="media"><p class="section-number">03 / IN PICTURES</p><h2>Media</h2><h3>Trailers</h3>{trailers}{gallery('screenshots', 'Screenshots')}{gallery('artwork', 'Key artwork')}{gallery('logos', 'Logos')}</section>
<section id="contact" class="press-contact"><p class="section-number">04 / GET IN TOUCH</p><h2>Let’s talk {esc(name)}.</h2><p>For press enquiries, interviews, review access, or additional assets.</p>{link('info@snekkersgames.com', 'mailto:info@snekkersgames.com', 'text-link')}</section>
</div></div></main><footer class="site-footer container"><div class="footer-bottom"><p>© 2026 Snekkers Games</p><a href="../../index.html">Back to our games</a></div></footer>
<dialog class="image-dialog" aria-label="Image preview"><form method="dialog"><button class="preview-close" aria-label="Close image preview">{icon('close')}</button></form><img alt=""/><a class="button game-button" download>Download original {icon()}</a></dialog>
</body></html>'''
    (dest / 'index.html').write_text(page)

for game in json.loads(DATA.read_text()):
    build(game)
