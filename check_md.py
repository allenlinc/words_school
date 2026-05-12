import re

with open('/Users/allen/Downloads/人教版(PEP)/四年级下册词汇表.md', 'r', encoding='utf-8') as f:
    content = f.read()

sections = re.findall(r'## ([A-Z])\n\n\| 单词 \|.*?\n\|[-| ]+\|\n((?:\| .*?\n)+)', content)
total = 0
total_key = 0
for letter, table in sections:
    lines_in_table = [l for l in table.split('\n') if l.strip().startswith('|')]
    entries = [l for l in lines_in_table if l.strip() not in ('| 单词 | 音标 | 释义 | 页码 |', '|------|------|------|------|')]
    key_count = sum(1 for e in entries if e.strip().startswith('| *'))
    total += len(entries)
    total_key += key_count
    print(f'  {letter}: {len(entries)} entries ({key_count} key)')

print(f'\nTotal: {total} entries ({total_key} key, {total - total_key} non-key)')

# Show a few entries
for l in content.split('\n')[10:30]:
    if l.startswith('|'):
        print(l[:80])