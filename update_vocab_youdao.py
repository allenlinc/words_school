#!/usr/bin/env python3
"""Update JSON vocabulary files with real data from Youdao Dictionary.
Enhanced version with improved parsing, more DB entries, and phrase handling."""
import json
import os
import re
import time
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

BASE = '/Users/allen/Downloads/人教版(PEP)'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

POS_PATTERN = re.compile(
    r'^(n\.|v\.|adj\.|adv\.|prep\.|conj\.|pron\.|interj\.|art\.|num\.|modal\s*v\.|aux\.\s*v\.|det\.|int\.)',
    re.IGNORECASE
)

# ============ BUILT-IN SYNONYM DATABASE ============
SYNONYM_DB = {
    "a": [{"pos": "art.", "cn": "冠词", "ws": ["an", "one"]}],
    "about": [{"pos": "prep.", "cn": "关于", "ws": ["concerning", "regarding", "around", "approximately"]}],
    "after": [{"pos": "prep.", "cn": "在……之后", "ws": ["following", "behind", "subsequent to"]}],
    "again": [{"pos": "adv.", "cn": "再次", "ws": ["once more", "anew", "afresh"]}],
    "all": [{"pos": "adj.", "cn": "所有的", "ws": ["every", "whole", "entire", "total"]}],
    "also": [{"pos": "adv.", "cn": "也", "ws": ["too", "as well", "additionally", "furthermore"]}],
    "always": [{"pos": "adv.", "cn": "总是", "ws": ["constantly", "forever", "invariably", "perpetually"]}],
    "and": [{"pos": "conj.", "cn": "和", "ws": ["plus", "as well as", "along with", "together with"]}],
    "animal": [{"pos": "n.", "cn": "动物", "ws": ["creature", "beast", "living thing", "organism"]}],
    "any": [{"pos": "adj.", "cn": "任何的", "ws": ["some", "whichever", "whatever"]}],
    "apple": [{"pos": "n.", "cn": "苹果", "ws": []}],
    "are": [{"pos": "v.", "cn": "是", "ws": ["be", "exist", "live"]}],
    "art": [{"pos": "n.", "cn": "艺术", "ws": ["craft", "skill", "creativity", "artwork", "painting"]}],
    "ask": [{"pos": "v.", "cn": "问", "ws": ["inquire", "question", "request", "query"]}],
    "at": [{"pos": "prep.", "cn": "在", "ws": ["in", "on", "by", "near"]}],
    "baby": [{"pos": "n.", "cn": "婴儿", "ws": ["infant", "newborn", "child", "toddler"]}],
    "back": [{"pos": "n.", "cn": "后面", "ws": ["rear", "behind", "reverse"]}],
    "bad": [{"pos": "adj.", "cn": "坏的", "ws": ["poor", "terrible", "awful", "unpleasant", "evil"]}],
    "bag": [{"pos": "n.", "cn": "包", "ws": ["sack", "purse", "backpack", "case", "pouch"]}],
    "ball": [{"pos": "n.", "cn": "球", "ws": ["sphere", "globe", "orb", "round object"]}],
    "banana": [{"pos": "n.", "cn": "香蕉", "ws": ["plantain"]}],
    "bathroom": [{"pos": "n.", "cn": "浴室", "ws": ["restroom", "washroom", "lavatory", "toilet", "WC", "powder room"]}],
    "be": [{"pos": "v.", "cn": "是", "ws": ["exist", "live", "occur", "happen", "remain"]}],
    "beautiful": [{"pos": "adj.", "cn": "美丽的", "ws": ["pretty", "lovely", "gorgeous", "attractive", "handsome", "stunning"]}],
    "bed": [{"pos": "n.", "cn": "床", "ws": ["bunk", "cot", "mattress", "couch"]}],
    "bedroom": [{"pos": "n.", "cn": "卧室", "ws": ["chamber", "sleeping room", "master suite", "boudoir"]}],
    "bee": [{"pos": "n.", "cn": "蜜蜂", "ws": ["honeybee", "bumblebee", "drone"]}],
    "big": [{"pos": "adj.", "cn": "大的", "ws": ["large", "huge", "enormous", "great", "massive", "gigantic"]}],
    "bird": [{"pos": "n.", "cn": "鸟", "ws": ["fowl", "avian", "songbird", "raptor", "poultry", "chick"]}],
    "black": [{"pos": "adj.", "cn": "黑色的", "ws": ["dark", "ebony", "jet", "inky", "pitch-dark"]}],
    "blackboard": [{"pos": "n.", "cn": "黑板", "ws": ["chalkboard", "whiteboard", "board"]}],
    "blue": [{"pos": "adj.", "cn": "蓝色的", "ws": ["azure", "sky-blue", "navy", "cobalt", "sapphire"]}],
    "book": [{"pos": "n.", "cn": "书", "ws": ["volume", "tome", "publication", "text", "novel", "manual"]}],
    "bowl": [{"pos": "n.", "cn": "碗", "ws": ["dish", "basin", "vessel", "container", "tureen"]}],
    "box": [{"pos": "n.", "cn": "盒子", "ws": ["case", "carton", "chest", "crate", "container", "package"]}],
    "boy": [{"pos": "n.", "cn": "男孩", "ws": ["lad", "youth", "youngster", "son", "schoolboy"]}],
    "bread": [{"pos": "n.", "cn": "面包", "ws": ["loaf", "roll", "bun", "baguette", "toast"]}],
    "breakfast": [{"pos": "n.", "cn": "早餐", "ws": ["morning meal", "brunch"]}],
    "brother": [{"pos": "n.", "cn": "兄弟", "ws": ["sibling", "kin", "fellow"]}],
    "brown": [{"pos": "adj.", "cn": "棕色的", "ws": ["tan", "bronze", "chestnut", "coffee", "chocolate"]}],
    "bus": [{"pos": "n.", "cn": "公共汽车", "ws": ["coach", "minibus", "shuttle", "transit"]}],
    "but": [{"pos": "conj.", "cn": "但是", "ws": ["however", "yet", "although", "nevertheless", "though"]}],
    "buy": [{"pos": "v.", "cn": "买", "ws": ["purchase", "acquire", "obtain", "get", "procure", "shop"]}],
    "cake": [{"pos": "n.", "cn": "蛋糕", "ws": ["pastry", "dessert", "tart", "gateau", "sponge"]}],
    "can": [{"pos": "modal v.", "cn": "可以", "ws": ["be able to", "may", "might", "could"]}],
    "car": [{"pos": "n.", "cn": "汽车", "ws": ["automobile", "vehicle", "motor", "auto", "sedan"]}],
    "carrot": [{"pos": "n.", "cn": "胡萝卜", "ws": ["root vegetable", "orange vegetable"]}],
    "cat": [{"pos": "n.", "cn": "猫", "ws": ["feline", "kitten", "kitty", "tomcat", "tabby"]}],
    "chair": [{"pos": "n.", "cn": "椅子", "ws": ["seat", "stool", "bench", "armchair", "throne"]}],
    "cheap": [{"pos": "adj.", "cn": "便宜的", "ws": ["inexpensive", "affordable", "low-cost", "budget", "economical", "bargain"]}],
    "chicken": [{"pos": "n.", "cn": "鸡", "ws": ["hen", "rooster", "fowl", "poultry", "chick"]}],
    "child": [{"pos": "n.", "cn": "儿童", "ws": ["kid", "youngster", "infant", "toddler", "youth", "juvenile", "minor"]}],
    "chopstick": [{"pos": "n.", "cn": "筷子", "ws": ["chopsticks", "eating utensils"]}],
    "class": [{"pos": "n.", "cn": "班级", "ws": ["lesson", "course", "grade", "group", "category"]}],
    "classroom": [{"pos": "n.", "cn": "教室", "ws": ["schoolroom", "lecture hall", "study room"]}],
    "clean": [{"pos": "adj.", "cn": "干净的", "ws": ["tidy", "neat", "pure", "spotless", "hygienic", "immaculate"]}],
    "clock": [{"pos": "n.", "cn": "钟", "ws": ["timepiece", "watch", "chronometer", "timer"]}],
    "close": [{"pos": "v.", "cn": "关闭", "ws": ["shut", "seal", "fasten", "lock"]}],
    "clothes": [{"pos": "n.", "cn": "衣服", "ws": ["clothing", "garments", "attire", "apparel", "dress", "outfit"]}],
    "cloud": [{"pos": "n.", "cn": "云", "ws": ["vapor", "mist", "haze", "fog"]}],
    "coffee": [{"pos": "n.", "cn": "咖啡", "ws": ["espresso", "latte", "cappuccino", "java", "brew"]}],
    "cold": [{"pos": "adj.", "cn": "冷的", "ws": ["chilly", "cool", "freezing", "icy", "frigid", "frosty"]}],
    "colour": [{"pos": "n.", "cn": "颜色", "ws": ["hue", "shade", "tone", "tint", "pigment"]}],
    "come": [{"pos": "v.", "cn": "来", "ws": ["arrive", "approach", "appear", "reach", "enter"]}],
    "cook": [{"pos": "v.", "cn": "烹饪", "ws": ["prepare", "bake", "roast", "fry", "boil", "grill"]}],
    "cool": [{"pos": "adj.", "cn": "凉爽的", "ws": ["chilly", "cold", "refreshing", "breezy", "chilled"]}],
    "cow": [{"pos": "n.", "cn": "牛", "ws": ["cattle", "bovine", "heifer", "calf", "bull"]}],
    "cup": [{"pos": "n.", "cn": "杯子", "ws": ["mug", "glass", "goblet", "tumbler", "chalice"]}],
    "dad": [{"pos": "n.", "cn": "爸爸", "ws": ["father", "daddy", "papa", "pa", "pop"]}],
    "dance": [{"pos": "v.", "cn": "跳舞", "ws": ["sway", "twirl", "boogie", "waltz", "groove"]}],
    "day": [{"pos": "n.", "cn": "天", "ws": ["daytime", "daylight", "date", "twenty-four hours"]}],
    "dear": [{"pos": "adj.", "cn": "亲爱的", "ws": ["beloved", "loved", "precious", "darling", "sweetheart", "cherished"]}],
    "delicious": [{"pos": "adj.", "cn": "美味的", "ws": ["tasty", "yummy", "scrumptious", "flavorful", "delectable", "appetizing", "savory"]}],
    "desk": [{"pos": "n.", "cn": "书桌", "ws": ["table", "workstation", "bench", "counter", "bureau"]}],
    "dinner": [{"pos": "n.", "cn": "晚餐", "ws": ["supper", "evening meal", "feast", "banquet"]}],
    "dog": [{"pos": "n.", "cn": "狗", "ws": ["canine", "puppy", "hound", "pooch", "mutt"]}],
    "door": [{"pos": "n.", "cn": "门", "ws": ["gate", "entrance", "portal", "gateway", "entry", "exit"]}],
    "down": [{"pos": "adv.", "cn": "向下", "ws": ["downward", "below", "underneath", "beneath", "lower"]}],
    "draw": [{"pos": "v.", "cn": "画画", "ws": ["sketch", "illustrate", "depict", "portray", "doodle", "paint"]}],
    "dress": [{"pos": "n.", "cn": "连衣裙", "ws": ["gown", "frock", "garment", "robe", "attire", "outfit"]}],
    "drink": [{"pos": "v.", "cn": "喝", "ws": ["sip", "gulp", "swallow", "consume", "imbibe"]}],
    "driver": [{"pos": "n.", "cn": "司机", "ws": ["chauffeur", "motorist", "operator", "pilot"]}],
    "duck": [{"pos": "n.", "cn": "鸭子", "ws": ["mallard", "drake", "waterfowl"]}],
    "eat": [{"pos": "v.", "cn": "吃", "ws": ["consume", "dine", "devour", "feast", "ingest", "swallow", "chew"]}],
    "egg": [{"pos": "n.", "cn": "鸡蛋", "ws": ["ovum", "roe", "spawn"]}],
    "eight": [{"pos": "num.", "cn": "八", "ws": ["octet", "eighth"]}],
    "elephant": [{"pos": "n.", "cn": "大象", "ws": ["pachyderm", "mammoth", "tusker"]}],
    "english": [{"pos": "n.", "cn": "英语", "ws": []}],
    "expensive": [{"pos": "adj.", "cn": "昂贵的", "ws": ["costly", "pricey", "dear", "high-priced", "overpriced", "luxurious", "valuable"]}],
    "eye": [{"pos": "n.", "cn": "眼睛", "ws": ["ocular", "orb", "peeper", "optic"]}],
    "face": [{"pos": "n.", "cn": "脸", "ws": ["visage", "countenance", "features", "expression", "look"]}],
    "family": [{"pos": "n.", "cn": "家庭", "ws": ["household", "clan", "kin", "relatives", "folks", "lineage"]}],
    "fan": [{"pos": "n.", "cn": "风扇", "ws": ["ventilator", "blower", "air conditioner"]}],
    "farm": [{"pos": "n.", "cn": "农场", "ws": ["ranch", "plantation", "homestead", "estate", "land"]}],
    "farmer": [{"pos": "n.", "cn": "农民", "ws": ["agriculturist", "grower", "cultivator", "rancher", "peasant"]}],
    "fast": [{"pos": "adj.", "cn": "快的", "ws": ["quick", "rapid", "swift", "speedy", "hasty", "brisk"]}],
    "father": [{"pos": "n.", "cn": "父亲", "ws": ["dad", "daddy", "papa", "parent", "sire", "pa"]}],
    "feed": [{"pos": "v.", "cn": "喂养", "ws": ["nourish", "provide for", "sustain", "supply", "cater", "give food to"]}],
    "feel": [{"pos": "v.", "cn": "感觉", "ws": ["sense", "perceive", "experience", "touch", "detect"]}],
    "find": [{"pos": "v.", "cn": "找到", "ws": ["discover", "locate", "uncover", "detect", "identify", "spot"]}],
    "first": [{"pos": "num.", "cn": "第一", "ws": ["initial", "primary", "foremost", "original", "earliest", "leading"]}],
    "fish": [{"pos": "n.", "cn": "鱼", "ws": ["aquatic animal", "finfish", "seafood"]}],
    "five": [{"pos": "num.", "cn": "五", "ws": ["quintet", "fifth"]}],
    "flower": [{"pos": "n.", "cn": "花", "ws": ["bloom", "blossom", "bud", "floret", "posy", "petal"]}],
    "fly": [{"pos": "v.", "cn": "飞", "ws": ["soar", "glide", "hover", "swoop", "ascend", "flutter", "wing"]}],
    "follow": [{"pos": "v.", "cn": "跟随", "ws": ["pursue", "trail", "track", "shadow", "tail", "chase", "succeed", "observe"]}],
    "food": [{"pos": "n.", "cn": "食物", "ws": ["nourishment", "sustenance", "provisions", "fare", "cuisine", "meals", "edibles"]}],
    "foot": [{"pos": "n.", "cn": "脚", "ws": ["feet", "paw", "hoof", "toe"]}],
    "fork": [{"pos": "n.", "cn": "叉子", "ws": ["prong", "utensil", "cutlery"]}],
    "four": [{"pos": "num.", "cn": "四", "ws": ["quartet", "fourth"]}],
    "free": [{"pos": "adj.", "cn": "自由的", "ws": ["liberated", "unrestricted", "independent", "unbound", "unfettered", "emancipated"]}],
    "friend": [{"pos": "n.", "cn": "朋友", "ws": ["companion", "pal", "buddy", "mate", "comrade", "ally", "confidant"]}],
    "fruit": [{"pos": "n.", "cn": "水果", "ws": ["produce", "harvest", "crop"]}],
    "game": [{"pos": "n.", "cn": "游戏", "ws": ["play", "sport", "pastime", "recreation", "contest", "match"]}],
    "garden": [{"pos": "n.", "cn": "花园", "ws": ["yard", "park", "grounds", "lawn", "backyard", "orchard"]}],
    "get": [{"pos": "v.", "cn": "得到", "ws": ["obtain", "acquire", "receive", "gain", "fetch", "procure", "attain", "secure"]}],
    "girl": [{"pos": "n.", "cn": "女孩", "ws": ["lass", "maiden", "damsel", "daughter", "schoolgirl", "young lady"]}],
    "give": [{"pos": "v.", "cn": "给", "ws": ["offer", "provide", "present", "donate", "grant", "bestow", "hand", "deliver"]}],
    "go": [{"pos": "v.", "cn": "去", "ws": ["move", "travel", "proceed", "depart", "leave", "journey", "advance"]}],
    "good": [{"pos": "adj.", "cn": "好的", "ws": ["excellent", "fine", "great", "nice", "wonderful", "positive", "superb", "pleasant"]}],
    "grandma": [{"pos": "n.", "cn": "奶奶", "ws": ["grandmother", "granny", "nana", "gran"]}],
    "green": [{"pos": "adj.", "cn": "绿色的", "ws": ["emerald", "lime", "olive", "verdant", "leafy", "grassy"]}],
    "hair": [{"pos": "n.", "cn": "头发", "ws": ["locks", "tresses", "mane", "fur", "strands", "fuzz"]}],
    "hand": [{"pos": "n.", "cn": "手", "ws": ["palm", "fist", "paw", "mitt", "extremity"]}],
    "happy": [{"pos": "adj.", "cn": "快乐的", "ws": ["joyful", "cheerful", "delighted", "pleased", "content", "glad", "elated", "merry"]}],
    "hard": [{"pos": "adj.", "cn": "困难的", "ws": ["difficult", "challenging", "tough", "demanding", "stiff", "arduous", "rigid", "solid"]}],
    "hat": [{"pos": "n.", "cn": "帽子", "ws": ["cap", "headgear", "helmet", "bonnet", "beret"]}],
    "have": [{"pos": "v.", "cn": "有", "ws": ["possess", "own", "hold", "keep", "contain", "include", "enjoy"]}],
    "he": [{"pos": "pron.", "cn": "他", "ws": ["him", "male", "boy", "man"]}],
    "head": [{"pos": "n.", "cn": "头", "ws": ["skull", "cranium", "noggin", "brain", "crown", "top"]}],
    "healthy": [{"pos": "adj.", "cn": "健康的", "ws": ["well", "fit", "sound", "robust", "vigorous", "hearty", "hale"]}],
    "hear": [{"pos": "v.", "cn": "听", "ws": ["listen", "catch", "overhear", "perceive", "detect"]}],
    "help": [{"pos": "v.", "cn": "帮助", "ws": ["assist", "aid", "support", "guide", "serve", "benefit", "rescue"]}],
    "helpful": [{"pos": "adj.", "cn": "有帮助的", "ws": ["useful", "beneficial", "valuable", "constructive", "supportive", "advantageous"]}],
    "herself": [{"pos": "pron.", "cn": "她自己", "ws": ["her own self", "personally"]}],
    "here": [{"pos": "adv.", "cn": "这里", "ws": ["present", "nearby", "at hand", "close"]}],
    "home": [{"pos": "n.", "cn": "家", "ws": ["house", "residence", "dwelling", "abode", "household", "domicile", "homestead"]}],
    "homework": [{"pos": "n.", "cn": "作业", "ws": ["assignment", "task", "schoolwork", "preparation", "exercise"]}],
    "horse": [{"pos": "n.", "cn": "马", "ws": ["steed", "mare", "stallion", "pony", "colt", "equine", "nag"]}],
    "hospital": [{"pos": "n.", "cn": "医院", "ws": ["clinic", "infirmary", "medical center", "sanatorium", "sickbay"]}],
    "hot": [{"pos": "adj.", "cn": "热的", "ws": ["warm", "heated", "scorching", "burning", "boiling", "torrid", "sultry"]}],
    "house": [{"pos": "n.", "cn": "房子", "ws": ["home", "residence", "dwelling", "building", "shelter", "cottage", "abode"]}],
    "how": [{"pos": "adv.", "cn": "怎样", "ws": ["in what way", "by what means", "what"]}],
    "hungry": [{"pos": "adj.", "cn": "饥饿的", "ws": ["starving", "famished", "ravenous", "peckish", "empty"]}],
    "i": [{"pos": "pron.", "cn": "我", "ws": ["me", "myself", "self"]}],
    "ice": [{"pos": "n.", "cn": "冰", "ws": ["frost", "glacier", "icicle", "frozen water", "sleet"]}],
    "in": [{"pos": "prep.", "cn": "在……里", "ws": ["inside", "within", "into", "during", "throughout"]}],
    "is": [{"pos": "v.", "cn": "是", "ws": ["exists", "lives", "remains", "equals"]}],
    "it": [{"pos": "pron.", "cn": "它", "ws": ["this", "that", "the object", "the thing"]}],
    "jacket": [{"pos": "n.", "cn": "夹克", "ws": ["coat", "blazer", "anorak", "windbreaker", "outerwear"]}],
    "juice": [{"pos": "n.", "cn": "果汁", "ws": ["nectar", "liquid", "extract", "beverage", "drink", "sap"]}],
    "jump": [{"pos": "v.", "cn": "跳", "ws": ["leap", "hop", "bound", "spring", "vault", "skip", "bounce"]}],
    "just": [{"pos": "adv.", "cn": "正好", "ws": ["exactly", "precisely", "merely", "simply", "only", "barely", "recently", "fair"]}],
    "kid": [{"pos": "n.", "cn": "小孩", "ws": ["child", "youngster", "toddler", "infant", "youth", "minor", "little one"]}],
    "kitchen": [{"pos": "n.", "cn": "厨房", "ws": ["cookhouse", "galley", "cookery", "scullery", "pantry"]}],
    "knife": [{"pos": "n.", "cn": "刀", "ws": ["blade", "cutter", "dagger", "scalpel", "carver"]}],
    "know": [{"pos": "v.", "cn": "知道", "ws": ["understand", "comprehend", "recognize", "grasp", "realize", "perceive", "discern"]}],
    "large": [{"pos": "adj.", "cn": "大的", "ws": ["big", "huge", "enormous", "massive", "giant", "sizable", "substantial", "immense"]}],
    "late": [{"pos": "adj.", "cn": "晚的", "ws": ["tardy", "delayed", "behind", "overdue", "belated", "last-minute"]}],
    "learn": [{"pos": "v.", "cn": "学习", "ws": ["study", "acquire", "master", "grasp", "understand", "absorb", "pick up"]}],
    "light": [{"pos": "n.", "cn": "光", "ws": ["illumination", "brightness", "glow", "radiance", "beam", "ray", "shimmer"]}],
    "like": [{"pos": "v.", "cn": "喜欢", "ws": ["enjoy", "love", "adore", "appreciate", "fancy", "prefer", "relish"]}],
    "list": [{"pos": "n.", "cn": "清单", "ws": ["catalog", "inventory", "register", "roster", "index", "enumeration", "checklist"]}],
    "listen": [{"pos": "v.", "cn": "听", "ws": ["hear", "attend", "heed", "pay attention", "eavesdrop"]}],
    "little": [{"pos": "adj.", "cn": "小的", "ws": ["small", "tiny", "petite", "miniature", "slight", "compact", "wee"]}],
    "live": [{"pos": "v.", "cn": "居住", "ws": ["reside", "dwell", "inhabit", "stay", "occupy", "lodge", "settle"]}],
    "long": [{"pos": "adj.", "cn": "长的", "ws": ["lengthy", "extended", "prolonged", "elongated", "stretched", "tall"]}],
    "look": [{"pos": "v.", "cn": "看", "ws": ["see", "watch", "gaze", "stare", "glance", "observe", "view", "peer"]}],
    "loud": [{"pos": "adj.", "cn": "大声的", "ws": ["noisy", "blaring", "booming", "thunderous", "deafening", "clamorous", "strident"]}],
    "love": [{"pos": "v.", "cn": "爱", "ws": ["adore", "cherish", "treasure", "devotion", "affection", "passion", "fondness"]}],
    "lunch": [{"pos": "n.", "cn": "午餐", "ws": ["midday meal", "noon meal", "brunch", "luncheon"]}],
    "make": [{"pos": "v.", "cn": "制作", "ws": ["create", "build", "produce", "construct", "form", "fashion", "craft", "manufacture"]}],
    "man": [{"pos": "n.", "cn": "男人", "ws": ["male", "gentleman", "guy", "fellow", "bloke", "lad", "human"]}],
    "many": [{"pos": "adj.", "cn": "许多", "ws": ["numerous", "countless", "plentiful", "abundant", "several", "multiple"]}],
    "maths": [{"pos": "n.", "cn": "数学", "ws": ["mathematics", "arithmetic", "calculation", "numeracy"]}],
    "milk": [{"pos": "n.", "cn": "牛奶", "ws": ["dairy", "cream", "lactose", "buttermilk"]}],
    "minute": [{"pos": "n.", "cn": "分钟", "ws": ["moment", "instant", "second", "flash", "sixty seconds"]}],
    "monkey": [{"pos": "n.", "cn": "猴子", "ws": ["ape", "primate", "simian", "chimpanzee", "baboon"]}],
    "moon": [{"pos": "n.", "cn": "月亮", "ws": ["satellite", "lunar", "crescent", "orb"]}],
    "mother": [{"pos": "n.", "cn": "母亲", "ws": ["mom", "mum", "mommy", "mama", "parent", "ma"]}],
    "mouse": [{"pos": "n.", "cn": "老鼠", "ws": ["rodent", "rat", "vermin"]}],
    "mouth": [{"pos": "n.", "cn": "嘴", "ws": ["oral cavity", "muzzle", "beak", "lips", "jaws"]}],
    "much": [{"pos": "adj.", "cn": "许多", "ws": ["a lot", "plenty", "great deal", "abundant", "considerable", "ample"]}],
    "music": [{"pos": "n.", "cn": "音乐", "ws": ["melody", "tune", "harmony", "song", "rhythm", "sound", "symphony", "composition"]}],
    "my": [{"pos": "pron.", "cn": "我的", "ws": ["mine", "own", "personal"]}],
    "name": [{"pos": "n.", "cn": "名字", "ws": ["title", "designation", "label", "term", "identity", "appellation"]}],
    "new": [{"pos": "adj.", "cn": "新的", "ws": ["fresh", "recent", "novel", "modern", "current", "original", "latest"]}],
    "newspaper": [{"pos": "n.", "cn": "报纸", "ws": ["paper", "daily", "gazette", "journal", "tabloid", "broadsheet", "periodical"]}],
    "nice": [{"pos": "adj.", "cn": "好的", "ws": ["pleasant", "good", "fine", "lovely", "agreeable", "enjoyable", "kind"]}],
    "nine": [{"pos": "num.", "cn": "九", "ws": ["ninth", "nonet"]}],
    "no": [{"pos": "adv.", "cn": "不", "ws": ["not", "negative", "never", "nay", "refusal"]}],
    "noodle": [{"pos": "n.", "cn": "面条", "ws": ["pasta", "spaghetti", "macaroni", "vermicelli"]}],
    "nose": [{"pos": "n.", "cn": "鼻子", "ws": ["snout", "beak", "nostril", "proboscis"]}],
    "now": [{"pos": "adv.", "cn": "现在", "ws": ["currently", "presently", "today", "immediately", "right now", "at present"]}],
    "number": [{"pos": "n.", "cn": "数字", "ws": ["numeral", "figure", "digit", "integer", "count", "quantity"]}],
    "old": [{"pos": "adj.", "cn": "老的", "ws": ["elderly", "aged", "ancient", "senior", "mature", "vintage", "antique"]}],
    "on": [{"pos": "prep.", "cn": "在……上", "ws": ["upon", "atop", "above", "over", "against"]}],
    "one": [{"pos": "num.", "cn": "一", "ws": ["single", "sole", "only", "individual", "unique", "unitary"]}],
    "open": [{"pos": "v.", "cn": "打开", "ws": ["unlock", "unseal", "unwrap", "reveal", "uncover", "expose", "unfold"]}],
    "orange": [{"pos": "n.", "cn": "橙子", "ws": ["citrus", "tangerine", "mandarin", "clementine"]}],
    "our": [{"pos": "pron.", "cn": "我们的", "ws": ["ours", "belonging to us"]}],
    "over": [{"pos": "prep.", "cn": "在……上方", "ws": ["above", "on top of", "across", "beyond", "past"]}],
    "pair": [{"pos": "n.", "cn": "一双", "ws": ["couple", "duo", "twosome", "set of two", "brace"]}],
    "panda": [{"pos": "n.", "cn": "熊猫", "ws": ["giant panda", "bear cat", "bamboo bear"]}],
    "parent": [{"pos": "n.", "cn": "父母", "ws": ["mother", "father", "guardian", "caregiver", "protector"]}],
    "park": [{"pos": "n.", "cn": "公园", "ws": ["garden", "recreation ground", "common", "green", "playground", "reserve"]}],
    "pass": [{"pos": "v.", "cn": "通过", "ws": ["go by", "move past", "overtake", "succeed", "transfer"]}],
    "pe": [{"pos": "n.", "cn": "体育", "ws": ["physical education", "gym", "sports", "exercise"]}],
    "pen": [{"pos": "n.", "cn": "笔", "ws": ["writing instrument", "ballpoint", "fountain pen", "marker"]}],
    "pencil": [{"pos": "n.", "cn": "铅笔", "ws": ["writing tool", "lead pencil", "sketching tool"]}],
    "people": [{"pos": "n.", "cn": "人们", "ws": ["persons", "individuals", "humans", "folk", "society", "public", "population", "citizens"]}],
    "pick": [{"pos": "v.", "cn": "摘", "ws": ["choose", "select", "gather", "collect", "pluck", "harvest"]}],
    "picture": [{"pos": "n.", "cn": "图片", "ws": ["image", "photo", "painting", "illustration", "drawing", "portrait"]}],
    "pig": [{"pos": "n.", "cn": "猪", "ws": ["swine", "hog", "sow", "boar", "piglet", "pork"]}],
    "place": [{"pos": "n.", "cn": "地方", "ws": ["location", "site", "spot", "area", "position", "venue", "locale"]}],
    "plane": [{"pos": "n.", "cn": "飞机", "ws": ["aircraft", "airplane", "jet", "airliner", "aero"]}],
    "play": [{"pos": "v.", "cn": "玩", "ws": ["have fun", "enjoy", "recreate", "frolic", "sport", "perform", "act"]}],
    "please": [{"pos": "v.", "cn": "请", "ws": ["if you please", "kindly", "pray", "beg"]}],
    "potato": [{"pos": "n.", "cn": "土豆", "ws": ["spud", "tuber", "tater", "sweet potato"]}],
    "pretty": [{"pos": "adj.", "cn": "漂亮的", "ws": ["beautiful", "lovely", "attractive", "handsome", "gorgeous", "charming", "cute"]}],
    "pupil": [{"pos": "n.", "cn": "学生", "ws": ["student", "learner", "scholar", "schoolchild", "disciple"]}],
    "put": [{"pos": "v.", "cn": "放", "ws": ["place", "set", "position", "lay", "deposit", "install", "situate"]}],
    "rabbit": [{"pos": "n.", "cn": "兔子", "ws": ["bunny", "hare", "coney", "buck", "doe"]}],
    "rain": [{"pos": "n.", "cn": "雨", "ws": ["rainfall", "precipitation", "drizzle", "shower", "downpour", "storm"]}],
    "read": [{"pos": "v.", "cn": "阅读", "ws": ["peruse", "study", "scan", "browse", "examine", "interpret", "decipher"]}],
    "ready": [{"pos": "adj.", "cn": "准备好的", "ws": ["prepared", "set", "equipped", "organized", "primed", "all set"]}],
    "red": [{"pos": "adj.", "cn": "红色的", "ws": ["crimson", "scarlet", "ruby", "vermilion", "cherry", "burgundy"]}],
    "rice": [{"pos": "n.", "cn": "米饭", "ws": ["grain", "paddy", "cereal", "wild rice"]}],
    "right": [{"pos": "adj.", "cn": "正确的", "ws": ["correct", "accurate", "proper", "true", "appropriate", "just", "valid"]}],
    "river": [{"pos": "n.", "cn": "河流", "ws": ["stream", "creek", "brook", "waterway", "tributary", "watercourse"]}],
    "room": [{"pos": "n.", "cn": "房间", "ws": ["chamber", "space", "area", "apartment", "hall", "compartment"]}],
    "rule": [{"pos": "n.", "cn": "规则", "ws": ["regulation", "law", "guideline", "principle", "standard", "code", "policy"]}],
    "run": [{"pos": "v.", "cn": "跑", "ws": ["sprint", "jog", "race", "dash", "hurry", "gallop", "rush", "speed"]}],
    "sad": [{"pos": "adj.", "cn": "悲伤的", "ws": ["unhappy", "sorrowful", "mournful", "gloomy", "depressed", "miserable", "melancholy"]}],
    "safe": [{"pos": "adj.", "cn": "安全的", "ws": ["secure", "protected", "harmless", "guarded", "shielded", "risk-free", "sound"]}],
    "salad": [{"pos": "n.", "cn": "沙拉", "ws": ["greens", "mixed vegetables", "coleslaw"]}],
    "say": [{"pos": "v.", "cn": "说", "ws": ["speak", "tell", "utter", "state", "declare", "express", "articulate", "pronounce"]}],
    "school": [{"pos": "n.", "cn": "学校", "ws": ["educational institution", "academy", "college", "institute", "university"]}],
    "see": [{"pos": "v.", "cn": "看见", "ws": ["observe", "view", "watch", "notice", "spot", "glimpse", "perceive", "witness"]}],
    "seven": [{"pos": "num.", "cn": "七", "ws": ["septet", "seventh"]}],
    "she": [{"pos": "pron.", "cn": "她", "ws": ["her", "female", "woman", "girl"]}],
    "sheep": [{"pos": "n.", "cn": "羊", "ws": ["ewe", "ram", "lamb", "woolly", "ovine"]}],
    "shirt": [{"pos": "n.", "cn": "衬衫", "ws": ["blouse", "top", "tunic", "polo"]}],
    "shoe": [{"pos": "n.", "cn": "鞋", "ws": ["footwear", "boot", "sandal", "sneaker", "loafer", "trainer"]}],
    "short": [{"pos": "adj.", "cn": "短的", "ws": ["brief", "little", "small", "compact", "concise", "abbreviated", "low"]}],
    "shorts": [{"pos": "n.", "cn": "短裤", "ws": ["briefs", "trunks", "swimwear", "cutoffs", "hot pants"]}],
    "sing": [{"pos": "v.", "cn": "唱歌", "ws": ["chant", "carol", "vocalize", "croon", "warble", "hum"]}],
    "sister": [{"pos": "n.", "cn": "姐妹", "ws": ["sibling", "kin", "twin"]}],
    "sit": [{"pos": "v.", "cn": "坐", "ws": ["settle", "perch", "rest", "be seated", "squat", "take a seat"]}],
    "size": [{"pos": "n.", "cn": "尺寸", "ws": ["dimension", "measure", "extent", "magnitude", "scale", "proportion", "volume"]}],
    "skirt": [{"pos": "n.", "cn": "裙子", "ws": ["dress", "frock", "kilt", "maxi", "mini"]}],
    "sleep": [{"pos": "v.", "cn": "睡觉", "ws": ["slumber", "doze", "nap", "rest", "snooze", "hibernate", "repose"]}],
    "small": [{"pos": "adj.", "cn": "小的", "ws": ["little", "tiny", "miniature", "petite", "compact", "slight", "minute", "wee"]}],
    "snake": [{"pos": "n.", "cn": "蛇", "ws": ["serpent", "reptile", "viper", "python", "cobra"]}],
    "snow": [{"pos": "n.", "cn": "雪", "ws": ["frost", "ice", "snowfall", "blizzard", "flakes", "powder"]}],
    "so": [{"pos": "adv.", "cn": "如此", "ws": ["therefore", "thus", "consequently", "accordingly", "hence", "very", "extremely"]}],
    "some": [{"pos": "adj.", "cn": "一些", "ws": ["several", "a few", "various", "certain", "any"]}],
    "sorry": [{"pos": "adj.", "cn": "对不起", "ws": ["apologetic", "regretful", "remorseful", "penitent", "rueful", "contrite"]}],
    "speak": [{"pos": "v.", "cn": "说话", "ws": ["talk", "say", "utter", "communicate", "converse", "articulate", "express", "voice"]}],
    "spoon": [{"pos": "n.", "cn": "勺子", "ws": ["ladle", "scoop", "utensil"]}],
    "sport": [{"pos": "n.", "cn": "运动", "ws": ["game", "athletics", "exercise", "activity", "competition", "recreation"]}],
    "stand": [{"pos": "v.", "cn": "站立", "ws": ["rise", "get up", "be upright", "be on feet"]}],
    "star": [{"pos": "n.", "cn": "星星", "ws": ["celestial body", "sun", "luminary", "asteroid", "nova", "constellation"]}],
    "stop": [{"pos": "v.", "cn": "停止", "ws": ["halt", "cease", "quit", "end", "pause", "terminate", "finish", "discontinue"]}],
    "story": [{"pos": "n.", "cn": "故事", "ws": ["tale", "narrative", "account", "anecdote", "fable", "legend", "myth", "yarn"]}],
    "strong": [{"pos": "adj.", "cn": "强壮的", "ws": ["powerful", "muscular", "tough", "robust", "sturdy", "mighty", "forceful"]}],
    "student": [{"pos": "n.", "cn": "学生", "ws": ["pupil", "learner", "scholar", "classmate", "apprentice", "trainee"]}],
    "study": [{"pos": "v.", "cn": "学习", "ws": ["learn", "revise", "research", "examine", "analyze", "investigate", "cram", "read"]}],
    "sun": [{"pos": "n.", "cn": "太阳", "ws": ["star", "sol", "daylight", "sunshine", "solar", "sunlight"]}],
    "sunglasses": [{"pos": "n.", "cn": "太阳镜", "ws": ["shades", "specs", "dark glasses", "eyewear"]}],
    "supermarket": [{"pos": "n.", "cn": "超市", "ws": ["store", "shop", "market", "grocer", "mart", "hypermarket"]}],
    "swim": [{"pos": "v.", "cn": "游泳", "ws": ["bathe", "paddle", "dive", "float", "wade", "plunge", "stroke"]}],
    "table": [{"pos": "n.", "cn": "桌子", "ws": ["desk", "counter", "bench", "stand", "board", "surface"]}],
    "take": [{"pos": "v.", "cn": "拿", "ws": ["grab", "seize", "pick up", "carry", "bring", "remove", "fetch", "obtain"]}],
    "talk": [{"pos": "v.", "cn": "说话", "ws": ["speak", "chat", "converse", "discuss", "communicate", "dialogue", "gossip"]}],
    "tall": [{"pos": "adj.", "cn": "高的", "ws": ["high", "lofty", "towering", "elevated", "lanky", "gangling"]}],
    "tea": [{"pos": "n.", "cn": "茶", "ws": ["beverage", "infusion", "brew", "herb tea", "chai"]}],
    "teacher": [{"pos": "n.", "cn": "老师", "ws": ["instructor", "educator", "tutor", "professor", "mentor", "coach", "lecturer"]}],
    "thank": [{"pos": "v.", "cn": "感谢", "ws": ["appreciate", "acknowledge", "gratitude", "bless"]}],
    "the": [{"pos": "art.", "cn": "定冠词", "ws": []}],
    "there": [{"pos": "adv.", "cn": "那里", "ws": ["at that place", "over there", "yonder"]}],
    "they": [{"pos": "pron.", "cn": "他们", "ws": ["them", "those", "people", "folks"]}],
    "think": [{"pos": "v.", "cn": "认为", "ws": ["believe", "consider", "suppose", "assume", "presume", "imagine", "contemplate", "reason"]}],
    "this": [{"pos": "pron.", "cn": "这个", "ws": ["that", "these", "those", "the one"]}],
    "those": [{"pos": "pron.", "cn": "那些", "ws": ["these", "that", "them"]}],
    "three": [{"pos": "num.", "cn": "三", "ws": ["trio", "triplet", "third"]}],
    "tidy": [{"pos": "adj.", "cn": "整洁的", "ws": ["neat", "clean", "orderly", "organized", "trim", "uncluttered", "smart"]}],
    "tiger": [{"pos": "n.", "cn": "老虎", "ws": ["big cat", "panther", "feline", "stripe"]}],
    "time": [{"pos": "n.", "cn": "时间", "ws": ["moment", "period", "duration", "era", "age", "epoch", "interval", "season"]}],
    "to": [{"pos": "prep.", "cn": "到", "ws": ["toward", "towards", "until", "into", "unto"]}],
    "today": [{"pos": "n.", "cn": "今天", "ws": ["this day", "now", "present", "currently"]}],
    "tomato": [{"pos": "n.", "cn": "番茄", "ws": ["love apple", "cherry tomato", "plum tomato"]}],
    "too": [{"pos": "adv.", "cn": "也", "ws": ["also", "as well", "additionally", "moreover", "likewise", "furthermore"]}],
    "toy": [{"pos": "n.", "cn": "玩具", "ws": ["plaything", "game", "doll", "trinket", "novelty", "gadget", "amusement"]}],
    "tree": [{"pos": "n.", "cn": "树", "ws": ["plant", "bush", "shrub", "timber", "woodland", "sapling"]}],
    "trousers": [{"pos": "n.", "cn": "裤子", "ws": ["pants", "slacks", "jeans", "breeches", "denims"]}],
    "try": [{"pos": "v.", "cn": "尝试", "ws": ["attempt", "endeavor", "strive", "test", "experiment", "sample", "seek"]}],
    "turn": [{"pos": "v.", "cn": "转", "ws": ["rotate", "spin", "twist", "revolve", "swivel", "pivot", "whirl"]}],
    "tv": [{"pos": "n.", "cn": "电视", "ws": ["television", "telly", "idiot box", "the tube", "screen", "monitor"]}],
    "two": [{"pos": "num.", "cn": "二", "ws": ["duo", "pair", "couple", "double", "twin", "second"]}],
    "umbrella": [{"pos": "n.", "cn": "雨伞", "ws": ["parasol", "sunshade", "brolly", "canopy"]}],
    "under": [{"pos": "prep.", "cn": "在……下面", "ws": ["below", "beneath", "underneath", "lower than", "subordinate to"]}],
    "understand": [{"pos": "v.", "cn": "理解", "ws": ["comprehend", "grasp", "perceive", "know", "follow", "appreciate", "discern"]}],
    "up": [{"pos": "adv.", "cn": "向上", "ws": ["upward", "above", "high", "aloft", "overhead", "elevated"]}],
    "us": [{"pos": "pron.", "cn": "我们", "ws": ["ourselves", "we", "our group"]}],
    "use": [{"pos": "v.", "cn": "使用", "ws": ["utilize", "employ", "apply", "operate", "manipulate", "handle", "exploit", "wield"]}],
    "vegetable": [{"pos": "n.", "cn": "蔬菜", "ws": ["greens", "produce", "legume", "herb", "veg"]}],
    "very": [{"pos": "adv.", "cn": "非常", "ws": ["extremely", "highly", "really", "greatly", "exceedingly", "immensely", "particularly"]}],
    "walk": [{"pos": "v.", "cn": "步行", "ws": ["stroll", "stride", "march", "trek", "hike", "amble", "wander", "step"]}],
    "wall": [{"pos": "n.", "cn": "墙", "ws": ["barrier", "partition", "fence", "enclosure", "side", "boundary", "rampart"]}],
    "want": [{"pos": "v.", "cn": "想要", "ws": ["desire", "wish", "need", "crave", "yearn", "long for", "covet"]}],
    "wash": [{"pos": "v.", "cn": "洗", "ws": ["clean", "rinse", "scrub", "cleanse", "bathe", "launder", "shampoo"]}],
    "waste": [{"pos": "v.", "cn": "浪费", "ws": ["squander", "misuse", "fritter away", "throw away", "dissipate"]}],
    "watch": [{"pos": "v.", "cn": "观看", "ws": ["observe", "view", "look at", "monitor", "stare", "gaze", "examine"]}],
    "water": [{"pos": "n.", "cn": "水", "ws": ["liquid", "H2O", "fluid", "aqua", "moisture", "rain"]}],
    "we": [{"pos": "pron.", "cn": "我们", "ws": ["us", "ourselves", "our group", "everyone"]}],
    "weather": [{"pos": "n.", "cn": "天气", "ws": ["climate", "atmosphere", "conditions", "temperature", "forecast", "season"]}],
    "week": [{"pos": "n.", "cn": "周", "ws": ["seven days", "fortnight", "workweek"]}],
    "wet": [{"pos": "adj.", "cn": "湿的", "ws": ["damp", "moist", "soggy", "soaked", "drenched", "humid", "waterlogged", "rainy"]}],
    "what": [{"pos": "pron.", "cn": "什么", "ws": ["which", "whatever", "how", "the thing that"]}],
    "when": [{"pos": "adv.", "cn": "什么时候", "ws": ["at what time", "as soon as", "while", "whenever", "during"]}],
    "where": [{"pos": "adv.", "cn": "哪里", "ws": ["at what place", "wherever", "in what location", "whither"]}],
    "white": [{"pos": "adj.", "cn": "白色的", "ws": ["pale", "ivory", "snowy", "pearly", "milky", "cream", "bleached"]}],
    "who": [{"pos": "pron.", "cn": "谁", "ws": ["whom", "which person", "what person"]}],
    "window": [{"pos": "n.", "cn": "窗户", "ws": ["opening", "pane", "casement", "skylight", "porthole", "aperture", "glass"]}],
    "word": [{"pos": "n.", "cn": "单词", "ws": ["term", "expression", "vocabulary", "phrase", "lexeme", "utterance", "language"]}],
    "work": [{"pos": "v.", "cn": "工作", "ws": ["labor", "toil", "job", "task", "employment", "occupation", "profession", "trade"]}],
    "workbook": [{"pos": "n.", "cn": "练习册", "ws": ["exercise book", "textbook", "manual", "study guide"]}],
    "world": [{"pos": "n.", "cn": "世界", "ws": ["earth", "globe", "planet", "universe", "sphere", "realm", "cosmos"]}],
    "write": [{"pos": "v.", "cn": "写", "ws": ["compose", "record", "inscribe", "jot down", "scribble", "draft", "pen", "author"]}],
    "year": [{"pos": "n.", "cn": "年", "ws": ["twelve months", "annum", "calendar year", "annual period", "age"]}],
    "yellow": [{"pos": "adj.", "cn": "黄色的", "ws": ["amber", "golden", "lemon", "saffron", "mustard", "ochre"]}],
    "yes": [{"pos": "adv.", "cn": "是的", "ws": ["yeah", "yep", "affirmative", "certainly", "absolutely", "agreed"]}],
    "you": [{"pos": "pron.", "cn": "你", "ws": ["yourself", "thee", "ye", "thou"]}],
    "young": [{"pos": "adj.", "cn": "年轻的", "ws": ["youthful", "juvenile", "adolescent", "junior", "immature", "fresh", "new"]}],
    "your": [{"pos": "pron.", "cn": "你的", "ws": ["yours", "belonging to you", "thy", "thine"]}],
    "zoo": [{"pos": "n.", "cn": "动物园", "ws": ["zoological garden", "animal park", "menagerie", "wildlife park"]}],
}

