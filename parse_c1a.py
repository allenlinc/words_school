#!/usr/bin/env python3
"""Extract vocabulary from 初一上册 OCR output."""
import re, os

with open('/tmp/ocr_c1a.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove headers and non-vocabulary lines
lines = text.split('\n')
# Normalize: merge page numbers that are on their own line
merged = []
for line in lines:
    s = line.strip()
    if not s: continue
    if s.startswith('=== ') or s.startswith('Appendix') or s.startswith('Vocabulary'):
        continue
    if re.match(r'^(L[A-Z ]+|K[A-Z ]+)\d*$', s): continue  # LADDER AL, KARATE, etc
    if re.match(r'^\d+$', s): continue  # bare numbers
    merged.append(s)

text2 = '\n'.join(merged)

# Extract entries: word /pron/ pos. meaning p.XX
# Pattern: word (possibly with spaces, hyphens), optional /pron/, word class, etc.
pattern = r'([A-Za-z][A-Za-z\s\-\']+(?:\s*/\s*[^/]*/\s*)?(?:\s*(?:n\.|v\.|adj\.|adv\.|prep\.|conj\.|pron\.|interj\.|modal v\.)).*?p\.\s*\d+)'
entries = re.findall(pattern, text2, re.DOTALL)

print(f"Found {len(entries)} raw entries\n")
for i, e in enumerate(entries):
    # Clean up
    e = ' '.join(e.split())
    print(f"{i+1}. {e[:130]}")