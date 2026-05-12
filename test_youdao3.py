#!/usr/bin/env python3
import urllib.request
from bs4 import BeautifulSoup

url = 'https://www.youdao.com/result?word=free&lang=en'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req, timeout=15)
html = resp.read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')

# Find "词源" in text and show parent context
for tag in soup.find_all(string=lambda t: t and '词源' in str(t)):
    parent = tag.parent
    context = parent.get_text(strip=True)[:300]
    print(f"Etymology context: {context}")
    print(f"Tag: {parent.name}, class: {parent.get('class','?')}")
    print("---")

# Check word forms with correct selectors
for sel in ['.word-wfs-cell-less', '.word-wfs-less', '.word-wfs', '.transformation']:
    items = soup.select(sel)
    if items:
        print(f"\nSelector '{sel}': {len(items)} items")
        for item in items[:10]:
            print(f"  {item.get_text(strip=True)[:80]}")

# Check phrases more carefully
for item in soup.select('.phrs-content .phrase'):
    en = item.select_one('.phrase-en, .en, .word')
    cn = item.select_one('.phrase-cn, .cn, .trans')
    print(f"Phrase: {item.get_text(strip=True)[:80]}")