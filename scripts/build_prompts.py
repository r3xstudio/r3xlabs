#!/usr/bin/env python3
import json, html, re
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / 'content' / 'prompts'
PROMPTS = ROOT / 'prompts'
SITE = 'https://r3xlabs.com'

CATEGORY_ORDER = [
    'Cinematic & Character',
    'Typography & 3D',
    'Product Photography',
    'Logo & Branding',
    'Illustration',
    'Ecommerce',
    'Creator Systems',
    'Analysis & Research',
]

def esc(v): return html.escape(str(v or ''), quote=True)
def para(v): return '<br><br>'.join(esc(v).replace('\n','<br>') for v in str(v or '').split('\n\n'))

def load_items():
    items=[]
    if not CONTENT.exists(): return items
    for p in sorted(CONTENT.glob('*.json')):
        try:
            d=json.loads(p.read_text(encoding='utf-8'))
            if d.get('published', True): items.append(d)
        except Exception as e:
            print(f'Skip {p}: {e}')
    return items

def render_page(d):
    slug=d['slug'].strip()
    title=d['title'].strip()
    category=d.get('category','Creator Systems')
    desc=d.get('description','')
    image=d.get('image','')
    prompt=d.get('prompt','')
    negative=d.get('negative_prompt','')
    why=d.get('why_it_works','')
    uses=d.get('best_use_cases','')
    seo_title=d.get('seo_title') or f'{title} — AI Prompt & Result — R3X Labs'
    meta=d.get('meta_description') or desc
    published=d.get('published_date') or str(date.today())
    canonical=f'{SITE}/prompts/{slug}/'
    og=f'<meta property="og:image" content="{SITE}{esc(image)}">' if image else ''
    img=(f'<figure style="margin:0 0 2rem"><img src="{esc(image)}" alt="{esc(d.get("image_alt") or title)}" style="display:block;max-width:720px;width:100%;height:auto;margin:0 auto;border-radius:20px"><figcaption style="margin-top:.75rem;opacity:.72">Generated result from the prompt below.</figcaption></figure>' if image else '<p class="article-deck">No result image uploaded yet.</p>')
    neg=(f'<h2 id="negative">Negative prompt</h2><div class="prompt-box"><strong>NEGATIVE PROMPT</strong><br><br>{para(negative)}</div>' if negative else '')
    negtoc='<a href="#negative">Negative prompt</a>' if negative else ''
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(seo_title)}</title><meta name="description" content="{esc(meta)}"><link rel="canonical" href="{canonical}"><meta property="og:title" content="{esc(title)} — AI Prompt & Result"><meta property="og:description" content="{esc(meta)}"><meta property="og:type" content="article"><meta property="og:url" content="{canonical}">{og}<meta name="twitter:card" content="summary_large_image"><link rel="stylesheet" href="/styles.css"><script async src="https://www.googletagmanager.com/gtag/js?id=G-JB53B9JR87"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-JB53B9JR87');</script></head><body><header class="site-header"><a class="brand" href="/"><span class="brand-mark">R3X</span><span class="brand-sub">LABS</span></a><nav class="nav"><a href="/tools/">Tools</a><a href="/guides/">Guides</a><a href="/prompts/">Prompts</a><a href="/signal/">Signal</a></nav></header><main><article class="article-shell"><header class="article-hero"><div class="eyebrow">R3X LABS / PROMPT SHOWCASE / {esc(category).upper()}</div><h1>{esc(title)}</h1><p class="article-deck">{esc(desc)}</p><div class="article-meta">Published {esc(published)} · Prompt Showcase</div></header><div class="article-layout"><aside class="article-toc"><span class="panel-label">ON THIS PAGE</span><a href="#result">Generated result</a><a href="#prompt">Full prompt</a>{negtoc}<a href="#why">Why it works</a><a href="#use">Best use cases</a></aside><div class="article-body"><h2 id="result">Generated result</h2>{img}<h2 id="prompt">Full prompt</h2><div class="prompt-box"><strong>PROMPT</strong><br><br>{para(prompt)}</div>{neg}<h2 id="why">Why it works</h2><p>{para(why)}</p><h2 id="use">Best use cases</h2><p>{para(uses)}</p></div></div></article></main><footer><div><strong>R3X LABS</strong><br><span>Build What's Next.</span></div><div>© 2026 R3X Labs</div></footer></body></html>'''

def render_index(items):
    groups={c:[] for c in CATEGORY_ORDER}
    for d in items: groups.setdefault(d.get('category','Creator Systems'),[]).append(d)
    sections=[]; n=1
    for cat in CATEGORY_ORDER:
        ds=groups.get(cat,[])
        if not ds: continue
        cards=''.join(f'<a class="guide-card-link" href="/prompts/{esc(d["slug"])}/"><article class="card"><span class="status">PROMPT</span><h3>{esc(d["title"])}</h3><p>{esc(d.get("description",""))}</p></article></a>' for d in sorted(ds,key=lambda x:x.get('published_date',''), reverse=True))
        sections.append(f'<section class="grid-section"><div class="section-head"><span>{n:02d}</span><h2>{esc(cat).upper()}</h2></div><div class="card-grid">{cards}</div></section>'); n+=1
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Prompts — R3X Labs</title><meta name="description" content="Reusable AI prompt systems organized by category: cinematic image generation, typography, ecommerce, creator workflows and analysis."><link rel="canonical" href="https://r3xlabs.com/prompts/"><link rel="stylesheet" href="/styles.css"><script async src="https://www.googletagmanager.com/gtag/js?id=G-JB53B9JR87"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag(\'js\',new Date());gtag(\'config\',\'G-JB53B9JR87\');</script></head><body><header class="site-header"><a class="brand" href="/"><span class="brand-mark">R3X</span><span class="brand-sub">LABS</span></a><nav class="nav"><a href="/tools/">Tools</a><a href="/guides/">Guides</a><a href="/prompts/">Prompts</a><a href="/signal/">Signal</a></nav></header><main><section class="hero"><div><div class="eyebrow">R3X LABS / PROMPTS</div><h1>PROMPTS.</h1><p class="hero-copy">Reusable prompt frameworks organized by visual discipline and workflow — built for repeatable results, not random one-off commands.</p></div></section>'+''.join(sections)+'</main><footer><div><strong>R3X LABS</strong><br><span>Build What\'s Next.</span></div><div>© 2026 R3X Labs</div></footer></body></html>'

def update_sitemap(items):
    p=ROOT/'sitemap.xml'
    if not p.exists(): return
    text=p.read_text(encoding='utf-8')
    for d in items:
        url=f'{SITE}/prompts/{d["slug"]}/'
        if url not in text:
            entry=f'  <url><loc>{url}</loc><lastmod>{d.get("published_date") or date.today()}</lastmod><changefreq>monthly</changefreq><priority>0.8</priority></url>\n'
            text=text.replace('</urlset>', entry+'</urlset>')
    p.write_text(text,encoding='utf-8')

def main():
    items=load_items(); PROMPTS.mkdir(exist_ok=True)
    for d in items:
        out=PROMPTS/d['slug']/ 'index.html'; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(render_page(d),encoding='utf-8')
    (PROMPTS/'index.html').write_text(render_index(items),encoding='utf-8')
    update_sitemap(items)
    print(f'Built {len(items)} prompt(s).')
if __name__=='__main__': main()
