# Sincroniza fichas técnicas (PDF) e imagens (JPG/PNG) da pasta pública do Google Drive.
# Arquivos identificados pelo código SAP (6 dígitos, ex.: 701318) no nome.
import re, json, os, io, urllib.request
from PIL import Image
ROOT = os.environ.get('DRIVE_FOLDER', '1I4TqT6SbzB_KhCrWcuRLCRDHJaNjlfCv')
UA = {'User-Agent': 'Mozilla/5.0'}
def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r: return r.read()
def listar(fid):
    h = get(f'https://drive.google.com/embeddedfolderview?id={fid}#list').decode('utf8', 'ignore')
    itens = re.findall(r'<a href="(https://drive\.google\.com/[^"]+)"[^>]*>.*?<div class="flip-entry-title">(.*?)</div>', h, re.S)
    return [(u.replace('&amp;', '&'), re.sub('<[^>]+>', '', n).strip()) for u, n in itens]
fichas = {}; imagens = 0; pastas = [(ROOT, '')]
os.makedirs('img', exist_ok=True)
while pastas:
    fid, nomep = pastas.pop()
    for url, nome in listar(fid):
        m = re.search(r'/folders/([\w-]+)', url)
        if m: pastas.append((m.group(1), nome)); continue
        m = re.search(r'/file/d/([\w-]+)', url); cod = re.search(r'(?<!\d)([78]\d{5})(?!\d)', nome)
        if not m or not cod: continue
        fid2, cod = m.group(1), cod.group(1)
        if nome.lower().endswith('.pdf'):
            fichas.setdefault(cod, fid2)
        elif re.search(r'\.(jpe?g|png|webp)$', nome, re.I):
            dest = f'img/{cod}.jpg'
            try:
                im = Image.open(io.BytesIO(get(f'https://drive.google.com/uc?export=download&id={fid2}'))).convert('RGB')
                im.thumbnail((500, 500)); bg = Image.new('RGB', (500, 500), 'white'); bg.paste(im, ((500-im.width)//2, (500-im.height)//2))
                bg.save(dest, quality=82); imagens += 1
            except Exception as e: print('falha imagem', nome, e)
# Para modelos sem imagem, extrai a foto da própria ficha técnica (maior imagem do PDF)
import fitz
extraidas = 0
for cod, fid2 in fichas.items():
    dest = f'img/{cod}.jpg'
    if os.path.exists(dest): continue
    try:
        doc = fitz.open(stream=get(f'https://drive.google.com/uc?export=download&id={fid2}'), filetype='pdf')
        best = None
        for pg in doc:
            for x in pg.get_images(full=True):
                pix = fitz.Pixmap(doc, x[0])
                if pix.n - pix.alpha >= 4: pix = fitz.Pixmap(fitz.csRGB, pix)
                if pix.width < 150 or pix.height < 150: continue
                if not best or pix.width * pix.height > best.width * best.height: best = pix
        if not best: continue
        im = Image.open(io.BytesIO(best.tobytes('png'))).convert('RGB')
        im.thumbnail((500, 500)); bg = Image.new('RGB', (500, 500), 'white'); bg.paste(im, ((500-im.width)//2, (500-im.height)//2))
        bg.save(dest, quality=82); extraidas += 1
    except Exception as e: print('falha ficha', cod, e)
print('imagens extraídas das fichas:', extraidas)
json.dump(fichas, open('fichas.json', 'w'), separators=(',', ':'))
print(f'fichas: {len(fichas)} | imagens: {imagens}')