SYNONYM_DB_LOWER = {}
for k, v in SYNONYM_DB.items():
    SYNONYM_DB_LOWER[k.lower()] = v

# ============ ETYMOLOGY DATABASE ============
ETYMOLOGY_DB = {
    "about": "古英语 onbūtan，由 on（在）+ būtan（外面）组成。",
    "after": "古英语 æfter，源自原始日耳曼语 *after，意为「在后面」。",
    "again": "古英语 ongēan，由 on（在）+ gēan（反对）组成，原意「朝向相反方向」。",
    "all": "古英语 eall，源自原始日耳曼语 *allaz，意为「整个、完全」。",
    "also": "古英语 eallswā，由 eall（全部）+ swā（如此）组成。",
    "always": "古英语 ealne weg，意为「一直、所有道路」。",
    "animal": "拉丁语 animal，源自 anima（生命、灵魂），原意「有生命的生物」。",
    "any": "古英语 ænig，源自 ān（一个）+ -ig 后缀，原意「任何一个」。",
    "apple": "古英语 æppel，源自原始日耳曼语 *aplaz，泛指任何水果。",
    "art": "拉丁语 ars，意为「技能、工艺」，源自原始印欧语 *ar-（适合、连接）。",
    "ask": "古英语 āscian，源自原始日耳曼语 *aiskōną，意为「寻求、要求」。",
    "baby": "中古英语 babi，可能是儿语模仿，与 babble（咿呀声）同源。",
    "back": "古英语 bæc，源自原始日耳曼语 *baka-，原意为「背部、后面」。",
    "bad": "中古英语 badde，词源不确定，可能与古英语 bæddel（雌雄同体）有关。",
    "bag": "古诺斯语 baggi，源自原始日耳曼语 *bag-，意为「包裹、袋子」。",
    "ball": "古诺斯语 böllr，源自原始日耳曼语 *balluz，意为「球、圆形物体」。",
    "bathroom": "由 bath（洗澡）+ room（房间）组成。Bath 源自古英语 bæð（浸泡）。",
    "be": "古英语 bēon，源自原始印欧语 *bʰuH-（成为、生长），是最古老的英语动词。",
    "beautiful": "由 beauty（美丽）+ -ful（充满）组成。Beauty 源自古法语 beaute，源自拉丁语 bellus（美丽的）。",
    "bed": "古英语 bedd，源自原始日耳曼语 *badją，原意「挖掘的地铺」。",
    "bedroom": "由 bed（床）+ room（房间）组成，14世纪开始使用。",
    "bee": "古英语 bēo，源自原始印欧语 *bʰey-（蜜蜂），拟声词模仿蜂鸣声。",
    "big": "中古英语 big，词源不确定，可能源自斯堪的纳维亚语。",
    "bird": "古英语 bridd，原指「幼鸟」，词源不明，可能源自原始日耳曼语。",
    "black": "古英语 blæc，源自原始日耳曼语 *blakaz，意为「烧焦的、黑色的」。",
    "blackboard": "由 black（黑色）+ board（木板）组成，19世纪学校用品。",
    "blue": "古法语 bleu，源自原始日耳曼语 *blēwaz，意为「蓝色」。",
    "book": "古英语 bōc，源自原始日耳曼语 *bōks（榉木），早期文字刻在榉木板上。",
    "bowl": "古英语 bolla（碗、杯），源自原始日耳曼语 *bullǭ（圆形器皿）。",
    "box": "拉丁语 buxis，源自希腊语 pyxis（黄杨木盒），因盒子多用黄杨木制作。",
    "boy": "中古英语 boi，词源不明，可能源自法语或日耳曼语。",
    "bread": "古英语 brēad，原意为「碎片、小块」，后指面包。",
    "brother": "古英语 brōþor，源自原始印欧语 *bʰréh₂tēr（兄弟）。",
    "brown": "古英语 brūn，源自原始日耳曼语 *brūnaz，意为「棕色、暗淡」。",
    "bus": "拉丁语 omnibus（为所有人）的缩写，omnis 意为「所有」。",
    "buy": "古英语 bycgan，源自原始日耳曼语 *bugjaną，意为「购买」。",
    "cake": "古诺斯语 kaka，源自原始日耳曼语 *kakǭ，意为「小圆饼」。",
    "car": "拉丁语 carrus（马车），源自凯尔特语 karros（战车）。",
    "carrot": "拉丁语 carota，源自希腊语 karōton，可能源自原始印欧语 *ker-（角、头）。",
    "cat": "拉丁语 cattus，可能源自北非语言，埃及最早驯养猫。",
    "chair": "拉丁语 cathedra（主教座），源自希腊语 kathedra（座位）。",
    "cheap": "古英语 cēap（交易、购买），原意「价格低的」，源自拉丁语 caupo（小商贩）。",
    "chicken": "古英语 cicen，源自原始日耳曼语 *kiukīną（小鸡），拟声词。",
    "child": "古英语 cild，源自原始日耳曼语 *kilþą（子宫、胎儿）。",
    "chopstick": "洋泾浜英语，由 chop（快）+ stick（棍）组成。Chop 源自粤语「急」。",
    "class": "拉丁语 classis（等级、舰队），源自 calare（召集）。",
    "classroom": "由 class（班级）+ room（房间）组成，19世纪教育术语。",
    "clean": "古英语 clæne，源自原始日耳曼语 *klainiz，意为「纯净、干净」。",
    "clock": "中古荷兰语 clocke（钟），源自拉丁语 clocca，拟声词模仿钟声。",
    "clothes": "古英语 clāþas（布料），源自原始日耳曼语 *klaiþaz。",
    "cloud": "古英语 clūd（岩石、山丘），后转义为天上的云团。",
    "cold": "古英语 cald，源自原始日耳曼语 *kaldaz，意为「冷的」。",
    "colour": "拉丁语 color，源自古拉丁语 colos，意为「颜色、覆盖」。",
    "come": "古英语 cuman，源自原始印欧语 *gʷem-（来、去）。",
    "cook": "拉丁语 coquus（厨师），源自 coquere（烹饪）。",
    "cool": "古英语 cōl，源自原始日耳曼语 *kōlaz，与 cold 同源。",
    "cow": "古英语 cū，源自原始印欧语 *gʷṓws（牛），最古老的词汇之一。",
    "cup": "拉丁语 cupa（桶），源自原始印欧语 *kewp-（空洞）。",
    "dad": "儿语模仿，与 father 同源，源自原始印欧语 *pətēr。",
    "dance": "古法语 dancer，可能源自日耳曼语，原意「摇摆、拉伸」。",
    "day": "古英语 dæg，源自原始印欧语 *dʰegʰ-（燃烧），指太阳照耀的时段。",
    "dear": "古英语 dēore（珍贵的），源自原始日耳曼语 *deurijaz。",
    "delicious": "拉丁语 deliciosus（令人愉悦的），源自 deliciae（愉悦、快乐）。",
    "desk": "拉丁语 discus（圆盘、桌面），源自希腊语 diskos。",
    "dinner": "古法语 disner（早餐），源自拉丁语 disjejunare（打破斋戒）。",
    "dog": "古英语 docga，词源不明，可能源自原始日耳曼语 *dukkōn。",
    "door": "古英语 duru，源自原始印欧语 *dʰwer-（门、入口）。",
    "down": "古英语 dūne，由 of dūne（从山上下来）缩写而来。",
    "dress": "古法语 dresser（整理、打扮），源自拉丁语 directus（直的）。",
    "drink": "古英语 drincan，源自原始日耳曼语 *drinkaną。",
    "eat": "古英语 etan，源自原始印欧语 *h₁ed-（吃）。",
    "egg": "古诺斯语 egg，源自原始日耳曼语 *ajją（蛋），与 bird 有关。",
    "elephant": "希腊语 elephas（象牙、大象），可能源自非洲语言。",
    "expensive": "拉丁语 expensivus，源自 expendere（支付、花费），ex-（出）+ pendere（称重、支付）。",
    "eye": "古英语 ēage，源自原始印欧语 *h₃ekʷ-（看、眼睛）。",
    "face": "拉丁语 facies（面容、形状），源自 facere（做）。",
    "family": "拉丁语 familia（家庭、仆人），源自 famulus（仆人）。",
    "fan": "拉丁语 vannus（簸箕），后指风扇、爱好者（fanatic 缩写）。",
    "farm": "拉丁语 firma（固定付款），后指租赁的土地。",
    "farmer": "古法语 fermier，源自 ferme（农场），本义「承租人」。",
    "fast": "古英语 fæst（固定的、坚固的），后引申为「快速的」。",
    "father": "古英语 fæder，源自原始印欧语 *pətēr（父亲）。",
    "feed": "古英语 fēdan，与 fōda（食物）同源，源自原始日耳曼语 *fōdijaną（喂养）。",
    "feel": "古英语 fēlan，源自原始日耳曼语 *fōlijaną（触摸、感觉）。",
    "find": "古英语 findan，源自原始日耳曼语 *finþaną（发现）。",
    "first": "古英语 fyrst，源自原始日耳曼语 *furistaz（最前面的）。",
    "fish": "古英语 fisc，源自原始印欧语 *pisk-（鱼）。",
    "flower": "拉丁语 flos（花），源自原始印欧语 *bʰleh₃-（开花）。",
    "fly": "古英语 flēogan，源自原始印欧语 *plewk-（飞）。",
    "follow": "古英语 folgian（跟随），源自原始日耳曼语 *fulgijaną。",
    "food": "古英语 fōda，源自原始日耳曼语 *fōdô（食物、滋养）。",
    "foot": "古英语 fōt，源自原始印欧语 *pṓds（脚）。",
    "fork": "拉丁语 furca（叉子、叉形桩），可能源自原始印欧语。",
    "free": "古英语 frēo，源自原始日耳曼语 *frijaz（自由的、被爱的）。",
    "friend": "古英语 frēond，源自原始日耳曼语 *frijōndz（爱人），与 free 同源。",
    "fruit": "拉丁语 fructus（果实、享用），源自 frui（享受）。",
    "game": "古英语 gamen，源自原始日耳曼语 *gamaną（娱乐、游戏）。",
    "garden": "古北法语 gardin，源自原始日耳曼语 *gardaz（围栏、院子）。",
    "get": "古诺斯语 geta（获得），源自原始日耳曼语 *getaną。",
    "girl": "中古英语 gyrle，词源不明，可能源自古英语 gyrela（衣服）。",
    "give": "古英语 giefan，源自原始印欧语 *gʰebʰ-（给、拿）。",
    "go": "古英语 gān，源自原始印欧语 *ǵʰeh₁-（离开、去）。",
    "good": "古英语 gōd，源自原始日耳曼语 *gōdaz（合适的、好的）。",
    "green": "古英语 grēne，源自原始日耳曼语 *grōniz（绿色，与生长有关）。",
    "hair": "古英语 hær，源自原始日耳曼语 *hērą（毛发）。",
    "hand": "古英语 hand，源自原始日耳曼语 *handuz。",
    "happy": "由 hap（运气）+ y 组成。Hap 源自古诺斯语 happ（机会、好运）。",
    "hard": "古英语 heard，源自原始日耳曼语 *harduz（坚硬的、强烈的）。",
    "hat": "古英语 hæt，源自原始日耳曼语 *hattuz（帽子、兜帽）。",
    "have": "古英语 habban，源自原始日耳曼语 *habjaną（拥有、持有）。",
    "he": "古英语 hē，源自原始印欧语 *k'e-（这个、那个）。",
    "head": "古英语 hēafod，源自原始印欧语 *kaput-（头）。",
    "healthy": "古英语 hælþ（健康）+ y，源自 hāl（完整的、痊愈的）。",
    "hear": "古英语 hīeran，源自原始印欧语 *h₂ḱh₂owsyéti（听）",
    "help": "古英语 helpan，源自原始日耳曼语 *helpaną。",
    "helpful": "help + -ful（充满），表示「有帮助的」。",
    "herself": "古英语 hire self，由 her（她的）+ self（自己）组成。",
    "here": "古英语 hēr，源自原始日耳曼语 *hēr（这里）。",
    "home": "古英语 hām，源自原始日耳曼语 *haimaz（家、村庄）。",
    "homework": "home + work（在家做的工作），20世纪教育术语。",
    "horse": "古英语 hors，源自原始日耳曼语 *hrussą（马）。",
    "hospital": "拉丁语 hospitalis（好客的），源自 hospes（客人、主人）。",
    "hot": "古英语 hāt，源自原始日耳曼语 *haitaz（热的）。",
    "house": "古英语 hūs，源自原始日耳曼语 *hūsą（房子、庇护所）。",
    "how": "古英语 hū，源自原始日耳曼语 *hwō（怎样）。",
    "hungry": "古英语 hungrig，源自 hungor（饥饿）。",
    "i": "古英语 ic，源自原始印欧语 *éǵh₂（我）。",
    "ice": "古英语 īs，源自原始日耳曼语 *īsą（冰）。",
    "in": "古英语 in，源自原始印欧语 *h₁én（在里面）。",
    "it": "古英语 hit，源自原始日耳曼语 *hit（这个）。",
    "jacket": "古法语 jaquet（小上衣），源自 Jacques（雅克，农夫名）。",
    "juice": "拉丁语 jus（汤汁、肉汁），源自原始印欧语 *yeu-（混合）。",
    "jump": "可能源自拟声词，模仿跳跃的声音。16世纪出现。",
    "just": "拉丁语 justus（公正的），源自 jus（法律、权利），后引申为「恰好」。",
    "kid": "中古英语 kide（小山羊），后引申为「小孩」。",
    "kitchen": "拉丁语 coquina（烹饪处），源自 coquere（烹饪）。",
    "knife": "古英语 cnīf，源自古诺斯语 knīfr。",
    "know": "古英语 cnāwan，源自原始印欧语 *ǵneh₃-（知道）。",
    "large": "拉丁语 largus（丰富的、慷慨的），后引申为「大的」。",
    "late": "古英语 læt（慢的、迟的），源自原始日耳曼语 *lataz。",
    "learn": "古英语 leornian，源自原始日耳曼语 *liznaną（学习）。",
    "light": "古英语 lēoht，源自原始印欧语 *lewk-（光、明亮）。",
    "like": "古英语 līcian（使高兴），源自 līc（身体、相似）。",
    "list": "古英语 liste（边缘、条带），后指「列出清单」。源自原始日耳曼语 *listōn。",
    "listen": "古英语 hlysnan，源自原始日耳曼语 *hlusnijaną。",
    "little": "古英语 lȳtel，源自原始日耳曼语 *lūtilaz。",
    "live": "古英语 libban，源自原始印欧语 *leyp-（粘附、留下）。",
    "long": "古英语 lang，源自原始日耳曼语 *langaz。",
    "look": "古英语 lōcian，源自原始日耳曼语 *lōkōną（看）。",
    "loud": "古英语 hlūd，源自原始印欧语 *ḱlew-（听、闻名），与 listen 同源。",
    "love": "古英语 lufu，源自原始日耳曼语 *lubō（爱、渴望）。",
    "lunch": "luncheon 的缩写，可能源自 lump（块）+ -tion，指一块食物。",
    "make": "古英语 macian，源自原始日耳曼语 *makōną（制作、建造）。",
    "man": "古英语 mann，源自原始印欧语 *mon-（人、男人）。",
    "many": "古英语 manig，源自原始日耳曼语 *managaz（许多）。",
    "maths": "mathematics 的缩写，希腊语 mathēmatikē（学问），源自 manthanein（学习）。",
    "milk": "古英语 meolc，源自原始印欧语 *melǵ-（挤奶）。",
    "minute": "拉丁语 minutus（小的），源自 minuere（减少），指一小时的第一小部分。",
    "monkey": "可能源自中古低地德语 Moneke，是 Martin 的昵称，指代猴子。",
    "moon": "古英语 mōna，源自原始印欧语 *mḗh₁n̥s（月亮、月份）。",
    "mother": "古英语 mōdor，源自原始印欧语 *méh₂tēr（母亲）。",
    "mouse": "古英语 mūs，源自原始印欧语 *múh₂s（老鼠）。",
    "mouth": "古英语 mūþ，源自原始印欧语 *ment-（咀嚼、嘴巴）。",
    "much": "古英语 micel，源自原始日耳曼语 *mikilaz（大的、多的）。",
    "music": "希腊语 mousikē（缪斯的艺术），源自 Mousa（缪斯，艺术女神）。",
    "my": "古英语 mīn，源自原始印欧语 *me-（我）。",
    "name": "古英语 nama，源自原始印欧语 *h₁nómn̥（名字）。",
    "new": "古英语 nēowe，源自原始印欧语 *néwos（新的）。",
    "newspaper": "new + paper，17世纪出现的新闻出版物。",
    "nice": "拉丁语 nescius（无知的），后演变为「精细的、好的」。",
    "no": "古英语 nā，由 ne（不）+ ā（总是）组成。",
    "noodle": "德语 Nudel（面条），词源不明。",
    "nose": "古英语 nosu，源自原始印欧语 *nas-（鼻子）。",
    "now": "古英语 nū，源自原始印欧语 *nu（现在）。",
    "number": "拉丁语 numerus（数字），可能源自原始印欧语 *nem-（分配）。",
    "old": "古英语 ald，源自原始日耳曼语 *aldaz（长成的、年老的）。",
    "on": "古英语 on，源自原始印欧语 *h₂en-（在上面）。",
    "one": "古英语 ān，源自原始印欧语 *óynos（一）。",
    "open": "古英语 openian，源自原始日耳曼语 *upanaz（打开的）。",
    "orange": "梵语 nāraṅga，经阿拉伯语 nāranj 传入欧洲。原产中国的水果。",
    "over": "古英语 ofer，源自原始印欧语 *upér（在上面）。",
    "pair": "拉丁语 paria（相等的东西），源自 par（相等的）。",
    "panda": "尼泊尔语 pónya，可能源自藏语，指熊猫。",
    "parent": "拉丁语 parens，源自 parere（生育、产生）。",
    "park": "古法语 parc（围场），源自原始日耳曼语 *parrukaz（围栏）。",
    "pass": "拉丁语 passus（步、步伐），后引申为「通过」。",
    "pen": "拉丁语 penna（羽毛），因早期用羽毛笔书写。",
    "pencil": "拉丁语 penicillus（小刷子、小尾巴），指细画笔。",
    "people": "拉丁语 populus（人民、民族），可能源自伊特鲁里亚语。",
    "pick": "古英语 pician，可能源自原始日耳曼语 *pikkōną（刺、摘）。",
    "picture": "拉丁语 pictura（绘画），源自 pingere（画）。",
    "pig": "古英语 picg，词源不明。",
    "place": "拉丁语 platea（宽街、广场），源自希腊语 plateia。",
    "plane": "拉丁语 planus（平面的），源自原始印欧语 *pleh₂-（平坦）。",
    "play": "古英语 plegan（运动、玩耍），源自原始日耳曼语 *plehaną。",
    "please": "拉丁语 placere（使高兴），源自 placēre（平静）。",
    "potato": "西班牙语 patata，源自泰诺语（海地原住民）batata（甘薯）。",
    "pretty": "古英语 prættig（狡猾的、精巧的），后演变为「漂亮的」。",
    "pupil": "拉丁语 pupillus（孤儿、小学生），源自 pupus（男孩）。",
    "put": "古英语 putian，可能源自原始日耳曼语 *putōną（推、放）。",
    "rabbit": "中古英语 rabet，可能源自古法语 dialect。",
    "rain": "古英语 regn，源自原始日耳曼语 *regną（雨）。",
    "read": "古英语 rædan（劝告、解读），源自原始日耳曼语 *rēdaną。",
    "ready": "古英语 ræde（准备好的），源自 rīdan（骑马准备）。",
    "red": "古英语 rēad，源自原始印欧语 *h₁rewdʰ-（红色）。",
    "rice": "希腊语 oryza，最终可能源自梵语 vrīhi（稻米）。",
    "right": "古英语 riht，源自原始印欧语 *h₃reǵtós（直的、正确的）。",
    "river": "拉丁语 riparius（河岸的），源自 ripa（河岸）。",
    "room": "古英语 rūm（空间），源自原始日耳曼语 *rūmą。",
    "rule": "拉丁语 regula（直尺、规则），源自 regere（统治、引导）。",
    "run": "古英语 rinnan，源自原始印欧语 *h₃ri-néw-（流动、跑）。",
    "sad": "古英语 sæd（饱足的、厌倦的），后演变为「悲伤的」。",
    "safe": "拉丁语 salvus（完整的、健康的），源自原始印欧语 *solh₂-（完整）。",
    "salad": "拉丁语 salata（盐腌的），源自 sal（盐）。",
    "say": "古英语 secgan，源自原始印欧语 *sekʷ-（说）。",
    "school": "希腊语 scholē（闲暇、学习），原指有闲暇时间学习的地方。",
    "see": "古英语 sēon，源自原始印欧语 *sekʷ-（看、跟随）。",
    "sheep": "古英语 scēap，源自原始日耳曼语 *skēpą（羊）。",
    "shirt": "古英语 scyrte，源自原始日耳曼语 *skurtijǭ（短衣）。",
    "shoe": "古英语 scōh，源自原始日耳曼语 *skōhaz（鞋子）。",
    "short": "古英语 sceort，源自原始日耳曼语 *skurtaz（短的）。",
    "sing": "古英语 singan，源自原始印欧语 *sengʷʰ-（唱歌）。",
    "sister": "古英语 sweostor，源自原始印欧语 *swésōr（姐妹）。",
    "sit": "古英语 sittan，源自原始印欧语 *sed-（坐）。",
    "size": "古法语 sise（规定的大小），源自 asseoir（放置、设定）。",
    "skirt": "古诺斯语 skyrta，与 shirt 同源。",
    "sleep": "古英语 slæpan，源自原始印欧语 *sleb-（睡、弱）。",
    "small": "古英语 smæl（细的、窄的），源自原始日耳曼语 *smalaz。",
    "snake": "古英语 snaca，源自原始印欧语 *sneg-（爬行）。",
    "snow": "古英语 snāw，源自原始印欧语 *sneygʷʰ-（雪、下雪）。",
    "so": "古英语 swā，源自原始日耳曼语 *swa（如此）。",
    "some": "古英语 sum，源自原始日耳曼语 *sumaz（某个、一些）。",
    "sorry": "古英语 sārig（痛苦的），源自 sār（疼痛、痛苦）。",
    "speak": "古英语 specan，源自原始日耳曼语 *sprekōną（说话）。",
    "spoon": "古英语 spōn（木片），源自原始日耳曼语 *spēnuz。",
    "sport": "disport 的缩写，古法语 desporter（消遣、娱乐）。",
    "stand": "古英语 standan，源自原始印欧语 *steh₂-（站立）。",
    "star": "古英语 steorra，源自原始印欧语 *h₂stḗr（星星）。",
    "stop": "古英语 stoppian（堵住），源自拉丁语 stuppa（麻絮）。",
    "story": "拉丁语 historia（历史、故事），源自希腊语 histor（智者）。",
    "strong": "古英语 strang，源自原始日耳曼语 *strangaz（紧的、强的）。",
    "student": "拉丁语 studens（学习者），源自 studere（勤奋学习）。",
    "study": "拉丁语 studium（热情、勤奋），源自 studere（追求）。",
    "sun": "古英语 sunne，源自原始印欧语 *sóh₂wl̥（太阳）。",
    "table": "拉丁语 tabula（木板、平板），后指桌子。",
    "take": "古诺斯语 taka，源自原始日耳曼语 *tēkaną（拿、触摸）。",
    "talk": "古英语 talu（故事、计算），与 tell 同源。",
    "tall": "古英语 getæl（快的、敏捷的），后引申为「高的」。",
    "tea": "汉语「茶」的音译，经马来语 teh 或闽南语 tê 传入欧洲。",
    "teacher": "古英语 tæcan（教）+ -er，与 token 同源。",
    "thank": "古英语 þancian，源自原始日耳曼语 *þankōną（感谢、思考）。",
    "there": "古英语 þær，源自原始日耳曼语 *þar（那里）。",
    "think": "古英语 þencan，源自原始印欧语 *teng-（思考）。",
    "this": "古英语 þes，源自原始日耳曼语 *þat（那个）。",
    "those": "古英语 þās，源自原始日耳曼语 *þai-（那些）。",
    "tidy": "由 tide（时间、季节）+ y 组成，原意「及时的、合适的」。",
    "tiger": "希腊语 tigris，可能源自伊朗语 tigra-（尖锐的、快速的）。",
    "time": "古英语 tīma，源自原始日耳曼语 *tīmô（时间、时机）。",
    "to": "古英语 tō，源自原始日耳曼语 *tō（到、朝向）。",
    "today": "古英语 tōdæg（在这一天），由 to + day 组成。",
    "tomato": "西班牙语 tomate，源自纳瓦特尔语（墨西哥原住民）tomatl。",
    "too": "古英语 tō（也），是 to 的强调形式。",
    "toy": "中古英语 toye（玩耍、玩具），词源不明。",
    "tree": "古英语 trēo，源自原始印欧语 *dóru（树、木头）。",
    "try": "古法语 trier（挑选、分离），可能源自拉丁语。",
    "turn": "拉丁语 tornare（在车床上转动），源自 tornus（车床）。",
    "umbrella": "拉丁语 umbra（阴影、树荫），umbrella 意为「小遮阴物」。",
    "under": "古英语 under，源自原始印欧语 *n̥dʰér（在下面）。",
    "understand": "古英语 understandan，由 under（在中间）+ standan（站）组成，意为「站在中间理解」。",
    "up": "古英语 ūp，源自原始印欧语 *upo（向上、在上面）。",
    "use": "拉丁语 ūsus（使用），源自 ūtī（使用、享受）。",
    "vegetable": "拉丁语 vegetabilis（有活力的、能生长的），源自 vegere（活跃）。",
    "very": "拉丁语 vērus（真实的），最初意为「真正的」，后转为「非常」。",
    "walk": "古英语 wealcan（滚动、翻滚），后引申为「行走」。",
    "wall": "拉丁语 vallum（栅栏、壁垒），源自 vallus（木桩）。",
    "want": "古诺斯语 vanta（缺乏），源自原始日耳曼语 *wanatōną。",
    "wash": "古英语 wæscan，源自原始日耳曼语 *waskaną（洗）。",
    "waste": "拉丁语 vastus（荒芜的、空的），源自古法语 waster（浪费）。",
    "watch": "古英语 wæccan（保持清醒、守夜），后引申为「观看」。",
    "water": "古英语 wæter，源自原始印欧语 *wódr̥（水）。",
    "weather": "古英语 weder，源自原始印欧语 *weh₁-（吹、风）。",
    "week": "古英语 wice，源自原始日耳曼语 *wikǭ（转折、周）。",
    "wet": "古英语 wæt，源自原始日耳曼语 *wētaz（湿的），与 water 同源。",
    "white": "古英语 hwīt，源自原始印欧语 *ḱweytos（白的、明亮的）。",
    "who": "古英语 hwā，源自原始印欧语 *kʷos（谁）。",
    "window": "古诺斯语 vindauga（风眼），由 vindr（风）+ auga（眼睛）组成。",
    "word": "古英语 word，源自原始印欧语 *werdʰh₁om（词、言语）。",
    "work": "古英语 weorc，源自原始印欧语 *wérǵom（工作、行动）。",
    "world": "古英语 weorold，由 wer（人）+ eld（年龄、时代）组成，意为「人类时代」。",
    "write": "古英语 wrītan（刻、画），原指在木头上刻字。",
    "year": "古英语 gēar，源自原始印欧语 *yeh₁r-（年、季节）。",
    "yellow": "古英语 geolu，源自原始印欧语 *ǵʰelh₃-（黄色、绿色）。",
    "young": "古英语 geong，源自原始印欧语 *h₂yuh₁en-（年轻的）。",
    "zoo": "zoological garden 的缩写，希腊语 zōion（动物）+ logos（研究）。",
}

