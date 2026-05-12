#!/usr/bin/env python3
"""Quick validation of updated JSON."""
import json

with open('/Users/allen/Downloads/人教版(PEP)/四年级下册词汇表.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

total = len(data)
has_synos = sum(1 for e in data if e.get('synos'))
has_etym = sum(1 for e in data if e.get('etymology'))
has_sent = sum(1 for e in data if e.get('sentences'))
has_phrases = sum(1 for e in data if e.get('phrases'))
has_rel = sum(1 for e in data if e.get('relWords', {}).get('rels'))
has_phonetic = sum(1 for e in data if e.get('phonetic0'))
has_trans_pos = sum(1 for e in data if any(t.get('pos') for t in e.get('trans', [])))

no_synos = [e['word'] for e in data if not e.get('synos')]
no_etym = [e['word'] for e in data if not e.get('etymology')]

print(f"Total: {total}")
print(f"Has synos: {has_synos}/{total}")
print(f"Has etymology: {has_etym}/{total}")
print(f"Has sentences: {has_sent}/{total}")
print(f"Has phrases: {has_phrases}/{total}")
print(f"Has relWords: {has_rel}/{total}")
print(f"Has phonetics: {has_phonetic}/{total}")
print(f"Has trans with POS: {has_trans_pos}/{total}")

if no_synos:
    print(f"\nNO synos ({len(no_synos)}): {no_synos}")
if no_etym:
    print(f"\nNO etymology ({len(no_etym)}): {no_etym}")

# Show some examples
print("\n=== Sample entries ===")
for e in data[:5]:
    w = e['word']
    p0 = e.get('phonetic0', '')
    s = e.get('synos', [])
    et = e.get('etymology', [])
    st = e.get('sentences', [])
    ph = e.get('phrases', [])
    print(f"\n--- {w} ---")
    print(f"  phonetic: {p0}")
    print(f"  trans: {e.get('trans', [])}")
    print(f"  synos: {s[0] if s else 'EMPTY'}")
    print(f"  etymology: {et[0].get('d', '') if et else 'EMPTY'}")
    print(f"  sentences: {len(st)}")
    print(f"  phrases: {len(ph)}")
    print(f"  relWords: {e.get('relWords', {})}")

# Check specific words user cares about
print("\n=== Key word checks ===")
for w in ['free', 'bird', 'beautiful', 'delicious', 'cheap', 'bedroom', 'bowl', 'go to bed']:
    for e in data:
        if e['word'].strip('* ') == w:
            syn = e.get('synos', [])
            et = e.get('etymology', [])
            print(f"\n{w}: synos={'YES' if syn else 'NO'} ({syn[:1]}), etymology={'YES' if et else 'NO'} ({et[:1]})")
            break