#!/usr/bin/env python3
import json, re, os
BASE = '/Users/allen/Downloads/人教版(PEP)'
counts = {}
for fname in ['八年级上册词汇表.json', '八年级下册词汇表.json', '七年级下册词汇表.json',
              '七年级上册词汇表.json', '四年级下册词汇表.json', '五年级上册词汇表.json', '五年级下册词汇表.json']:
    d = json.load(open(os.path.join(BASE, fname)))
    counts[fname] = len(d)
    for e in d:
        assert 'word' in e and 'trans' in e and 'phonetic0' in e
        assert isinstance(e['trans'], list)
        for t in e['trans']:
            assert 'pos' in t and 'cn' in t
    print(f'OK: {fname}: {len(d)} entries')
print(f'Total: {sum(counts.values())} entries, all valid')