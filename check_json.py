#!/usr/bin/env python3
import json, re, os
BASE = '/Users/allen/Downloads/人教版(PEP)'
issues_found = 0
for fname in ['八年级上册词汇表.json', '八年级下册词汇表.json', '七年级下册词汇表.json',
              '七年级上册词汇表.json', '四年级下册词汇表.json', '五年级上册词汇表.json', '五年级下册词汇表.json']:
    d = json.load(open(os.path.join(BASE, fname)))
    issues = []
    for e in d:
        for t in e.get('trans', []):
            cn = t.get('cn', '')
            if '&' in cn and t['pos']:
                issues.append(f"{e['word']}: pos='{t['pos']}' cn='{cn[:60]}'")
            m = re.match(r'^(n\.|v\.|adj\.|adv\.|prep\.|conj\.|pron\.)', cn)
            if m:
                issues.append(f"{e['word']}: pos='{t['pos']}' cn_POS='{cn[:60]}'")
    if issues:
        count = len(issues)
        issues_found += count
        print(f"--- {fname} ({count} issues) ---")
        for i in issues[:8]:
            print(f"  {i}")
        if count > 8:
            print(f"  ... +{count-8} more")
        print()
print(f"Total issues: {issues_found}")