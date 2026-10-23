import json, ephem
from datetime import datetime, timedelta

# Get all new moons and full moons from 2020-2040
def get_moons(start_year, end_year):
    nm = []  # new moon dates
    fm = []  # full moon dates
    # start from before 2020
    prev = ephem.Date(datetime(start_year-1, 12, 1))
    m = ephem.Moon()
    # iterate
    d = ephem.Date(datetime(start_year, 1, 1))
    end = ephem.Date(datetime(end_year, 12, 31))
    # new moon: sun and moon same longitude. Use ephem.next_new_moon
    nm_date = ephem.next_new_moon(d)
    while nm_date < end:
        dt = nm_date.datetime()
        if dt.year >= start_year:
            nm.append(dt)
        nm_date = ephem.next_new_moon(nm_date)
    fm_date = ephem.next_full_moon(d)
    while fm_date < end:
        dt = fm_date.datetime()
        if dt.year >= start_year:
            fm.append(dt)
        fm_date = ephem.next_full_moon(fm_date)
    return sorted(nm), sorted(fm)

nm, fm = get_moons(2020, 2040)
print(f"New moons: {len(nm)}, Full moons: {len(fm)}")
print("First new moon:", nm[0].date())
print("First full moon:", fm[0].date())

# Build uposatha entries: for each new moon -> 黑月十四 + 黑月十五; for each full moon -> 白月十四 + 白月十五
# Note: 黑月十四 = day before new moon, 黑月十五 = new moon day
#       白月十四 = day before full moon, 白月十五 = full moon day

entries_by_year = {}
for d_list, label_14, label_15 in [(nm, '黑月十四（新月前一日）', '黑月十五（新月日·晦）'),
                                     (fm, '白月十四（满月前一日）', '白月十五（满月日·望）')]:
    for dt in d_list:
        y = dt.year
        if y not in entries_by_year:
            entries_by_year[y] = []
        # 14th = day before
        d14 = dt - timedelta(days=1)
        entries_by_year[y].append({
            'date': d14.strftime('%Y-%m-%d'),
            'name': f'布萨日（{label_14}）',
            'lunar': f'傣历月相日',
            'note': '南传上座部四布萨日',
            'source': 'ephem月相推算'
        })
        # 15th = the moon day itself
        entries_by_year[y].append({
            'date': dt.strftime('%Y-%m-%d'),
            'name': f'布萨日（{label_15}）',
            'lunar': f'傣历月相日',
            'note': '南传上座部四布萨日',
            'source': 'ephem月相推算'
        })

# Load existing data
with open(r'D:\一个电脑软件\佛教三系日历手机版\www\data\festival_2020_2040.json','r',encoding='utf-8') as f:
    data = json.load(f)

south = data['south']
added = 0
for y in range(2020, 2041):
    yk = str(y)
    if yk not in south:
        south[yk] = []
    existing = set((e['date'], e['name']) for e in south[yk])
    if y in entries_by_year:
        for e in entries_by_year[y]:
            key = (e['date'], e['name'])
            if key not in existing:
                south[yk].append(e)
                existing.add(key)
                added += 1
    south[yk].sort(key=lambda x: x['date'])

with open(r'D:\一个电脑软件\佛教三系日历手机版\www\data\festival_2020_2040.json','w',encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Added {added} uposatha entries")
print(f"2020 south entries: {len(south['2020'])}")
