#!/usr/bin/env python3
"""Debug sentence structure in detail."""
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

# Look at blng_sents_part children structure
print("=== blng_sents_part children ===")
biling = soup.select('.blng_sents_part')
for bl in biling:
    for child in bl.children:
        if hasattr(child, 'get_text'):
            txt = child.get_text(strip=True)
            cls = child.get('class', [])
            tag = child.name if hasattr(child, 'name') else str(type(child))
            print(f"  tag={tag} class={cls}: {txt[:100]}")
        else:
            print(f"  child type: {type(child)}")

# Try getting sentences by looking at individual .sen-eng and .sen-ch elements
print("\n=== sen-eng elements ===")
for se in soup.select('.sen-eng, .sen-eng2, [class*="sen-eng"]')[:5]:
    print(f"  class={se.get('class')}: text={se.get_text(strip=True)[:100]}")

print("\n=== sen-ch elements ===")
for sc in soup.select('.sen-ch, [class*="sen-ch"]')[:5]:
    print(f"  class={sc.get('class')}: text={sc.get_text(strip=True)[:100]}")

# Check for data-src or similar attributes  
print("\n=== Any 'sen' class elements ===")
for s in soup.select('[class*="sen"]')[:10]:
    cls = s.get('class', [])
    txt = s.get_text(strip=True)[:80]
    print(f"  class={cls}: {txt}")

# Try to get sentences from the catalogue_sentence using a different approach
print("\n=== catalogue_sentence inner HTML (first 500) ===")
cat = soup.select_one('.catalogue_sentence')
if cat:
    inner = str(cat)[:1000]
    print(inner)

# Check .blng_sents_part inner
print("\n=== blng_sents_part inner HTML (first 800) ===")
bl = soup.select_one('.blng_sents_part')
if bl:
    print(str(bl)[:800])

# Try getting sentences from word-exp that are actual sentences
print("\n=== word-exp sentence detection ===")
exp_elems = soup.select('.word-exp')
for elem in exp_elems:
    text = elem.get_text(strip=True)
    # Check if it's an English sentence (starts with capital letter, contains spaces)
    if re.match(r'^[A-Z][a-zA-Z\s.,;!?\']+$', text[:30]):
        print(f"  EN sentence: {text[:80]}")
    elif re.match(r'^[\u4e00-\u9fff][\u4e00-\u9fff\s，。！？、；：""''「」]+$', text[:20]):
        print(f"  CN text: {text[:80]}")
    elif '《' in text:
        print(f"  Citation: {text[:80]}")