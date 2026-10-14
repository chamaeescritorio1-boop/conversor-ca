import sys, json, re, unicodedata, io, zipfile
raw = open(sys.argv[1], 'rb').read()
if raw[:2] == b'PK':
    z = zipfile.ZipFile(io.BytesIO(raw)); name = max(z.namelist(), key=lambda n: z.getinfo(n).file_size); raw = z.read(name)
try: txt = raw.decode('utf-8')
except UnicodeDecodeError: txt = raw.decode('cp1252', errors='replace')
lines = txt.splitlines()
sep = '|' if lines[0].count('|') > lines[0].count(';') else ';'
norm = lambda s: unicodedata.normalize('NFD', s or '').encode('ascii', 'ignore').decode().upper()
FOOT = re.compile(r'CALCADO|BOTA|BOTINA|SAPATO|TENIS|SANDALIA|TAMANCO|COTURNO|GALOCHA|BABUCHE')
h = [re.sub(r'[^A-Z]', '', norm(x)) for x in lines[0].split(sep)]
def f(*ns):
    for n in ns:
        for i, x in enumerate(h):
            if n in x: return i
    return -1
idx = dict(ca=f('REGISTROCA', 'NRCA'), v=f('VALIDADE'), s=f('SITUACAO'), f=f('RAZAOSOCIAL', 'FABRICANTE'), n=f('NOMEEQUIPAMENTO', 'EQUIPAMENTO'), d=f('DESCRICAO'), r=f('REFERENCIA'), cor=f('COR'), ap=f('APROVADOPARA'))
if idx['ca'] < 0: idx['ca'] = 0
print('header', h, idx, file=sys.stderr)
m = {}
for line in lines[1:]:
    p = line.split(sep)
    g = lambda k: p[idx[k]].strip() if 0 <= idx[k] < len(p) else ''
    try: ca = str(int(g('ca')))
    except ValueError: continue
    nome, desc = g('n'), g('d')
    if not FOOT.search(norm(nome) + ' ' + norm(desc[:80])): continue
    ap = g('ap')
    if ca not in m:
        m[ca] = dict(c=ca, v=g('v'), s=g('s'), f=g('f'), n=nome, d=desc + (' | Aprovado para: ' + ap if ap else ''), r=g('r'), cor=g('cor'))
    elif ap and ap[:40] not in m[ca]['d'] and len(m[ca]['d']) < 1200:
        m[ca]['d'] += ' | ' + ap
json.dump(list(m.values()), open(sys.argv[2], 'w'), ensure_ascii=False, separators=(',', ':'))
print(len(m), 'CAs de calçados', file=sys.stderr)
