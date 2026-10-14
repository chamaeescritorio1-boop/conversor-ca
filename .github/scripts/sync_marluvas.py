# Completa imagens faltantes com a foto do site oficial da Marluvas (loja Shopify).
# Só baixa para códigos SAP que ainda não têm imagem; não substitui as existentes.
import json, os, re, io, urllib.request
from PIL import Image
UA = {'User-Agent': 'Mozilla/5.0'}
def get(u):
    with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60) as r: return r.read()
refs = json.load(open('catalogo-refs.json'))
norm = lambda s: re.sub(r'[^A-Z0-9]', '', str(s).upper())
prods = []
for pg in range(1, 30):
    d = json.loads(get(f'https://www.marluvas.com.br/products.json?limit=250&page={pg}'))['products']
    prods += d
    if len(d) < 250: break
by_sku, by_ref = {}, {}
for p in prods:
    if not p.get('images'): continue
    src = p['images'][0]['src']
    for v in p['variants']:
        if v.get('sku'): by_sku.setdefault(str(v['sku']).strip(), src)
    m = re.search(r'\(([^)]+)\)\s*$', p['title'])
    if m: by_ref.setdefault(norm(m.group(1)), src)
novas = 0
for cod, ref in refs.items():
    dest = f'img/{cod}.jpg'
    if os.path.exists(dest): continue
    src = by_sku.get(cod) or by_ref.get(norm(ref))
    if not src: continue
    try:
        im = Image.open(io.BytesIO(get(src.split('?')[0] + '?width=600'))).convert('RGBA')
        bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3]); im = bg
        im.thumbnail((500, 500)); out = Image.new('RGB', (500, 500), 'white'); out.paste(im, ((500-im.width)//2, (500-im.height)//2))
        out.save(dest, quality=82); novas += 1; print('nova', cod, ref)
    except Exception as e: print('falha', cod, e)
print(f'produtos no site: {len(prods)} | imagens novas: {novas}')
