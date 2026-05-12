#!/usr/bin/env python3
"""Generate 五年级上册 and 五年级下册 vocabulary markdown files from OCR data."""
import os

BASE = '/Users/allen/Downloads/人教版(PEP)'

# ============================================================
# 五年级上册词汇表
# ============================================================
G5A_VOCAB = [
    # A
    ("afraid", "/ə'freɪd/", "害怕的", "19", False),
    ("agree", "/ə'ɡriː/", "同意", "16", False),
    ("*angry", "/'æŋɡri/", "生气的", "17", True),
    ("*answer", "/'ɑːnsə(r)/", "回答", "33", True),
    ("*ask", "/ɑːsk/", "问", "67", True),
    ("Australia", "/ɒ'streɪliə/", "澳大利亚", "4", False),
    # B
    ("*because", "/bɪ'kɒz/", "因为", "28", True),
    ("beef", "/biːf/", "牛肉", "52", False),
    ("*before", "/bɪ'fɔː(r)/", "在……之前", "69", True),
    ("both", "/bəʊθ/", "两者都", "16", False),
    ("*bring", "/brɪŋ/", "带来", "40", True),
    ("brush", "/brʌʃ/", "刷；刷子", "44", False),
    # C
    ("centre", "/'sentə(r)/", "中心", "17", False),
    ("check", "/tʃek/", "检查", "44", False),
    ("chess", "/tʃes/", "国际象棋", "8", False),
    ("*clever", "/'klevə(r)/", "聪明的", "5", True),
    ("*close", "/kləʊz/", "关；近的", "67", True),
    ("coconut", "/'kəʊkənʌt/", "椰子", "55", False),
    # D
    ("dangerous", "/'deɪndʒərəs/", "危险的", "20", False),
    ("different", "/'dɪfrənt/", "不同的", "57", False),
    ("dumpling", "/'dʌmplɪŋ/", "饺子", "53", False),
    # E
    ("*easy", "/'iːzi/", "容易的", "9", True),
    ("else", "/els/", "其他的；另外", "69", False),
    ("enough", "/ɪ'nʌf/", "足够的", "40", False),
    ("*evening", "/'iːvnɪŋ/", "傍晚；晚上", "32", True),
    ("everything", "/'evriθɪŋ/", "每件事；一切", "64", False),
    ("*excited", "/ɪk'saɪtɪd/", "兴奋的", "16", True),
    ("*exercise", "/'eksəsaɪz/", "锻炼；练习", "40", True),
    # F
    ("*famous", "/'feɪməs/", "著名的", "64", True),
    ("*fine", "/faɪn/", "好的；晴朗的", "67", True),
    ("finish", "/'fɪnɪʃ/", "完成", "40", False),
    ("*fire", "/'faɪə(r)/", "火；火灾", "68", True),
    ("flood", "/flʌd/", "洪水", "68", False),
    ("flu", "/fluː/", "流感", "40", False),
    ("fog", "/fɒɡ/", "雾", "68", False),
    ("forest", "/'fɒrɪst/", "森林", "64", False),
    ("*free", "/friː/", "空闲的；免费的", "45", True),
    ("Friday", "/'fraɪdeɪ/", "星期五", "28", False),
    ("*front", "/frʌnt/", "前面", "9", True),
    # G
    ("go hiking", "/'haɪkɪŋ/", "去远足", "69", False),
    ("grandparent", "/'ɡrænpeərənt/", "祖父母", "44", False),
    # H
    ("habit", "/'hæbɪt/", "习惯", "41", False),
    ("hamburger", "/'hæmbɜːɡə(r)/", "汉堡包", "53", False),
    ("hard-working", "/ˌhɑːd 'wɜːkɪŋ/", "勤奋的", "5", False),
    ("*heavy", "/'hevi/", "重的", "67", True),
    ("*him", "/hɪm/", "他（宾格）", "4", True),
    ("hotel", "/həʊ'tel/", "旅馆", "67", False),
    ("*hour", "/'aʊə(r)/", "小时", "45", True),
    ("*hungry", "/'hʌŋɡri/", "饥饿的", "55", True),
    # I
    ("*ice cream", "/ˌaɪs 'kriːm/", "冰淇淋", "52", True),
    ("if", "/ɪf/", "如果", "16", False),
    ("*interesting", "/'ɪntrəstɪŋ/", "有趣的", "55", True),
    # J
    ("*jump", "/dʒʌmp/", "跳", "8", True),
    # K
    ("*know", "/nəʊ/", "知道", "69", True),
    # L
    ("*Lake", "/leɪk/", "湖", "57", True),
    ("less", "/les/", "更少的", "44", False),
    ("*Lesson", "/'lesn/", "课", "31", True),
    ("*Little", "/'lɪtl/", "小的；少的", "52", True),
    ("lotus", "/'ləʊtəs/", "莲花", "57", False),
    ("*lovely", "/'lʌvli/", "可爱的", "5", True),
    # M
    ("matter", "/'mætə(r)/", "事情；问题", "16", False),
    ("Monday", "/'mʌndeɪ/", "星期一", "29", False),
    ("mountain", "/'maʊntən/", "山；山脉", "64", False),
    ("*move", "/muːv/", "移动；搬家", "21", True),
    ("*Mrs", "/'mɪsɪz/", "夫人", "52", True),
    # N
    ("nature", "/'neɪtʃə(r)/", "自然", "64", False),
    ("*night", "/naɪt/", "夜晚", "33", True),
    # P
    ("*parent", "/'peərənt/", "父；母；家长", "20", True),
    ("*phone", "/fəʊn/", "电话", "43", True),
    ("*piano", "/pi'ænəʊ/", "钢琴", "8", True),
    ("*ping-pong", "/'pɪŋ pɒŋ/", "乒乓球", "33", True),
    ("player", "/'pleɪə(r)/", "运动员；播放器", "4", False),
    ("project", "/'prɒdʒekt/", "项目；课题", "16", False),
    ("pull", "/pʊl/", "拉", "56", False),
    # R
    ("raincoat", "/'reɪnkəʊt/", "雨衣", "67", False),
    ("reply", "/rɪ'plaɪ/", "回复", "33", False),
    ("rest", "/rest/", "休息", "43", False),
    ("*river", "/'rɪvə(r)/", "河流", "64", True),
    ("*robot", "/'rəʊbɒt/", "机器人", "4", True),
    ("root", "/ruːt/", "根", "56", False),
    ("rope", "/rəʊp/", "绳子", "8", False),
    ("round", "/raʊnd/", "圆的", "57", False),
    # S
    ("*sad", "/sæd/", "悲伤的", "16", True),
    ("Saturday", "/'sætədeɪ/", "星期六", "31", False),
    ("*science", "/'saɪəns/", "科学", "7", True),
    ("seed", "/siːd/", "种子", "56", False),
    ("*should", "/ʃʊd/", "应该", "40", True),
    ("*show", "/ʃəʊ/", "展示", "43", True),
    ("*sometimes", "/'sʌmtaɪmz/", "有时", "31", True),
    ("*star", "/stɑː(r)/", "星星；明星", "9", True),
    ("start", "/stɑːt/", "开始", "29", False),
    ("stay", "/steɪ/", "停留；保持", "40", False),
    ("stem", "/stem/", "茎", "56", False),
    ("*subject", "/'sʌbdʒɪkt/", "学科；主题", "28", True),
    ("Sunday", "/'sʌndeɪ/", "星期日", "31", False),
    # T
    ("take care of", "", "照顾", "44", False),
    ("*tea", "/tiː/", "茶；茶叶", "53", True),
    ("team", "/tiːm/", "团队", "4", False),
    ("*then", "/ðen/", "然后", "43", True),
    ("Thursday", "/'θɜːzdeɪ/", "星期四", "29", False),
    ("tooth", "/tuːθ/", "牙齿", "44", False),
    ("trip", "/trɪp/", "旅行", "67", False),
    ("Tuesday", "/'tjuːzdeɪ/", "星期二", "28", False),
    ("twice", "/twaɪs/", "两次", "44", False),
    # U
    ("*umbrella", "/ʌm'brelə/", "雨伞", "67", True),
    ("usually", "/'juːʒuəli/", "通常", "31", False),
    # V
    ("*visit", "/'vɪzɪt/", "参观；访问", "33", True),
    # W
    ("waterfall", "/'wɔːtəfɔːl/", "瀑布", "64", False),
    ("*way", "/weɪ/", "方法；路", "57", True),
    ("Wednesday", "/'wenzdeɪ/", "星期三", "28", False),
    ("weekend", "/ˌwiːk'end/", "周末", "31", False),
    ("wind", "/wɪnd/", "风", "67", False),
    ("*wonderful", "/'wʌndəfl/", "精彩的", "9", True),
    ("*world", "/wɜːld/", "世界", "57", True),
    ("worried", "/'wʌrid/", "担心的", "16", False),
    ("*worry", "/'wʌri/", "担心", "67", True),
    ("*wrong", "/rɒŋ/", "错误的", "17", True),
    # Y
    ("*young", "/jʌŋ/", "年轻的", "5", True),
    ("yours", "/jɔːz/", "你的（名词性）", "21", False),
]

