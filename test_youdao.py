#!/usr/bin/env python3
import urllib.request, urllib.parse
import re
from bs4 import BeautifulSoup

url = 'https://www.youdao.com/result?word=free&lang=en'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req, timeout=15)
html = resp.read().decode('utf-8')

# Check for __NUXT__ data
m = re.search(r'window\.__NUXT__\s*=\s*(\{.*?\});\s*</script>', html, re.DOTALL)
if m:
    print("__NUXT__ found, length:", len(m.group(1)))
    # Save for debugging
    with open('/Users/allen/Downloads/人教版(PEP)/_nuxt_free.json', 'w') as f:
        f.write(m.group(1))
else:
    print("No __NUXT__ found")

soup = BeautifulSoup(html, 'html.parser')

# Check phonetic
phonetics = soup.select('.phonetic')
print(f"Phonetic: {len(phonetics)}")
for p in phonetics[:3]:
    print(f"  {p.get_text(strip=True)}")

# Check POS + trans
pos_elems = soup.select('.pos')
trans_elems = soup.select('.trans')
print(f"POS: {len(pos_elems)}, Trans: {len(trans_elems)}")
for i, (p, t) in enumerate(zip(pos_elems[:5], trans_elems[:5])):
    print(f"  {p.get_text(strip=True):12s} {t.get_text(strip=True)[:80]}")

# Check phrases
phr = soup.select('.phrs-content .word-exp, .phrs-content p')
print(f"Phrases: {len(phr)}")
for p in phr[:5]:
    print(f"  {p.get_text(strip=True)[:80]}")

# Check sentences
sent = soup.select('.catalogue_sentence')
print(f"Sentences: {len(sent)}")
for s in sent[:3]:
    cn = s.select_one('.catalogue_sentence_cn')
    en = s.select_one('.catalogue_sentence_en')
    if cn and en:
        print(f"  EN: {en.get_text(strip=True)[:80]}")
        print(f"  CN: {cn.get_text(strip=True)[:80]}")

# Check word forms
wfs = soup.select('.wfs-name, .wfs .word')
print(f"Word forms: {len(wfs)}")
for w in wfs[:5]:
    print(f"  {w.get_text(strip=True)}")

# Look for etymology in __NUXT__
if m:
    import json
    try:
        data = json.loads(m.group(1))
        # Search for etymology in the nested structure
        def find_etym(obj, path=""):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if 'etym' in k.lower() or 'origin' in k.lower():
                        print(f"  Found at {path}.{k}: {str(v)[:200]}")
                    find_etym(v, f"{path}.{k}")
            elif isinstance(obj, list):
                for i, v in enumerate(obj):
                    find_etym(v, f"{path}[{i}]")
        find_etym(data)
    except:
        print("Failed to parse __NUXT__")