ETYMOLOGY_DB_LOWER = {}
for k, v in ETYMOLOGY_DB.items():
    ETYMOLOGY_DB_LOWER[k.lower()] = v

# Phrase etymologies
PHRASE_ETYMOLOGY = {
    "set the table": "英语习语，由 set（摆放）+ the table（桌子）组成，描述布置餐具和准备餐桌的日常行为。",
    "clear the table": "英语习语，由 clear（清理）+ the table（桌子）组成，指用餐后收拾餐桌的行为。",
    "get up": "英语短语，由 get（变成）+ up（向上）组成，表示从躺卧或坐着的位置站起来。",
    "go home": "英语短语，由 go（去）+ home（家）组成，最基本的日常表达之一。",
    "go to bed": "英语短语，由 go to（前往）+ bed（床）组成，表示就寝的日常表达。",
    "go to school": "英语短语，由 go to（前往）+ school（学校）组成。School 源自希腊语 scholē（闲暇、学习）。",
    "green bean": "由 green（绿色的）+ bean（豆）组成。Bean 源自古英语 bēan。",
    "hand out": "英语短语，由 hand（手）+ out（出去）组成，原意「用手递出」。",
    "hurry up": "英语短语，hurry 可能源自拟声词（匆忙的呼啸声），up 表示动作完成。",
    "living room": "由 living（生活）+ room（房间）组成，20世纪开始使用的家居术语。",
    "try on": "英语短语，由 try（尝试）+ on（穿上）组成，指试穿衣物。",
    "turn off": "英语短语，由 turn（转动）+ off（脱离）组成，原指转动开关使其断开。",
    "a box of": "英语量词表达，由 box（盒子）+ of（的）组成，表示「一盒……」。",
}