# ============================================================
# 五年级下册词汇表
# ============================================================
G5B_VOCAB = [
    # A
    ("*ago", "/ə'ɡəʊ/", "以前", "33", True),
    ("along", "/ə'lɒŋ/", "沿着", "16", False),
    ("app", "/æp/", "应用程序", "67", False),
    ("April", "/'eɪprəl/", "四月", "29", False),
    ("artist", "/'ɑːtɪst/", "艺术家", "20", False),
    ("August", "/'ɔːɡəst/", "八月", "32", False),
    # B
    ("*beach", "/biːtʃ/", "海滩", "40", True),
    ("*behind", "/bɪ'haɪnd/", "在……后面", "40", True),
    ("Beijing opera", "/'ɒprə/", "京剧", "41", False),
    ("*beside", "/bɪ'saɪd/", "在……旁边", "33", True),
    ("*between", "/bɪ'twiːn/", "在……之间", "17", True),
    ("*bike", "/baɪk/", "自行车", "52", True),
    ("blog", "/blɒɡ/", "博客", "68", False),
    ("borrow", "/'bɒrəʊ/", "借", "9", False),
    ("Britain", "/'brɪtn/", "英国", "44", False),
    ("building", "/'bɪldɪŋ/", "建筑物", "69", False),
    # C
    ("Cairo", "/'kaɪrəʊ/", "开罗", "45", False),
    ("camel", "/'kæml/", "骆驼", "45", False),
    ("carry", "/'kæri/", "搬运；携带", "57", False),
    ("*catch", "/kætʃ/", "抓住；赶上", "33", True),
    ("celebrate", "/'selɪbreɪt/", "庆祝", "31", False),
    ("Christmas", "/'krɪsməs/", "圣诞节", "31", False),
    ("*cinema", "/'sɪnəmə/", "电影院", "17", True),
    ("*city", "/'sɪti/", "城市", "17", True),
    ("common", "/'kɒmən/", "普通的；共同的", "41", False),
    ("Confucius", "/kən'fjuːʃəs/", "孔子", "17", False),
    ("could", "/kʊd/", "可以（can的过去式）", "43", False),
    ("country", "/'kʌntri/", "国家", "33", False),
    ("CPC Founding Day", "/'faʊndɪŋ/", "中国共产党建党日", "32", False),
    ("culture", "/'kʌltʃə(r)/", "文化", "65", False),
    ("*cup", "/kʌp/", "杯子", "33", True),
    # D
    ("December", "/dɪ'sembə(r)/", "十二月", "31", False),
    ("desert", "/'dezət/", "沙漠", "41", False),
    ("direct", "/də'rekt/", "直接的", "20", False),
    ("Dragon Boat Festival", "/'festɪvl/", "端午节", "29", False),
    # E
    ("*early", "/'ɜːli/", "早的", "52", True),
    ("environment", "/ɪn'vaɪrənmənt/", "环境", "57", False),
    ("even", "/'iːvn/", "甚至", "45", False),
    ("everyday", "/'evrideɪ/", "日常的", "57", False),
    ("explore", "/ɪk'splɔː(r)/", "探索", "65", False),
    # F
    ("*far", "/fɑː(r)/", "远的", "16", True),
    ("February", "/'februəri/", "二月", "28", False),
    ("feel like", "", "感觉像；想要", "45", False),
    ("finally", "/'faɪnəli/", "最后", "57", False),
    ("flash", "/flæʃ/", "闪光", "8", False),
    ("*foot", "/fʊt/", "脚", "40", True),
    ("foreign", "/'fɒrən/", "外国的", "21", False),
    # G
    ("grassland", "/'ɡrɑːslænd/", "草原", "41", False),
    ("guard", "/ɡɑːd/", "守卫", "7", False),
    # H
    ("Hawaii", "/hə'waɪiː/", "夏威夷", "45", False),
    ("health", "/helθ/", "健康", "57", False),
    ("high", "/haɪ/", "高的", "44", False),
    ("*hill", "/hɪl/", "小山", "65", True),
    ("history", "/'hɪstri/", "历史", "65", False),
    ("*holiday", "/'hɒlədeɪ/", "假期", "29", True),
    ("*hometown", "/'həʊmtaʊn/", "家乡", "40", True),
    ("hot pot", "/pɒt/", "火锅", "65", False),
    ("*hurt", "/hɜːt/", "受伤；伤害", "57", True),
    # I
    ("*ice", "/aɪs/", "冰", "33", True),
    ("India", "/'ɪndiə/", "印度", "43", False),
    ("information", "/ˌɪnfə'meɪʃn/", "信息", "68", False),
    ("inside", "/ˌɪn'saɪd/", "在里面", "4", False),
    ("*internet", "/'ɪntənet/", "互联网", "64", True),
    ("island", "/'aɪlənd/", "岛屿", "44", False),
    ("Italy", "/'ɪtəli/", "意大利", "43", False),
    ("*its", "/ɪts/", "它的", "53", True),
    # J
    ("January", "/'dʒænjuəri/", "一月", "28", False),
    ("join", "/dʒɔɪn/", "加入", "64", False),
    ("July", "/dʒu'laɪ/", "七月", "32", False),
    ("June", "/dʒuːn/", "六月", "29", False),
    # K
    ("kangaroo", "/ˌkæŋɡə'ruː/", "袋鼠", "43", False),
    ("koala", "/kəʊ'ɑːlə/", "考拉", "43", False),
    # L
    ("Labour Day", "/'leɪbə(r)/", "劳动节", "29", False),
    ("*last", "/lɑːst/", "最后的；上一个", "69", True),
    ("*Left", "/left/", "左边的", "17", True),
    ("line", "/laɪn/", "线；路线", "7", False),
    ("litter", "/'lɪtə(r)/", "垃圾；乱扔", "19", False),
    ("*Live", "/lɪv/", "居住", "21", True),
    ("local", "/'ləʊkl/", "当地的", "65", False),
    ("lost", "/lɒst/", "丢失的；迷路的", "21", False),
    # M
    ("magazine", "/ˌmæɡə'ziːn/", "杂志", "68", False),
    ("March", "/mɑːtʃ/", "三月", "29", False),
    ("May", "/meɪ/", "五月", "29", False),
    ("maybe", "/'meɪbi/", "也许", "64", False),
    ("*middle", "/'mɪdl/", "中间的", "45", True),
    ("Mount Taishan", "/maʊnt/", "泰山", "41", False),
    ("*Ms", "/mɪz/", "女士", "19", True),
    ("*must", "/mʌst/", "必须", "4", True),
    # N
    ("National Day", "/'næʃnəl/", "国庆节", "32", False),
    ("*next", "/nekst/", "下一个", "16", True),
    ("northeast", "/ˌnɔːθ'iːst/", "东北", "64", False),
    ("note", "/nəʊt/", "笔记", "21", False),
    ("November", "/nəʊ'vembə(r)/", "十一月", "32", False),
    # O
    ("October", "/ɒk'təʊbə(r)/", "十月", "32", False),
    ("on foot", "", "步行", "53", False),
    ("*open", "/'əʊpən/", "打开", "9", True),
    # P
    ("painting", "/'peɪntɪŋ/", "绘画", "45", False),
    ("palace", "/'pæləs/", "宫殿", "69", False),
    ("*party", "/'pɑːti/", "聚会；派对", "29", True),
    ("password", "/'pɑːswɜːd/", "密码", "5", False),
    ("PLA Day", "", "中国人民解放军建军节", "32", False),
    ("plan", "/plæn/", "计划", "67", False),
    ("*plane", "/pleɪn/", "飞机", "53", True),
    ("pyramid", "/'pɪrəmɪd/", "金字塔", "45", False),
    # R
    ("recycle", "/ˌriː'saɪkl/", "回收利用", "20", False),
    ("return", "/rɪ'tɜːn/", "返回；归还", "9", False),
    ("ride", "/raɪd/", "骑", "45", False),
    # S
    ("scare", "/skeə(r)/", "吓唬", "4", False),
    ("scientist", "/'saɪəntɪst/", "科学家", "20", False),
    ("seafood", "/'siːfuːd/", "海鲜", "69", False),
    ("September", "/sep'tembə(r)/", "九月", "32", False),
    ("*ship", "/ʃɪp/", "船", "53", True),
    ("shout", "/ʃaʊt/", "喊叫", "7", False),
    ("sign", "/saɪn/", "标志", "21", False),
    ("sir", "/sɜː(r)/", "先生", "4", False),
    ("*sit", "/sɪt/", "坐", "33", True),
    ("skate", "/skeɪt/", "滑冰", "28", False),
    ("smoke", "/sməʊk/", "吸烟；烟", "8", False),
    ("special", "/'speʃl/", "特别的", "45", False),
    ("*stand", "/stænd/", "站立", "7", True),
    ("station", "/'steɪʃn/", "车站", "16", False),
    ("stone", "/stəʊn/", "石头", "69", False),
    ("*street", "/striːt/", "街道", "16", True),
    ("suggest", "/sə'dʒest/", "建议", "57", False),
    ("sunshine", "/'sʌnʃaɪn/", "阳光", "33", False),
    # T
    ("*taxi", "/'tæksi/", "出租车", "20", True),
    ("teach", "/tiːtʃ/", "教", "7", False),
    ("tip", "/tɪp/", "小费；提示", "33", False),
    ("tour", "/tʊə(r)/", "旅游", "65", False),
    ("traffic", "/'træfɪk/", "交通", "20", False),
    ("*train", "/treɪn/", "火车", "43", True),
    ("*travel", "/'trævl/", "旅行", "45", True),
    ("turkey", "/'tɜːki/", "火鸡", "43", False),
    # U
    ("underground", "/'ʌndəɡraʊnd/", "地铁", "52", False),
    # V
    ("visitor", "/'vɪzɪtə(r)/", "参观者", "21", False),
    ("volunteer", "/ˌvɒlən'tɪə(r)/", "志愿者", "21", False),
    # W
    ("*wait", "/weɪt/", "等待", "19", True),
    ("west", "/west/", "西方", "57", False),
    ("wild", "/waɪld/", "野生的", "43", False),
    ("*wish", "/wɪʃ/", "愿望；希望", "21", True),
    ("*write", "/raɪt/", "写", "9", True),
]

