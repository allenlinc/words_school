#!/usr/bin/env python3
"""Generate missing relWords (word forms) for JSON vocabulary entries."""
import json
import re

JSON_PATH = '/Users/allen/Downloads/人教版(PEP)/四年级下册词汇表.json'

# Irregular forms
IRREGULAR = {
    # Nouns - irregular plurals
    'child': {'c': 'children', 'cn': '复数'},
    'man': {'c': 'men', 'cn': '复数'},
    'woman': {'c': 'women', 'cn': '复数'},
    'mouse': {'c': 'mice', 'cn': '复数'},
    'foot': {'c': 'feet', 'cn': '复数'},
    'tooth': {'c': 'teeth', 'cn': '复数'},
    'goose': {'c': 'geese', 'cn': '复数'},
    'person': {'c': 'people', 'cn': '复数'},
    'sheep': {'c': 'sheep', 'cn': '复数'},
    'deer': {'c': 'deer', 'cn': '复数'},
    'fish': {'c': 'fish', 'cn': '复数'},
    'knife': {'c': 'knives', 'cn': '复数'},
    'wife': {'c': 'wives', 'cn': '复数'},
    'life': {'c': 'lives', 'cn': '复数'},
    'leaf': {'c': 'leaves', 'cn': '复数'},
    'wolf': {'c': 'wolves', 'cn': '复数'},
    'half': {'c': 'halves', 'cn': '复数'},
    'tomato': {'c': 'tomatoes', 'cn': '复数'},
    'potato': {'c': 'potatoes', 'cn': '复数'},
    'hero': {'c': 'heroes', 'cn': '复数'},
    'photo': {'c': 'photos', 'cn': '复数'},
    'piano': {'c': 'pianos', 'cn': '复数'},
    # Adjectives - irregular
    'good': [{'c': 'better', 'cn': '比较级'}, {'c': 'best', 'cn': '最高级'}],
    'bad': [{'c': 'worse', 'cn': '比较级'}, {'c': 'worst', 'cn': '最高级'}],
    'little': [{'c': 'less', 'cn': '比较级'}, {'c': 'least', 'cn': '最高级'}],
    'many': [{'c': 'more', 'cn': '比较级'}, {'c': 'most', 'cn': '最高级'}],
    'much': [{'c': 'more', 'cn': '比较级'}, {'c': 'most', 'cn': '最高级'}],
    'far': [{'c': 'farther', 'cn': '比较级'}, {'c': 'farthest', 'cn': '最高级'}],
    'old': [{'c': 'older', 'cn': '比较级'}, {'c': 'oldest', 'cn': '最高级'}],
    # Verbs - irregular forms
    'be': [
        {'c': 'am', 'cn': '现在式(第一人称)'}, {'c': 'is', 'cn': '第三人称单数'}, {'c': 'are', 'cn': '现在式(复数)'},
        {'c': 'was', 'cn': '过去式(单数)'}, {'c': 'were', 'cn': '过去式(复数)'},
        {'c': 'been', 'cn': '过去分词'}, {'c': 'being', 'cn': '现在分词'}
    ],
    'go': [{'c': 'goes', 'cn': '第三人称单数'}, {'c': 'going', 'cn': '现在分词'}, {'c': 'went', 'cn': '过去式'}, {'c': 'gone', 'cn': '过去分词'}],
    'have': [{'c': 'has', 'cn': '第三人称单数'}, {'c': 'having', 'cn': '现在分词'}, {'c': 'had', 'cn': '过去式'}, {'c': 'had', 'cn': '过去分词'}],
    'do': [{'c': 'does', 'cn': '第三人称单数'}, {'c': 'doing', 'cn': '现在分词'}, {'c': 'did', 'cn': '过去式'}, {'c': 'done', 'cn': '过去分词'}],
    'say': [{'c': 'says', 'cn': '第三人称单数'}, {'c': 'saying', 'cn': '现在分词'}, {'c': 'said', 'cn': '过去式'}, {'c': 'said', 'cn': '过去分词'}],
    'get': [{'c': 'gets', 'cn': '第三人称单数'}, {'c': 'getting', 'cn': '现在分词'}, {'c': 'got', 'cn': '过去式'}, {'c': 'got', 'cn': '过去分词'}],
    'make': [{'c': 'makes', 'cn': '第三人称单数'}, {'c': 'making', 'cn': '现在分词'}, {'c': 'made', 'cn': '过去式'}, {'c': 'made', 'cn': '过去分词'}],
    'know': [{'c': 'knows', 'cn': '第三人称单数'}, {'c': 'knowing', 'cn': '现在分词'}, {'c': 'knew', 'cn': '过去式'}, {'c': 'known', 'cn': '过去分词'}],
    'think': [{'c': 'thinks', 'cn': '第三人称单数'}, {'c': 'thinking', 'cn': '现在分词'}, {'c': 'thought', 'cn': '过去式'}, {'c': 'thought', 'cn': '过去分词'}],
    'take': [{'c': 'takes', 'cn': '第三人称单数'}, {'c': 'taking', 'cn': '现在分词'}, {'c': 'took', 'cn': '过去式'}, {'c': 'taken', 'cn': '过去分词'}],
    'see': [{'c': 'sees', 'cn': '第三人称单数'}, {'c': 'seeing', 'cn': '现在分词'}, {'c': 'saw', 'cn': '过去式'}, {'c': 'seen', 'cn': '过去分词'}],
    'come': [{'c': 'comes', 'cn': '第三人称单数'}, {'c': 'coming', 'cn': '现在分词'}, {'c': 'came', 'cn': '过去式'}, {'c': 'come', 'cn': '过去分词'}],
    'run': [{'c': 'runs', 'cn': '第三人称单数'}, {'c': 'running', 'cn': '现在分词'}, {'c': 'ran', 'cn': '过去式'}, {'c': 'run', 'cn': '过去分词'}],
    'eat': [{'c': 'eats', 'cn': '第三人称单数'}, {'c': 'eating', 'cn': '现在分词'}, {'c': 'ate', 'cn': '过去式'}, {'c': 'eaten', 'cn': '过去分词'}],
    'buy': [{'c': 'buys', 'cn': '第三人称单数'}, {'c': 'buying', 'cn': '现在分词'}, {'c': 'bought', 'cn': '过去式'}, {'c': 'bought', 'cn': '过去分词'}],
    'bring': [{'c': 'brings', 'cn': '第三人称单数'}, {'c': 'bringing', 'cn': '现在分词'}, {'c': 'brought', 'cn': '过去式'}, {'c': 'brought', 'cn': '过去分词'}],
    'put': [{'c': 'puts', 'cn': '第三人称单数'}, {'c': 'putting', 'cn': '现在分词'}, {'c': 'put', 'cn': '过去式'}, {'c': 'put', 'cn': '过去分词'}],
    'let': [{'c': 'lets', 'cn': '第三人称单数'}, {'c': 'letting', 'cn': '现在分词'}, {'c': 'let', 'cn': '过去式'}, {'c': 'let', 'cn': '过去分词'}],
    'write': [{'c': 'writes', 'cn': '第三人称单数'}, {'c': 'writing', 'cn': '现在分词'}, {'c': 'wrote', 'cn': '过去式'}, {'c': 'written', 'cn': '过去分词'}],
    'swim': [{'c': 'swims', 'cn': '第三人称单数'}, {'c': 'swimming', 'cn': '现在分词'}, {'c': 'swam', 'cn': '过去式'}, {'c': 'swum', 'cn': '过去分词'}],
    'sing': [{'c': 'sings', 'cn': '第三人称单数'}, {'c': 'singing', 'cn': '现在分词'}, {'c': 'sang', 'cn': '过去式'}, {'c': 'sung', 'cn': '过去分词'}],
    'drink': [{'c': 'drinks', 'cn': '第三人称单数'}, {'c': 'drinking', 'cn': '现在分词'}, {'c': 'drank', 'cn': '过去式'}, {'c': 'drunk', 'cn': '过去分词'}],
    'fly': [{'c': 'flies', 'cn': '第三人称单数'}, {'c': 'flying', 'cn': '现在分词'}, {'c': 'flew', 'cn': '过去式'}, {'c': 'flown', 'cn': '过去分词'}],
    'draw': [{'c': 'draws', 'cn': '第三人称单数'}, {'c': 'drawing', 'cn': '现在分词'}, {'c': 'drew', 'cn': '过去式'}, {'c': 'drawn', 'cn': '过去分词'}],
    'choose': [{'c': 'chooses', 'cn': '第三人称单数'}, {'c': 'choosing', 'cn': '现在分词'}, {'c': 'chose', 'cn': '过去式'}, {'c': 'chosen', 'cn': '过去分词'}],
    'give': [{'c': 'gives', 'cn': '第三人称单数'}, {'c': 'giving', 'cn': '现在分词'}, {'c': 'gave', 'cn': '过去式'}, {'c': 'given', 'cn': '过去分词'}],
    'speak': [{'c': 'speaks', 'cn': '第三人称单数'}, {'c': 'speaking', 'cn': '现在分词'}, {'c': 'spoke', 'cn': '过去式'}, {'c': 'spoken', 'cn': '过去分词'}],
    'begin': [{'c': 'begins', 'cn': '第三人称单数'}, {'c': 'beginning', 'cn': '现在分词'}, {'c': 'began', 'cn': '过去式'}, {'c': 'begun', 'cn': '过去分词'}],
    'teach': [{'c': 'teaches', 'cn': '第三人称单数'}, {'c': 'teaching', 'cn': '现在分词'}, {'c': 'taught', 'cn': '过去式'}, {'c': 'taught', 'cn': '过去分词'}],
    'feel': [{'c': 'feels', 'cn': '第三人称单数'}, {'c': 'feeling', 'cn': '现在分词'}, {'c': 'felt', 'cn': '过去式'}, {'c': 'felt', 'cn': '过去分词'}],
    'tell': [{'c': 'tells', 'cn': '第三人称单数'}, {'c': 'telling', 'cn': '现在分词'}, {'c': 'told', 'cn': '过去式'}, {'c': 'told', 'cn': '过去分词'}],
    'stand': [{'c': 'stands', 'cn': '第三人称单数'}, {'c': 'standing', 'cn': '现在分词'}, {'c': 'stood', 'cn': '过去式'}, {'c': 'stood', 'cn': '过去分词'}],
    'understand': [{'c': 'understands', 'cn': '第三人称单数'}, {'c': 'understanding', 'cn': '现在分词'}, {'c': 'understood', 'cn': '过去式'}, {'c': 'understood', 'cn': '过去分词'}],
    'sit': [{'c': 'sits', 'cn': '第三人称单数'}, {'c': 'sitting', 'cn': '现在分词'}, {'c': 'sat', 'cn': '过去式'}, {'c': 'sat', 'cn': '过去分词'}],
    'sleep': [{'c': 'sleeps', 'cn': '第三人称单数'}, {'c': 'sleeping', 'cn': '现在分词'}, {'c': 'slept', 'cn': '过去式'}, {'c': 'slept', 'cn': '过去分词'}],
    'keep': [{'c': 'keeps', 'cn': '第三人称单数'}, {'c': 'keeping', 'cn': '现在分词'}, {'c': 'kept', 'cn': '过去式'}, {'c': 'kept', 'cn': '过去分词'}],
    'read': [{'c': 'reads', 'cn': '第三人称单数'}, {'c': 'reading', 'cn': '现在分词'}, {'c': 'read', 'cn': '过去式'}, {'c': 'read', 'cn': '过去分词'}],
    'cut': [{'c': 'cuts', 'cn': '第三人称单数'}, {'c': 'cutting', 'cn': '现在分词'}, {'c': 'cut', 'cn': '过去式'}, {'c': 'cut', 'cn': '过去分词'}],
    'hit': [{'c': 'hits', 'cn': '第三人称单数'}, {'c': 'hitting', 'cn': '现在分词'}, {'c': 'hit', 'cn': '过去式'}, {'c': 'hit', 'cn': '过去分词'}],
    'win': [{'c': 'wins', 'cn': '第三人称单数'}, {'c': 'winning', 'cn': '现在分词'}, {'c': 'won', 'cn': '过去式'}, {'c': 'won', 'cn': '过去分词'}],
    'find': [{'c': 'finds', 'cn': '第三人称单数'}, {'c': 'finding', 'cn': '现在分词'}, {'c': 'found', 'cn': '过去式'}, {'c': 'found', 'cn': '过去分词'}],
    'break': [{'c': 'breaks', 'cn': '第三人称单数'}, {'c': 'breaking', 'cn': '现在分词'}, {'c': 'broke', 'cn': '过去式'}, {'c': 'broken', 'cn': '过去分词'}],
    'drive': [{'c': 'drives', 'cn': '第三人称单数'}, {'c': 'driving', 'cn': '现在分词'}, {'c': 'drove', 'cn': '过去式'}, {'c': 'driven', 'cn': '过去分词'}],
    'pay': [{'c': 'pays', 'cn': '第三人称单数'}, {'c': 'paying', 'cn': '现在分词'}, {'c': 'paid', 'cn': '过去式'}, {'c': 'paid', 'cn': '过去分词'}],
    'wear': [{'c': 'wears', 'cn': '第三人称单数'}, {'c': 'wearing', 'cn': '现在分词'}, {'c': 'wore', 'cn': '过去式'}, {'c': 'worn', 'cn': '过去分词'}],
    'feed': [{'c': 'feeds', 'cn': '第三人称单数'}, {'c': 'feeding', 'cn': '现在分词'}, {'c': 'fed', 'cn': '过去式'}, {'c': 'fed', 'cn': '过去分词'}],
}