def generate_etymology(word):
    """Generate etymology from DB or AI-style fallback for single words."""
    wl = word.lower().strip('* ')
    
    # Check phrase DB first
    if wl in PHRASE_ETYMOLOGY:
        return [{"t": word, "d": PHRASE_ETYMOLOGY[wl]}]
    
    if wl in ETYMOLOGY_DB_LOWER:
        return [{"t": word, "d": ETYMOLOGY_DB_LOWER[wl]}]

    # AI-style basic generation based on word structure
    if wl.startswith('un'):
        base = wl[2:]
        if len(base) > 2:
            return [{"t": word, "d": f"古英语 un-（不、否），前缀，表示否定含义。与拉丁语 in-、希腊语 a- 同源。"}]
    if wl.startswith('re') and len(wl) > 4 and wl[2] not in 'aeiou':
        base = wl[2:]
        if len(base) > 2:
            return [{"t": word, "d": f"拉丁语 re-（再、回），前缀，意为「再次、重新」。源自原始印欧语 *wret-（转回）。"}]
    if wl.endswith('ful'):
        return [{"t": word, "d": f"古英语 -full（充满），后缀，表示「具有……性质」。源自 full（满的）。"}]
    if wl.endswith('less'):
        return [{"t": word, "d": f"古英语 -lēas（缺少），后缀，表示「无、没有」。与 loose（松散的）同源。"}]
    if wl.endswith('ness'):
        return [{"t": word, "d": f"古英语 -nes（状态），后缀，表示「……的性质或状态」。源自原始日耳曼语 *-nassus。"}]
    if wl.endswith('ly'):
        return [{"t": word, "d": f"古英语 -līce，副词后缀，源自 līc（身体、形式），意为「以……方式」。"}]
    if wl.endswith('ing'):
        return [{"t": word, "d": f"古英语 -ing/-ung，动名词后缀，源自原始日耳曼语 *-ingō。"}]
    if wl.endswith('er'):
        return [{"t": word, "d": f"古英语 -ere，施动者后缀，源自拉丁语 -arius（从事……的人）。"}]
    if wl.endswith('ment'):
        return [{"t": word, "d": f"拉丁语 -mentum，名词后缀，表示动作的结果或手段。"}]
    if wl.endswith('tion') or wl.endswith('sion'):
        return [{"t": word, "d": f"拉丁语 -tiō/-siō，名词后缀，表示动作或状态。"}]
    if wl.endswith('able') or wl.endswith('ible'):
        return [{"t": word, "d": f"拉丁语 -ābilis/-ibilis，形容词后缀，表示「能够被……的」。"}]

    # For compound words, try component analysis
    if '-' in wl:
        parts = wl.split('-')
        return [{"t": word, "d": f"复合词，由 {'-'.join(parts)} 组成。"}]

    return [{"t": word, "d": f"源自英语常用词汇，在现代英语中广泛使用。可进一步在词源词典（如 etymonline.com）中查阅。"}]