def generate_md(vocab, title, output_path):
    lines = [f"# {title}\n"]
    lines.append("> 注：加 `*` 的词为《义务教育英语课程标准（2022年版）》中的二级词。\n")
    lines.append("---\n")

    import string
    for letter in string.ascii_uppercase:
        group = [(w, p, c, pg, k) for w, p, c, pg, k in vocab if w.lstrip('*').upper().startswith(letter)]
        if group:
            lines.append(f"## {letter}\n")
            lines.append("| 单词 | 音标 | 释义 | 页码 |")
            lines.append("|------|------|------|------|")
            for w, p, c, pg, k in group:
                phonetic = p if p else ""
                lines.append(f"| {w} | {phonetic} | {c} | p. {pg} |")
            lines.append("")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    return len([1 for _ in vocab])

# Generate both files
n1 = generate_md(G5A_VOCAB, "人教版 PEP 五年级上册词汇表",
                 os.path.join(BASE, '五年级上册词汇表.md'))
n2 = generate_md(G5B_VOCAB, "人教版 PEP 五年级下册词汇表",
                 os.path.join(BASE, '五年级下册词汇表.md'))

print(f"五年级上册词汇表.md: {n1} entries")
print(f"  Key: {sum(1 for _,_,_,_,k in G5A_VOCAB if k)}")
print(f"  Non-key: {sum(1 for _,_,_,_,k in G5A_VOCAB if not k)}")
print(f"五年级下册词汇表.md: {n2} entries")
print(f"  Key: {sum(1 for _,_,_,_,k in G5B_VOCAB if k)}")
print(f"  Non-key: {sum(1 for _,_,_,_,k in G5B_VOCAB if not k)}")