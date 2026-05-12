#!/usr/bin/env python3
"""Extract all unique words from OCR output and build vocabulary list."""
import re

with open('/tmp/ocr_output.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove non-vocabulary lines
text = re.sub(r'=== .+? ===', '', text)
text = re.sub(r'Appendix \d|Vocabulary', '', text)
text = re.sub(r'LADDER AL|L R A R R|LATeR EAR|A Me A & TR', '', text)

# Normalize: merge "p. XX" that's on its own line back
lines = text.split('\n')
merged = []
for line in lines:
    stripped = line.strip()
    if re.match(r'^p\.\s*\d+$', stripped):
        if merged:
            merged[-1] += ' ' + stripped
    elif re.match(r'^\d+$', stripped):
        continue  # skip page numbers
    elif stripped:
        merged.append(stripped)

text2 = '\n'.join(merged)

# Now extract: * optional, word (or phrase), optional /pron/, then p. XX
pattern = r'(\*?)([A-Za-z][A-Za-z\s\-\']+?)(?:\s+(/[^/]*/))?.*?p\.\s*(\d+)'
matches = re.findall(pattern, text2)

seen = set()
words = []
for star, word, pron, page in matches:
    word = word.strip()
    if word.lower() in seen:
        continue
    if len(word) < 2:
        continue
    # Skip letter headers (A, B, C, etc)
    if len(word) == 1 and word.isalpha():
        continue
    seen.add(word.lower())
    words.append((star, word.strip(), pron.strip(), page))

print(f"Found {len(words)} unique words:\n")
for star, word, pron, page in sorted(words, key=lambda x: x[1].lower()):
    star_mark = '*' if star else ''
    print(f"{star_mark}{word:<25} {pron:<25} p. {page}")