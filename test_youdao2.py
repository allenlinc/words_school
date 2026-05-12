#!/usr/bin/env python3
import urllib.request
import re
from bs4 import BeautifulSoup

url = 'https://www.youdao.com/result?word=free&lang=en'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req, timeout=15)
html = resp.read().decode('utf-8')

# Save HTML for analysis
with open('/Users/allen/Downloads/人教版(PEP)/_youdao_free.html', 'w') as f:
    f.write(html)
print(f"HTML saved ({len(html)} chars)")

soup = BeautifulSoup(html, 'html.parser')

# Try multiple phrase selectors
for sel in ['.phrs-content', '.phrase', '.word-exp', '[class*=phr]', '[class*=collins]']:
    items = soup.select(sel)
    if items:
        print(f"Selector '{sel}': {len(items)} items")
        for item in items[:3]:
            print(f"  {item.get_text(strip=True)[:120]}")

# Try multiple sentence selectors
for sel in ['.catalogue_sentence', '.sentence', '[class*=sent]', '[class*=example]', '.bilingual', '[class*=catalogue]']:  
    items = soup.select(sel)
    if items:
        print(f"Selector '{sel}': {len(items)} items")
        for item in items[:2]:
            txt = item.get_text(strip=True)[:120]
            if txt:
                print(f"  {txt}")

# Try synonym selectors
for sel in ['.synonyms', '.syno', '[class*=syno]', '[class*=thesaurus]', '.rel-word', '.similar']:
    items = soup.select(sel)
    if items:
        print(f"Synonym '{sel}': {len(items)} items")
        for item in items[:3]:
            print(f"  {item.get_text(strip=True)[:120]}")

# Look for button/link text containing 同义/词源/短语/例句
for text in ['短语', '同义', '词源', '例句', '柯林斯', '词组']:
    elems = soup.find_all(lambda tag: tag.name and text in (tag.get_text() or ''))
    if elems:
        print(f"'{text}' found {len(elems)} times, first parent classes: {elems[0].parent.get('class','?')[:3]}")

# Check all script tags for word data
for script in soup.find_all('script'):
    if script.string and ('NUXT' in script.string or 'window.__' in script.string):
        print(f"Script found with key data: {script.string[:200]}")

# Try to get etymology from Collins section
collins = soup.select('.collins-section, .collins, [class*=collins]')
print(f"Collins sections: {len(collins)}")

# Search for etymology in text
etym_elems = soup.find_all(string=lambda t: t and ('词源' in t or 'etymo' in t.lower()))
print(f"Etymology mentions: {len(etym_elems)}")
for e in etym_elems[:5]:
    print(f"  {e.strip()[:120]}")

# Get all unique class names to understand the page structure
classes = set()
for tag in soup.find_all(class_=True):
    for c in tag.get('class', []):
        classes.add(c)
main_cls = [c for c in sorted(classes) if any(k in c.lower() for k in ['sent', 'phr', 'trans', 'syn', 'word', 'collins', 'mean', 'ety'])]
print(f"\nRelevant classes: {main_cls}")