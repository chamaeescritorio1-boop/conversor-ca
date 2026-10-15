import json, re, time, os, sys, urllib.request
base = json.load(open('caepi.json'))
out_p = 'caepi_fotos.json'
fotos = json.load(open(out_p)) if os.path.exists(out_p) else {}
cas = [r['c'] for r in base if 'LIDO' in (r.get('s') or '').upper() and 'MARLUVAS' not in (r.get('f') or '').upper()]
todo = [c for c in cas if c not in fotos]
limit = int(os.environ.get('LIMIT', '1500')); t0 = time.time(); n = 0
print(len(cas), 'válidos;', len(todo), 'pendentes', file=sys.stderr)
for c in todo[:limit]:
    try:
        req = urllib.request.Request(f'https://consultaca.com/{c}', headers={'User-Agent': 'Mozilla/5.0 (Chamae conversor-ca; contato chamaeescritorio1)'})
        html = urllib.request.urlopen(req, timeout=20).read().decode('utf-8', 'ignore')
        urls = list(dict.fromkeys(re.findall(r'/files/fotos_ca/[\w.-]+\.(?:jpe?g|png|webp)', html, re.I)))
        fotos[c] = ['https://consultaca.com' + u for u in urls[:4]]
        n += 1
    except Exception as e:
        print(c, e, file=sys.stderr)
    time.sleep(1.2)
    if time.time() - t0 > 5000: break
json.dump(fotos, open(out_p, 'w'), separators=(',', ':'))
print(n, 'consultados;', sum(1 for v in fotos.values() if v), 'com foto', file=sys.stderr)
