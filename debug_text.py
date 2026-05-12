#!/usr/bin/env python3
"""Debug text formatting issues."""
import urllib.request, re
from bs4 import BeautifulSoup

word = 'free'
url = f'https://www.youdao.com/result?word={word}&lang=en'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
req = urllib.request.Request(url, headers=headers)
resp = urllib.request.urlopen(req, timeout=15)
html = resp.read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')

# Check sen-eng raw HTML
print("=== sen-eng elements ===")
for se in soup.select('.sen-eng')[:3]:
    print(f"  raw HTML: {str(se)[:200]}")
    print(f"  get_text: '{se.get_text()}'")
    print(f"  stripped_strings join: '{' '.join(se.stripped_strings)}'")
    print()

# Check phrs-content raw HTML  
print("=== phrs-content children ===")
phr = soup.select_one('.phrs-content')
if phr:
    print(f"  raw HTML (first 600): {str(phr)[:600]}")
    print()
    for child in phr.find_all(['div', 'p', 'li', 'span', 'a'], recursive=True):
        txt = child.get_text(strip=True)
        attrs = dict(child.attrs) if hasattr(child, 'attrs') else {}
        if txt:
            print(f"  tag={child.name} class={child.get('class', [])} text='{txt}'")

# Test ' '.join approach on sentences
print("\n=== Fixed sentence parsing ===")
for i, se in enumerate(soup.select('.sen-eng')[:3]):
    en = ' '.join(se.stripped_strings)
    ch = soup.select('.sen-ch')[i]
    cn = ' '.join(ch.stripped_strings)
    print(f"  EN: {en}")
    print(f"  CN: {cn}")
    print()