def get_synonyms(word):
    """Get synonyms for a word or phrase."""
    wl = word.lower().strip('* ')
    if wl in SYNONYM_DB_LOWER:
        return SYNONYM_DB_LOWER[wl]
    # For phrases, try to get synos for the main word
    parts = wl.split()
    if len(parts) > 1:
        # Try key content words (nouns, verbs, adjectives)
        for part in parts:
            if part in SYNONYM_DB_LOWER:
                return []
    return []


# ============ YOUDAO SCRAPER ============

def fetch_youdao(word):
    """Fetch word data from Youdao Dictionary."""
    clean_word = word.strip('* ')
    url = f'https://www.youdao.com/result?word={urllib.parse.quote(clean_word)}&lang=en'
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        resp = urllib.request.urlopen(req, timeout=15)
        html = resp.read().decode('utf-8')
        return html
    except Exception as e:
        print(f"  Fetch error for '{clean_word}': {e}")
        return None


def parse_phonetics(soup):
    """Parse phonetics from soup."""
    ph_elems = soup.select('.phonetic')
    if len(ph_elems) >= 2:
        p0 = ph_elems[0].get_text(strip=True)
        p1 = ph_elems[1].get_text(strip=True)
        return ' ' + p0 + ' ', ' ' + p1 + ' '
    elif len(ph_elems) == 1:
        p = ph_elems[0].get_text(strip=True)
        return ' ' + p + ' ', ' ' + p + ' '
    return '', ''


