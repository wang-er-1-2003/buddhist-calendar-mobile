import json

with open(r'D:\一个电脑软件\佛教三系节日历\data\festival_2020_2040.json','r',encoding='utf-8') as f:
    d = json.load(f)

# Move entries whose date year doesn't match the data year
moved = 0
for year in range(2020, 2041):
    yk = str(year)
    if yk not in d['tibetan']: continue
    keep = []
    move = []
    for it in d['tibetan'][yk]:
        it_year = int(it['date'][:4])
        if it_year == year:
            keep.append(it)
        else:
            move.append(it)
    if move:
        d['tibetan'][yk] = keep
        if str(it_year) not in d['tibetan']:
            d['tibetan'][str(it_year)] = []
        d['tibetan'][str(it_year)].extend(move)
        moved += len(move)
        print(f"Moved {len(move)} entries from {year} to {it_year}")

# Sort all years
for y in d['tibetan']:
    if isinstance(d['tibetan'][y], list):
        d['tibetan'][y].sort(key=lambda x: x['date'])

with open(r'D:\一个电脑软件\佛教三系节日历\data\festival_2020_2040.json','w',encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print(f"Total moved: {moved}")
print(f"2026 tibetan entries: {len(d['tibetan']['2026'])}")
print(f"2027 tibetan entries: {len(d['tibetan']['2027'])}")