def plural_noun(word):
    """Generate plural form of a noun."""
    wl = word.lower()
    if wl in IRREGULAR:
        ir = IRREGULAR[wl]
        if isinstance(ir, dict):
            return [ir]
    if wl.endswith(('ch', 'sh', 's', 'x', 'z')):
        return [{'c': word + 'es', 'cn': '复数'}]
    if wl.endswith('y') and len(wl) > 1 and wl[-2] not in 'aeiou':
        return [{'c': word[:-1] + 'ies', 'cn': '复数'}]
    if wl.endswith('o') and wl[-2] not in 'aeiou':
        return [{'c': word + 'es', 'cn': '复数'}]
    return [{'c': word + 's', 'cn': '复数'}]


def verb_forms(word):
    """Generate all verb forms."""
    wl = word.lower()
    if wl in IRREGULAR:
        ir = IRREGULAR[wl]
        if isinstance(ir, list) and len(ir) >= 2:
            return ir
    forms = []
    # 3rd person singular
    if wl.endswith(('ch', 'sh', 'ss', 'x', 'z', 'o')):
        forms.append({'c': word + 'es', 'cn': '第三人称单数'})
    elif wl.endswith('y') and len(wl) > 1 and wl[-2] not in 'aeiou':
        forms.append({'c': word[:-1] + 'ies', 'cn': '第三人称单数'})
    else:
        forms.append({'c': word + 's', 'cn': '第三人称单数'})
    # Present participle
    if wl.endswith('e') and not wl.endswith('ee'):
        forms.append({'c': word[:-1] + 'ing', 'cn': '现在分词'})
    elif wl.endswith('ie'):
        forms.append({'c': word[:-2] + 'ying', 'cn': '现在分词'})
    elif len(wl) >= 3 and wl[-1] not in 'aeiouwy' and wl[-2] in 'aeiou' and wl[-3] not in 'aeiou':
        forms.append({'c': word + word[-1] + 'ing', 'cn': '现在分词'})
    else:
        forms.append({'c': word + 'ing', 'cn': '现在分词'})
    # Past tense & past participle
    if wl.endswith('e'):
        forms.append({'c': word + 'd', 'cn': '过去式'})
        forms.append({'c': word + 'd', 'cn': '过去分词'})
    elif wl.endswith('y') and len(wl) > 1 and wl[-2] not in 'aeiou':
        forms.append({'c': word[:-1] + 'ied', 'cn': '过去式'})
        forms.append({'c': word[:-1] + 'ied', 'cn': '过去分词'})
    elif len(wl) >= 3 and wl[-1] not in 'aeiouwy' and wl[-2] in 'aeiou' and wl[-3] not in 'aeiou':
        forms.append({'c': word + word[-1] + 'ed', 'cn': '过去式'})
        forms.append({'c': word + word[-1] + 'ed', 'cn': '过去分词'})
    else:
        forms.append({'c': word + 'ed', 'cn': '过去式'})
        forms.append({'c': word + 'ed', 'cn': '过去分词'})
    return forms


