#!/usr/bin/env python3
"""Convert all 7 vocabulary markdown files to JSON format."""
import json
import re
import os

BASE = '/Users/allen/Downloads/人教版(PEP)'

# POS patterns in Chinese meaning
SINGLE_POS = r'(n\.|v\.|adj\.|adv\.|prep\.|conj\.|pron\.|interj\.|art\.|num\.|modal\s+v\.|aux\.\s+v\.)'
POS_RE = re.compile(r'^' + SINGLE_POS)
# Combined POS: "adv. & prep.", "v. & n.", "prep., adv. & conj." etc.
MULTI_POS_RE = re.compile(
    r'^((?:n\.|v\.|adj\.|adv\.|prep\.|conj\.|pron\.|interj\.|art\.|num\.|modal\s+v\.|aux\.\s+v\.)'
    r'(?:\s*[,&]\s*(?:n\.|v\.|adj\.|adv\.|prep\.|conj\.|pron\.|interj\.|art\.|num\.|modal\s+v\.|aux\.\s+v\.))+)'
    r'(?:\s+)(.+)',
    re.DOTALL
)
SINGLE_POS_LIST = re.compile(r'\b(n\.|v\.|adj\.|adv\.|prep\.|conj\.|pron\.|interj\.|art\.|num\.|modal\s+v\.|aux\.\s+v\.)')


def parse_cn(cn_text):
    """Parse Chinese meaning into (pos, cn) pairs."""
    if not cn_text:
        return [{"pos": "", "cn": ""}]

    cn_text = cn_text.strip().rstrip(';；')

    # Try to match combined POS like "adv. & prep. meaning"
    m = MULTI_POS_RE.match(cn_text)
    if m:
        pos_part = m.group(1)  # "adv. & prep."
        rest = m.group(2).strip().rstrip(';；')
        poses = SINGLE_POS_LIST.findall(pos_part)
        results = []
        for pos in poses:
            results.append({"pos": pos.strip(), "cn": rest})
        if results:
            return results

    # Try pattern: "pos. meaning1 pos. meaning2" (separate POS with separate meanings)
    # Example: "v. 对待；治疗；款待 n. 款待"
    rest_of_text = cn_text
    m0 = POS_RE.match(cn_text)
    if m0:
        results = []
        while rest_of_text:
            m = POS_RE.match(rest_of_text)
            if m:
                pos = m.group(1).strip()
                remaining = rest_of_text[m.end():].strip()
                # Find the next POS marker in the remaining text
                next_pos = SINGLE_POS_LIST.search(remaining)
                if next_pos:
                    cn_part = remaining[:next_pos.start()].strip().rstrip(';；')
                    rest_of_text = remaining[next_pos.start():].strip()
                else:
                    cn_part = remaining.strip().rstrip(';；')
                    rest_of_text = ''
                results.append({"pos": pos, "cn": cn_part})
            else:
                if results:
                    results[-1]["cn"] = (results[-1]["cn"] + rest_of_text).strip()
                else:
                    results.append({"pos": "", "cn": cn_text})
                break
        if len(results) > 1:
            return results

    # Try single POS: "pos. meaning; pos. meaning" (multiple parts separated by ; or ；)
    parts = re.split(r'[；;]\s*(?=' + SINGLE_POS + r')', cn_text)
    if len(parts) > 1:
        results = []
        for part in parts:
            part = part.strip().rstrip(';；')
            m = POS_RE.match(part)
            if m:
                pos = m.group(1).strip()
                rest = part[m.end():].strip()
                results.append({"pos": pos, "cn": rest})
            else:
                results.append({"pos": "", "cn": part})
        if results:
            return results

    # Single POS
    m = POS_RE.match(cn_text)
    if m:
        pos = m.group(1).strip()
        rest = cn_text[m.end():].strip().rstrip(';；')
        return [{"pos": pos, "cn": rest}]

    return [{"pos": "", "cn": cn_text.strip().rstrip(';；')}]


def parse_phonetic(raw):
    """Clean up phonetic notation."""
    if not raw:
        return ""
    p = raw.strip()
    if p.startswith('/') and not p.endswith('/'):
        p = p + '/'
    if not p.startswith('/'):
        p = '/' + p + '/'
    return ' ' + p + ' '


def parse_md(filepath):
    """Parse a markdown vocabulary table file."""
    entries = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    current_word = None
    current_phonetic = ""
    current_cn = ""

    for line in lines:
        line = line.strip()
        # Match table rows: | word | phonetic | meaning | page |
        m = re.match(r'^\|\s*(.+?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*p\.\s*\S+\s*\|', line)
        if m:
            word = m.group(1).strip()
            phonetic_raw = m.group(2).strip()
            cn = m.group(3).strip()

            # Clean phonetic
            phonetic = parse_phonetic(phonetic_raw)

            entries.append({
                "word": word,
                "phonetic0": phonetic,
                "phonetic1": phonetic,
                "trans": parse_cn(cn),
                "sentences": [],
                "phrases": [],
                "synos": [],
                "relWords": {},
                "etymology": []
            })

    return entries


def generate_json(md_path, json_path):
    """Generate JSON file from markdown."""
    basename = os.path.basename(md_path).replace('.md', '')
    entries = parse_md(md_path)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    return len(entries)


# All markdown files to process
MD_FILES = [
    '八年级上册词汇表.md',
    '八年级下册词汇表.md',
    '七年级下册词汇表.md',
    '七年级上册词汇表.md',
    '四年级下册词汇表.md',
    '五年级上册词汇表.md',
    '五年级下册词汇表.md',
]

total = 0
for md_name in MD_FILES:
    md_path = os.path.join(BASE, md_name)
    json_name = md_name.replace('.md', '.json')
    json_path = os.path.join(BASE, json_name)
    if os.path.exists(md_path):
        n = generate_json(md_path, json_path)
        total += n
        print(f"  {md_name} -> {json_name}: {n} entries")
    else:
        print(f"  SKIP {md_name}: file not found")

print(f"\nTotal: {total} entries across {len(MD_FILES)} files")