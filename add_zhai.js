const { Lunar } = require('lunar-javascript');
// 十斋日: 初一、初八、十四、十五、十八、二十三、二十四、二十八、二十九、三十
// 六斋日: 初八、十四、十五、二十三、二十九、三十
const shizhai = [1, 8, 14, 15, 18, 23, 24, 28, 29, 30];
const liuzhai = [8, 14, 15, 23, 29, 30];

const fs = require('fs');
const data = JSON.parse(fs.readFileSync('D:/一个电脑软件/佛教三系日历手机版/www/data/festival_2020_2040.json','utf8'));

let added = 0;
for (let year = 2020; year <= 2040; year++) {
  const han = data.han[String(year)];
  if (!han) continue;
  // iterate each day of the year
  for (let m = 1; m <= 12; m++) {
    for (let d = 1; d <= 31; d++) {
      let lunar;
      try {
        lunar = Lunar.fromYmd(year, m, d);
      } catch(e) { continue; }
      const ld = lunar.getDay();
      const lm = lunar.getMonth();
      // skip leap month
      if (lunar.getMonth() < 0) continue;
      
      const isShi = shizhai.includes(ld);
      const isLiu = liuzhai.includes(ld);
      if (!isShi && !isLiu) continue;
      
      const greg = `${year}-${String(m).padStart(2,'0')}-${String(d).padStart(2,'0')}`;
      const lunarStr = `农历${lm}月${ld}`;
      
      let name, note;
      if (isShi && isLiu) {
        name = '六斋日／十斋日';
        note = '汉传斋日';
      } else if (isShi) {
        name = '十斋日';
        note = '汉传斋日';
      } else {
        name = '六斋日';
        note = '汉传斋日';
      }
      
      // check not already added
      if (!han.find(e => e.date === greg && e.note === '汉传斋日')) {
        han.push({
          date: greg,
          name: name,
          lunar: lunarStr,
          note: note,
          source: 'lunar-javascript'
        });
        added++;
      }
    }
  }
  han.sort((a,b) => a.date < b.date ? -1 : 1);
}

fs.writeFileSync('D:/一个电脑软件/佛教三系日历手机版/www/data/festival_2020_2040.json', JSON.stringify(data, null, 2));
console.log(`Added ${added} zhai entries`);
console.log(`2020 han entries: ${data.han['2020'].length}`);