def adj_forms(word):
    """Generate comparative and superlative."""
    wl = word.lower()
    if wl in IRREGULAR:
        ir = IRREGULAR[wl]
        if isinstance(ir, list) and any('比较级' in x.get('cn','') for x in ir):
            return ir
    # Count syllables (approximate)
    vowels = sum(1 for c in wl if c in 'aeiou')
    # 1 syllable: use -er/-est
    if vowels <= 1 and len(wl) <= 6:
        if wl.endswith('e'):
            return [{'c': word + 'r', 'cn': '比较级'}, {'c': word + 'st', 'cn': '最高级'}]
        if wl.endswith('y'):
            return [{'c': word[:-1] + 'ier', 'cn': '比较级'}, {'c': word[:-1] + 'iest', 'cn': '最高级'}]
        if len(wl) >= 3 and wl[-1] not in 'aeiouwy' and wl[-2] in 'aeiou' and wl[-3] not in 'aeiou':
            return [{'c': word + word[-1] + 'er', 'cn': '比较级'}, {'c': word + word[-1] + 'est', 'cn': '最高级'}]
        return [{'c': word + 'er', 'cn': '比较级'}, {'c': word + 'est', 'cn': '最高级'}]
    else:
        return [{'c': 'more ' + word, 'cn': '比较级'}, {'c': 'most ' + word, 'cn': '最高级'}]


