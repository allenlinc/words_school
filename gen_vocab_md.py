#!/usr/bin/env python3
"""
Build 四年级下册词汇表 from OCR-extracted English words + known curriculum vocabulary.
OCR caught English words and pronunciations correctly; Chinese meanings filled from knowledge.
"""
import json, os

BASE = '/Users/allen/Downloads/人教版(PEP)'

# All vocabulary entries extracted from OCR, with Chinese meanings filled manually
# Format: (word, phonetic, chinese_meaning, page, is_key)
VOCAB = [
    # ===== A =====
    ("a box of", "", "一盒", "57", False),
    ("*any", "/'eni/", "任何的；一些", "52", True),
    ("*art", "/ɑːt/", "美术；艺术", "45", True),
    # ===== B =====
    ("bathroom", "/'bɑːθruːm/", "浴室；洗手间", "43", False),
    ("*beautiful", "/'bjuːtɪfl/", "美丽的", "20", True),
    ("bedroom", "/'bedruːm/", "卧室", "19", False),
    ("*bee", "/biː/", "蜜蜂", "55", True),
    ("*blackboard", "/'blækbɔːd/", "黑板", "7", True),
    ("bowl", "/bəʊl/", "碗", "68", False),
    # ===== C =====
    ("*can", "/kæn/", "可以；能", "57", True),
    ("carrot", "/'kærət/", "胡萝卜", "56", False),
    ("*chair", "/tʃeə(r)/", "椅子", "8", True),
    ("cheap", "/tʃiːp/", "便宜的", "44", False),
    ("*chicken", "/'tʃɪkɪn/", "鸡；鸡肉", "52", True),
    ("chopstick", "/'tʃɒpstɪk/", "筷子", "67", False),
    ("*class", "/klɑːs/", "班级；课", "67", True),
    ("*classroom", "/'klɑːsruːm/", "教室", "5", True),
    ("clear the table", "", "收拾桌子", "67", False),
    ("*clock", "/klɒk/", "钟；时钟", "45", True),
    ("*clothes", "/kləʊðz/", "衣服", "40", True),
    ("*cow", "/kaʊ/", "奶牛", "52", True),
    # ===== D =====
    ("*dear", "/dɪə(r)/", "亲爱的", "29", True),
    ("delicious", "/dɪ'lɪʃəs/", "美味的", "67", False),
    ("*desk", "/desk/", "书桌", "7", True),
    ("*dinner", "/'dɪnə(r)/", "正餐；晚餐", "28", True),
    ("*door", "/dɔː(r)/", "门", "7", True),
    # ===== E =====
    ("expensive", "/ɪk'spensɪv/", "昂贵的", "43", False),
    # ===== F =====
    ("*fan", "/fæn/", "风扇；扇子", "7", True),
    ("feed", "/fiːd/", "喂养", "52", False),
    ("*feel", "/fiːl/", "感觉", "64", True),
    ("first", "/fɜːst/", "第一；首先", "16", False),
    ("follow", "/'fɒləʊ/", "跟随", "4", False),
    ("*food", "/fuːd/", "食物", "67", True),
    ("fork", "/fɔːk/", "叉子", "67", False),
    ("*free", "/friː/", "空闲的；免费的", "45", True),
    # ===== G =====
    ("get up", "", "起床", "31", False),
    ("go home", "", "回家", "32", False),
    ("go to bed", "", "上床睡觉", "32", False),
    ("go to school", "", "去上学", "31", False),
    ("green bean", "/biːn/", "绿豆；四季豆", "5", False),
    # ===== H =====
    ("hand out", "/aʊt/", "分发", "9", False),
    ("*hard", "/hɑːd/", "困难的；坚硬的", "21", True),
    ("hat", "/hæt/", "帽子", "44", False),
    ("*helpful", "/'helpfl/", "有帮助的", "17", True),
    ("herself", "/hɜː'self/", "她自己", "29", False),
    ("homework", "/'həʊmwɜːk/", "家庭作业", "33", False),
    ("*horse", "/hɔːs/", "马", "56", True),
    ("hurry up", "/ʌp/", "赶快", "8", False),
    # ===== J =====
    ("jacket", "/'dʒækɪt/", "夹克衫", "41", False),
    ("just", "/dʒʌst/", "正好；刚刚", "33", False),
    # ===== K =====
    ("*kid", "/kɪd/", "小孩", "28", True),
    ("*kitchen", "/'kɪtʃɪn/", "厨房", "19", True),
    ("knife", "/naɪf/", "刀", "67", False),
    # ===== L =====
    ("large", "/lɑːdʒ/", "大的", "45", False),
    ("*late", "/leɪt/", "晚的；迟的", "4", True),
    ("*light", "/laɪt/", "灯；光", "5", True),
    ("list", "/lɪst/", "清单；列表", "57", False),
    ("living room", "/'lɪvɪŋ ruːm/", "客厅", "16", False),
    ("loud", "/laʊd/", "大声的", "19", False),
    ("*lunch", "/lʌntʃ/", "午餐", "29", True),
    # ===== M =====
    ("*maths", "/mæθs/", "数学", "29", True),
    ("*milk", "/mɪlk/", "牛奶", "65", True),
    ("*minute", "/'mɪnɪt/", "分钟", "16", True),
    ("*mouse", "/maʊs/", "老鼠", "52", True),
    ("*music", "/'mjuːzɪk/", "音乐", "4", True),
    # ===== N =====
    ("newspaper", "/'njuːzpeɪpə(r)/", "报纸", "9", False),
    # ===== O =====
    ("*over", "/'əʊvə(r)/", "在……上方；结束", "28", True),
    # ===== P =====
    ("*pair", "/peə(r)/", "一双；一对", "40", True),
    ("pass", "/pɑːs/", "传递；通过", "64", False),
    ("pick", "/pɪk/", "摘；捡；挑选", "65", False),
    ("*pig", "/pɪɡ/", "猪", "52", True),
    ("*potato", "/pə'teɪtəʊ/", "土豆", "56", True),
    # ===== R =====
    ("ready", "/'redi/", "准备好的", "4", False),
    ("rule", "/ruːl/", "规则", "5", False),
    ("*run", "/rʌn/", "跑", "16", True),
    # ===== S =====
    ("*safe", "/seɪf/", "安全的", "16", True),
    ("salad", "/'sæləd/", "沙拉", "69", False),
    ("set the table", "", "摆桌子", "68", False),
    ("*sheep", "/ʃiːp/", "绵羊", "52", True),
    ("*shoe", "/ʃuː/", "鞋", "44", True),
    ("*shorts", "/ʃɔːts/", "短裤", "40", True),
    ("size", "/saɪz/", "尺寸；尺码", "45", False),
    ("*skirt", "/skɜːt/", "裙子", "41", True),
    ("*sleep", "/sliːp/", "睡觉", "19", True),
    ("*sorry", "/'sɒri/", "对不起", "4", True),
    ("spoon", "/spuːn/", "勺子", "68", False),
    ("*study", "/'stʌdi/", "学习；书房", "20", True),
    ("sunglasses", "/'sʌnɡlɑːsɪz/", "太阳镜", "44", False),
    ("*supermarket", "/'suːpəmɑːkɪt/", "超市", "69", True),
    # ===== T =====
    ("*take", "/teɪk/", "拿；取；带走", "43", True),
    ("*think", "/θɪŋk/", "想；认为", "9", True),
    ("*those", "/ðəʊz/", "那些", "40", True),
    ("*tidy", "/'taɪdi/", "整洁的；整理", "7", True),
    ("*tomato", "/tə'mɑːtəʊ/", "西红柿", "55", True),
    ("*trousers", "/'traʊzəz/", "裤子", "40", True),
    ("try on", "/ɒn/", "试穿", "45", False),
    ("turn off", "/ɒf/", "关掉", "5", False),
    ("*TV", "/ˌtiː'viː/", "电视", "16", True),
    # ===== U =====
    ("understand", "/ˌʌndə'stænd/", "理解；明白", "9", False),
    # ===== W =====
    ("*wall", "/wɔːl/", "墙", "9", True),
    ("*want", "/wɒnt/", "想要", "33", True),
    ("*wash", "/wɒʃ/", "洗", "17", True),
    ("waste", "/weɪst/", "浪费；废物", "67", False),
    ("*watch", "/wɒtʃ/", "看；手表", "16", True),
    ("*week", "/wiːk/", "星期；周", "69", True),
    ("wet", "/wet/", "湿的", "16", False),
    ("*when", "/wen/", "什么时候", "9", True),
    ("*window", "/'wɪndəʊ/", "窗户", "8", True),
    ("*word", "/wɜːd/", "单词；词", "17", True),
    ("*work", "/wɜːk/", "工作", "21", True),
    ("workbook", "/'wɜːkbʊk/", "练习册", "21", False),
]

