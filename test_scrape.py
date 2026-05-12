#!/usr/bin/env python3
"""Quick test of Youdao scraping."""
import urllib.request
import re
from bs4 import BeautifulSoup

word = 'free'
url = f'https://www.youdao.com/result?word={word}&lang=en'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req, timeout=15)
html = resp.read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')

# Test phonetics
ph = soup.select('.phonetic')
print('=== PHONETICS ===')
for i, p in enumerate(ph):
    print(f'  [{i}]: {p.get_text(strip=True)}')

# Test trans
exp = soup.select('.word-exp')
print('=== TRANS ===')
for e in exp:
    text = e.get_text(strip=True)[:100]
    print(f'  {text}')

# Test phrases
phr = soup.select('.phrs-content .phrase, .phrs-content p')
print('=== PHRASES ===')
for p in phr[:5]:
    print(f'  {p.get_text(strip=True)[:80]}')

# Test sentences
sent = soup.select('.catalogue_sentence')
print('=== SENTENCES ===')
for s in sent[:3]:
    print(f'  {s.get_text(strip=True)[:120]}')

# Test word forms
wfs = soup.select('.word-wfs-cell-less')
print('=== WORD FORMS ===')
for w in wfs[:5]:
    print(f'  {w.get_text(strip=True)}')

print('=== DONE ===')