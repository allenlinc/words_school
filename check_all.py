import json
files = ['五年级上册词汇表.json','五年级下册词汇表.json','七年级上册词汇表.json','七年级下册词汇表.json','八年级上册词汇表.json','八年级下册词汇表.json']
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        data = json.load(fp)
    n = len(data)
    s = sum(1 for e in data if e.get('synos'))
    e = sum(1 for e in data if e.get('etymology'))
    t = sum(1 for e in data if e.get('sentences'))
    p = sum(1 for e in data if e.get('phrases'))
    r = sum(1 for e in data if e.get('relWords',{}).get('rels'))
    h = sum(1 for e in data if e.get('phonetic0'))
    star = sum(1 for e in data if e['word'].startswith('*'))
    print(f'{f}: {n} entries | synos={s} etym={e} sent={t} phr={p} rel={r} phon={h} star={star}')