def generate_relwords(word, pos_set):
    """Generate relWords based on word and its POS."""
    words = []
    for pos in pos_set:
        pos_clean = pos.strip().rstrip('.')
        if pos_clean in ('n', 'noun'):
            # Skip uncountable nouns
            uncountable = {'clothes', 'homework', 'music', 'maths', 'mathematics', 'shorts', 'trousers', 'sunglasses'}
            if word.lower() not in uncountable:
                words.extend(plural_noun(word))
        elif pos_clean in ('v', 'verb'):
            words.extend(verb_forms(word))
        elif pos_clean in ('adj', 'adjective'):
            words.extend(adj_forms(word))
        elif pos_clean in ('adv', 'adverb'):
            # Some adverbs have comparative/superlative
            if word.lower() in ('hard', 'fast', 'early', 'late', 'soon', 'near'):
                words.extend(adj_forms(word))

    # Deduplicate by (c, cn) pair
    seen = set()
    unique = []
    for w in words:
        key = (w['c'], w['cn'])
        if key not in seen:
            seen.add(key)
            unique.append(w)

    if unique:
        return {"root": "", "rels": [{"pos": "", "words": unique}]}
    return {}


# Words that shouldn't have relWords
NO_REL = {'any', 'herself', 'just', 'those', 'when', 'clothes', 'homework', 'music', 'maths', 'shorts', 'sunglasses', 'trousers'}

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    data = json.load(f)

updated = 0
for entry in data:
    word = entry['word']
    # Skip phrases
    if ' ' in word:
        continue

    rw = entry.get('relWords', {})
    if rw and rw.get('rels'):
        continue  # Already has relWords

    if word.lower() in NO_REL:
        continue  # Words that don't have useful word forms

    trans = entry.get('trans', [])
    pos_set = set()
    for t in trans:
        p = t.get('pos', '')
        if p:
            pos_set.add(p.strip().rstrip('.'))

    if not pos_set:
        continue

    new_rw = generate_relwords(word, pos_set)
    if new_rw and new_rw.get('rels'):
        entry['relWords'] = new_rw
        updated += 1
        forms = [w['c'] for w in new_rw['rels'][0]['words']]
        print(f'  {word}: {forms}')

with open(JSON_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'\nUpdated {updated} entries.')