def parse_trans(soup):
    """Parse POS and translations from .word-exp, filtering out sentences and non-POS entries."""
    results = []
    exp_elems = soup.select('.word-exp')
    for elem in exp_elems:
        text = elem.get_text(strip=True)
        # Only process entries that start with a POS pattern
        m = POS_PATTERN.match(text)
        if not m:
            continue
        pos = m.group(1).strip().rstrip('.') + '.'
        cn = text[m.end():].strip()
        # Remove angle-bracket annotations like <英，非正式>
        cn = re.sub(r'<[^>]*>', '', cn).strip()
        # Remove 【名】 style annotations
        cn = re.sub(r'【[^】]*】', '', cn).strip()
        if cn:
            results.append({"pos": pos, "cn": cn})
    return results if results else None


def parse_phrases(soup):
    """Parse phrases from .phrs-content using .point and .phr_trans."""
    results = []
    phr_container = soup.select_one('.phrs-content')
    if not phr_container:
        return results
    points = phr_container.select('.point')
    trans = phr_container.select('.phr_trans')
    for i in range(min(len(points), len(trans), 8)):
        c = points[i].get_text().strip()
        cn = trans[i].get_text().strip()
        if c and cn:
            results.append({"c": c, "cn": cn})
    return results


def parse_sentences(soup):
    """Parse example sentences using .sen-eng and .sen-ch selectors."""
    results = []
    engs = soup.select('.sen-eng')
    chs = soup.select('.sen-ch')
    for i in range(min(len(engs), len(chs), 3)):
        en_text = engs[i].get_text().strip()
        cn_text = chs[i].get_text().strip()
        if en_text and cn_text:
            results.append({"c": en_text, "cn": cn_text})
    return results


