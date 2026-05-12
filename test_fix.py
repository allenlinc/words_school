#!/usr/bin/env python3
"""Test fixed parsing functions."""
import urllib.request, re, json, sys
from bs4 import BeautifulSoup

sys.path.insert(0, '/Users/allen/Downloads/人教版(PEP)')
from update_vocab_youdao import parse_sentences, parse_phrases, parse_trans, parse_phonetics, parse_word_forms, fetch_youdao

words = ['free', 'beautiful', 'delicious', 'cheap']
for word in words:
    print(f"\n=== {word} ===")
    html = fetch_youdao(word)
    if not html:
        print("  FETCH FAILED")
        continue
    soup = BeautifulSoup(html, 'html.parser')
    
    # Test sentences
    sents = parse_sentences(soup)
    print(f"  Sentences: {len(sents)}")
    for s in sents[:3]:
        print(f"    EN: {s['c'][:80]}")
        print(f"    CN: {s['cn'][:80]}")
    
    # Test phrases
    phrs = parse_phrases(soup)
    print(f"  Phrases: {len(phrs)}")
    for p in phrs[:5]:
        print(f"    {p['c']} → {p['cn'][:60]}")
    
    # Test trans
    trans = parse_trans(soup)
    print(f"  Trans: {len(trans)} entries with POS")