# Verify all words have valid pronunciations
issues = []
for w, p, c, pg, k in VOCAB:
    if p and not p.startswith('/'):
        issues.append(f"Bad phonetic for '{w}': {p}")

if issues:
    for i in issues:
        print(i)
else:
    print("All pronunciations OK")

print(f"\nTotal vocabulary entries: {len(VOCAB)}")
print(f"Key words (with *): {sum(1 for _,_,_,_,k in VOCAB if k)}")
print(f"Non-key words: {sum(1 for _,_,_,_,k in VOCAB if not k)}")

# Generate markdown file
lines = []
lines.append("# 人教版 PEP 四年级下册词汇表\n")
lines.append("> 注：加 `*` 的词为《义务教育英语课程标准（2022年版）》中的二级词。\n")
lines.append("---\n")

# Group by first letter
import string
for letter in string.ascii_uppercase:
    group = [(w, p, c, pg, k) for w, p, c, pg, k in VOCAB if w.lstrip('*').upper().startswith(letter)]
    if group:
        lines.append(f"## {letter}\n")
        lines.append("| 单词 | 音标 | 释义 | 页码 |")
        lines.append("|------|------|------|------|")
        for w, p, c, pg, k in group:
            display = w  # w already contains * prefix for key words
            phonetic = p if p else ""
            lines.append(f"| {display} | {phonetic} | {c} | p. {pg} |")
        lines.append("")

md_content = "\n".join(lines)

output_path = os.path.join(BASE, '四年级下册词汇表.md')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(md_content)

print(f"\nGenerated: {output_path}")
print(f"File size: {os.path.getsize(output_path)} bytes")