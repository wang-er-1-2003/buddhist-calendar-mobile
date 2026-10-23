import json, re, os, glob

# Parse pl files to get tibetan lunar day -> gregorian date mapping
# Pattern: "N: Day. name. elem-elem; DD Mon YYYY"
# Month changes when "Tibetan Lunar Month: N" appears

MONTHS_CN = {1:'正',2:'二',3:'三',4:'四',5:'五',6:'六',7:'七',8:'八',9:'九',10:'十',11:'十一',12:'十二'}

def parse_pl(filepath):
    """Return list of (tib_month, tib_day, gregorian_date_str)"""
    results = []
    current_month = None
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            m = re.match(r'Tibetan Lunar Month: (\d+)', line)
            if m:
                current_month = int(m.group(1))
                continue
            # day line: "1: Mon. mon gre. Water-Water; 24 Feb 2020"
            m = re.match(r'^(\d+):\s+\w+\.\s+[^;]+;\s+(\d+\s+\w+\s+\d+)', line)
            if m and current_month:
                day = int(m.group(1))
                greg = m.group(2)
                results.append((current_month, day, greg))
    return results

# Convert "24 Feb 2020" to "2020-02-24"
MON_MAP = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}
def to_iso(s):
    parts = s.split()
    d = int(parts[0]); m = MON_MAP[parts[1]]; y = int(parts[2])
    return f"{y}-{m:02d}-{d:02d}"

# Huiyog days to add
HUIYOG = {
    8:  ('药师佛殊胜日', '藏历每月初八'),
    10: ('莲师荟供日', '藏历每月初十'),
    15: ('月望日（长净/受戒）', '藏历每月十五'),
    21: ('度母荟供日', '藏历每月二十一'),
    25: ('空行母荟供日', '藏历每月二十五'),
    29: ('护法荟供日', '藏历每月二十九'),
    30: ('月晦日（忏悔/百字明）', '藏历每月三十'),
}

# Load existing data
with open(r'D:\一个电脑软件\佛教三系日历手机版\www\data\festival_2020_2040.json','r',encoding='utf-8') as f:
    data = json.load(f)

tib = data['tibetan']

# Process each year 2020-2040
added = 0
for year in range(2020, 2041):
    pl_path = rf'D:\一个电脑软件\时轮历数据\phugpa-calendar-archive\pl_{year}.txt'
    if not os.path.exists(pl_path):
        continue
    days = parse_pl(pl_path)
    year_key = str(year)
    if year_key not in tib:
        tib[year_key] = []
    
    # Get existing date+name set to avoid duplicates
    existing = set()
    for it in tib[year_key]:
        existing.add((it['date'], it['name']))
    
    for tib_month, tib_day, greg in days:
        iso = to_iso(greg)
        # Huiyog days
        if tib_day in HUIYOG:
            name, lunar = HUIYOG[tib_day]
            lunar_full = f"藏历{MONTHS_CN[tib_month]}月{tib_day:02d}"
            entry = {
                'date': iso,
                'name': name,
                'lunar': lunar_full,
                'note': '藏传每月固定荟供日',
                'source': 'phugpa pl'
            }
            if (iso, name) not in existing:
                tib[year_key].append(entry)
                existing.add((iso, name))
                added += 1
        
        # Gu-tor (驱鬼节): 12th month, 29th day
        if tib_month == 12 and tib_day == 29:
            name = '古突（驱鬼节）'
            entry = {
                'date': iso,
                'name': name,
                'lunar': '藏历十二月二十九',
                'note': '岁末除障，寺院跳金刚法舞，吃古突面疙瘩',
                'source': 'phugpa pl'
            }
            if (iso, name) not in existing:
                tib[year_key].append(entry)
                existing.add((iso, name))
                added += 1

# Sort each year by date
for y in tib:
    if isinstance(tib[y], list):
        tib[y].sort(key=lambda x: x['date'])

with open(r'D:\一个电脑软件\佛教三系日历手机版\www\data\festival_2020_2040.json','w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Added {added} entries")
# Count per year
for y in range(2020, 2023):
    print(f"{y}: {len(tib[str(y)])} tibetan entries")