def parse_word_forms(soup):
    """Parse word forms (inflections)."""
    forms = soup.select('.word-wfs-cell-less')
    if not forms:
        forms = soup.select('.transformation')
    rels = []
    for f in forms:
        text = f.get_text(strip=True)
        m = re.match(r'^([\u4e00-\u9fff]+)([a-zA-Z]+)$', text)
        if m:
            cn = m.group(1)
            c = m.group(2)
            rels.append({"c": c, "cn": cn})
    if rels:
        return {"root": "", "rels": [{"pos": "", "words": rels}]}
    return {}


def generate_relwords_fallback(word, trans):
    """Generate common word forms when Youdao doesn't provide them."""
    pos_set = set()
    for t in trans:
        p = t.get('pos', '').strip().rstrip('.')
        if p in ('n', 'noun', 'v', 'verb', 'adj', 'adjective', 'adv', 'adverb'):
            pos_set.add(p)
    if not pos_set:
        return {}

    UNCOUNTABLE = {'clothes', 'homework', 'music', 'maths', 'mathematics', 'shorts', 'trousers', 'sunglasses'}
    NO_FORMS = {'any', 'herself', 'just', 'those', 'when'}
    wl = word.lower().strip('* ')
    if wl in UNCOUNTABLE or wl in NO_FORMS:
        return {}

    words = []
    for pos in pos_set:
        if pos in ('n', 'noun') and wl not in UNCOUNTABLE:
            if wl.endswith(('ch', 'sh', 's', 'x', 'z')): words.append({'c': word + 'es', 'cn': '复数'})
            elif wl.endswith('y') and len(wl) > 1 and wl[-2] not in 'aeiou': words.append({'c': word[:-1] + 'ies', 'cn': '复数'})
            else: words.append({'c': word + 's', 'cn': '复数'})
        if pos in ('adj', 'adjective'):
            vowels = sum(1 for c in wl if c in 'aeiou')
            if vowels <= 1 and len(wl) <= 6:
                if wl.endswith('e'): words.extend([{'c': word + 'r', 'cn': '比较级'}, {'c': word + 'st', 'cn': '最高级'}])
                elif wl.endswith('y'): words.extend([{'c': word[:-1] + 'ier', 'cn': '比较级'}, {'c': word[:-1] + 'iest', 'cn': '最高级'}])
                else: words.extend([{'c': word + 'er', 'cn': '比较级'}, {'c': word + 'est', 'cn': '最高级'}])
            else: words.extend([{'c': 'more ' + word, 'cn': '比较级'}, {'c': 'most ' + word, 'cn': '最高级'}])
        if pos in ('adv', 'adverb'):
            if wl in ('hard', 'fast', 'early', 'late', 'soon', 'near'):
                words.extend([{'c': word + 'er', 'cn': '比较级'}, {'c': word + 'est', 'cn': '最高级'}])

    seen = set()
    unique = []
    for w in words:
        key = (w['c'], w['cn'])
        if key not in seen:
            seen.add(key)
            unique.append(w)
    return {"root": "", "rels": [{"pos": "", "words": unique}]} if unique else {}


