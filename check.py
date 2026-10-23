import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'D:\一个电脑软件\佛教三系节日历\data\festival_2020_2040.json','r',encoding='utf-8') as f:
    d = json.load(f)
tib = d['tibetan']['2026']
for it in tib:
    print(it['date'], '|', it['name'][:30], '|', it.get('note',''))
