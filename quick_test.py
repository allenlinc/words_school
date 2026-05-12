#!/usr/bin/env python3
"""Quick test of fixed parsing."""
import urllib.request, re, json
from bs4 import BeautifulSoup

def parse_sentences(soup):
    results = []
    engs = soup.select('.sen-eng')
    chs = soup.select('.sen-ch')
    for i in range(min(len(engs), len(chs), 3)):
        en_text = engs[i].get_text().strip()
        cn_text = chs[i].get_text().strip()
        if en_text and cn_text:
            results.append({"c": en_text, "cn": cn_text})
    return results

def parse_phrases(soup):
    results = []
    phr_container = soup.select_one('.phrs-content')
    if not phr_container:
        return results
    points = phr_container.select('.point')
    trans = phr_container.select('.phr_trans')
    for i in range(min(len(points), len(trans), 8)):
        c = points[i].get_text().strip()
        cn = trans[i].get_text().strip()
        if c and cn:
            results.append({"c": c, "cn": cn})
    return results

words = ['free', 'beautiful', 'delicious', 'cheap', 'chicken', 'expensive']
headers = {'User-Agent': 'Mozilla/5.0'}
for word in words:
    url = f'https://www.youdao.com/result?word={word}&lang=en'
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req, timeout=15)
    soup = BeautifulSoup(resp.read().decode('utf-8'), 'html.parser')
    
    sents = parse_sentences(soup)
    phrs = parse_phrases(soup)
    print(f"\n=== {word} ===")
    print(f"  Sentences ({len(sents)}):")
    for s in sents:
        print(f"    {s['c']}")
        print(f"    {s['cn']}")
    print(f"  Phrases ({len(phrs)}):")
    for p in phrs:
        print(f"    {p['c']} → {p['cn']}")