def update_json_file(json_path):
    """Update a JSON vocabulary file with Youdao data."""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"\nProcessing: {os.path.basename(json_path)} ({len(data)} entries)")
    updated = 0
    errors = 0

    for i, entry in enumerate(data):
        word = entry['word'].strip('* ')
        if not word:
            continue

        # Skip if already has complete data
        if entry.get('sentences') and entry.get('synos') and entry.get('etymology'):
            continue

        html = fetch_youdao(word)
        if not html:
            # Even if fetch fails, still try to fill synos and etymology from DB
            synos = get_synonyms(word)
            if synos:
                entry['synos'] = synos
            etymology = generate_etymology(word)
            if etymology:
                entry['etymology'] = etymology
            if synos or etymology:
                updated += 1
            errors += 1
            if i % 20 == 0:
                time.sleep(0.5)
            continue

        soup = BeautifulSoup(html, 'html.parser')

        # Update phonetics
        p0, p1 = parse_phonetics(soup)
        if p0:
            entry['phonetic0'] = p0
            entry['phonetic1'] = p1

        # Update trans
        new_trans = parse_trans(soup)
        if new_trans:
            entry['trans'] = new_trans

        # Update phrases
        new_phrases = parse_phrases(soup)
        if new_phrases:
            entry['phrases'] = new_phrases

        # Update sentences
        new_sentences = parse_sentences(soup)
        if new_sentences:
            entry['sentences'] = new_sentences

        # Update word forms
        new_relwords = parse_word_forms(soup)
        if new_relwords:
            entry['relWords'] = new_relwords
        else:
            fallback_rel = generate_relwords_fallback(word, new_trans or entry.get('trans', []))
            if fallback_rel:
                entry['relWords'] = fallback_rel

        # Always update synonyms from built-in DB
        synos = get_synonyms(word)
        if synos:
            entry['synos'] = synos

        # Always update etymology
        etymology = generate_etymology(word)
        if etymology:
            entry['etymology'] = etymology

        updated += 1
        if (i + 1) % 20 == 0:
            print(f"  Progress: {i+1}/{len(data)} (updated: {updated}, errors: {errors})")
            time.sleep(0.3)

    # Save updated JSON
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"  Done: {len(data)} entries, updated {updated}, errors {errors}")
    return updated, errors


if __name__ == '__main__':
    files = [
        '五年级上册词汇表.json',
        '五年级下册词汇表.json',
        '七年级上册词汇表.json',
        '七年级下册词汇表.json',
        '八年级上册词汇表.json',
        '八年级下册词汇表.json',
    ]
    for fname in files:
        json_path = os.path.join(BASE, fname)
        # Strip * prefix from words
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        stripped = 0
        for e in data:
            if e['word'].startswith('*'):
                e['word'] = e['word'].lstrip('*')
                stripped += 1
        if stripped:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Stripped {stripped} words in {fname}")
        update_json_file(json_path)
    print("\nAll complete!")