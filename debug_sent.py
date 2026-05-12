#!/usr/bin/env python3
"""Debug sentence and phrase parsing."""
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

# Debug sentences
print("=== catalogue_sentence elements ===")
sent_elems = soup.select('.catalogue_sentence')
for i, elem in enumerate(sent_elems):
    text = elem.get_text(strip=True)
    print(f"  [{i}] raw text (first 500 chars): {text[:500]}")

# Debug phrases - find any element containing "phrase" in class
print("\n=== Looking for phrase containers ===")
for cls in ['.phrs-content', '.collins-phrases', '.phrase-item', '.phrase']:
    items = soup.select(cls)
    print(f"  {cls}: {len(items)} elements")
    for item in items[:3]:
        print(f"    text: {item.get_text(strip=True)[:100]}")

# Try broader phrase search
print("\n=== All elements with 'phr' in class ===")
all_phr = soup.select('[class*="phr"]')
for ap in all_phr[:5]:
    print(f"  class={ap.get('class')} text={ap.get_text(strip=True)[:80]}")

# Try to find sentences differently
print("\n=== Elements with 'sentence' in class ===")
sent_cls = soup.select('[class*="sent"]')
for sc in sent_cls[:5]:
    print(f"  class={sc.get('class')} text={sc.get_text(strip=True)[:80]}")

# Try to save HTML snippet for inspection
print("\n=== Looking at word-exp elements that contain sentences ===")
exp_elems = soup.select('.word-exp')
non_pos_count = 0
for elem in exp_elems:
    text = elem.get_text(strip=True)
    m = re.match(r'^(n\.|v\.|adj\.|adv\.|prep\.|conj\.|pron\.|interj\.|art\.|num\.|modal\s*v\.|aux\.\s*v\.|det\.|int\.)', text, re.IGNORECASE)
    if not m and non_pos_count < 5:
        print(f"  non-POS: {text[:100]}")
        non_pos_count += 1