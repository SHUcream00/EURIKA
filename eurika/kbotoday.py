from bs4 import BeautifulSoup as bs
import asyncio
import re
import aiosqlite
import aiohttp
import time
import datetime
import json

cwd = r'C:\EurikaMkIII' #fallback

async def kbo():
    ns_prefix = "https://sports.news.naver.com"
    target = "https://sports.news.naver.com/kbaseball/schedule/index.nhn"
    async with aiohttp.ClientSession() as session:
        async with session.get(target) as resp:
            raw = await resp.text()

    soup = bs(raw, "lxml") #can i make it an async?
    games = soup.find_all("li", class_="live") + soup.find_all("li", class_="before_game")
    if len(games) == 0:
        games = soup.find_all("li", class_="end")
    #broadcast = a, btn_ltr
    res = []
    for i in games:
        temp, etc = {}, []
        for j in i.findChildren():

            if j.name == 'em':
                temp['start_time'] = j.text.replace("\n","").replace(chr(32),"")
            elif j.name == 'a':
                if j.get('href').startswith('http://'):
                    temp[j.text.replace("\n","").replace(chr(32),"")] = j.get('href')
                else:
                    temp[j.text.replace("\n","").replace(chr(32),"")] = ns_prefix + j.get('href')
            else:
                if len(j.get_text().replace("\n", "").replace(chr(32), "")) != 0:
                    etc.append(j.get_text().replace("\n", "").replace(chr(32), ""))
        temp['etc'] = etc
        res.append(temp)
    #print(res)
    return res

async def standing():
    kboteam = {'SK': '씹솩', 'KT': '꼴콱', 'KIA': '홍어', 'LG': '좆쥐', '두산': '범죄', '롯데': '꼴데',
               'NC': '입양', '키움': '거지', '한화': '꼴칰', '삼성': '칩성'}

    async with aiosqlite.connect(cwd + "\db\EurKBODB.db") as db:
        async with db.execute("SELECT * FROM Etcdata WHERE name='standing' LIMIT 1") as cursor:
            entry = await cursor.fetchone()
            if entry[2] != time.strftime('%Y-%m-%d %H'):
                async with aiohttp.ClientSession() as session:
                    async with session.get("http://www.koreabaseball.com/TeamRank/TeamRank.aspx") as kbohtml:
                        html = await kbohtml.text()
                        await db.execute("UPDATE Etcdata SET last_checked='{}', cache='{}' WHERE name='standing'".format(time.strftime('%Y-%m-%d %H'), html.replace(chr(39),"")))
                        await db.commit()
            else:
                html = entry[3]

    soup = bs(html, 'lxml')
    res = "        팀명    승   패   무   승률\n" \
          + "    ================================="
    i = 1
    while (i <= 10):
        res += "\n"
        base = soup.findAll("tr")[i]

        for j,k in enumerate(base.findAll("td")[0:7]):
            text = k.get_text()
            if j == 1:
                res += "{:>5}".format(kboteam.get(text, text))
            elif j in [0,3,4,5]:
                res += "{:>5}".format(text)
            elif j == 6:
                res += "{:>8}".format(text)

        i += 1
    return res

async def stat_leaders(**kwargs):
        kboteam = {'SK': '씹솩', 'KT': '꼴콱', 'KIA': '홍어', 'LG': '좆쥐', '두산': '범죄', '롯데': '꼴데',
                   'NC': '입양', '키움': '거지', '한화': '꼴칰', '삼성': '칩성'}
        kbocategory = {'타율': "/Record/Player/HitterBasic/Basic1.aspx?sort=HRA_RT", '홈런': "/Record/Player/HitterBasic/Basic1.aspx?sort=HR_CN"
                , '타점': "/Record/Player/HitterBasic/Basic1.aspx?sort=RBI_CN", '도루': "/Record/Player/Runner/Basic.aspx?sort=SB_CN"
                , '득점': "/Record/Player/HitterBasic/Basic1.aspx?sort=RUN_CN", '안타': "/Record/Player/HitterBasic/Basic1.aspx?sort=HIT_CN"
                , '출루율': "/Record/Player/HitterBasic/Basic2.aspx?sort=OBP_RT", '장타율': "/Record/Player/HitterBasic/Basic2.aspx?sort=SLG_RT"
                , '2루타': "/Record/Player/HitterBasic/Basic1.aspx?sort=H2_CN", '3루타': "/Record/Player/HitterBasic/Basic1.aspx?sort=H3_CN"
                , '루타': "/Record/Player/HitterBasic/Basic1.aspx?sort=TB_CN", 'OPS': "/Record/Player/HitterBasic/Basic2.aspx?sort=OPS_RT"
                , '타수': "/Record/Player/HitterBasic/Basic1.aspx?sort=AB_CN", '볼넷': "/Record/Player/HitterBasic/Basic2.aspx?sort=BB_CN"
                , '삼진': "/Record/Player/HitterBasic/Basic2.aspx?sort=KK_CN", '평자점': "/Record/Player/PitcherBasic/Basic1.aspx?sort=ERA_RT"
                , '승리': "/Record/Player/PitcherBasic/Basic1.aspx?sort=W_CN", '세이브': "/Record/Player/PitcherBasic/Basic1.aspx?sort=SV_CN"
                , '승률': "/Record/Player/PitcherBasic/Basic1.aspx?sort=WRA_RT", '홀드': "/Record/Player/PitcherBasic/Basic1.aspx?sort=HOLD_CN"
                , '탈삼진': "/Record/Player/PitcherBasic/Basic1.aspx?sort=KK_CN", '경기': "/Record/Player/PitcherBasic/Basic1.aspx?sort=GAME_CN"
                , '패배': "/Record/Player/PitcherBasic/Basic1.aspx?sort=L_CN", '이닝': "/Record/Player/PitcherBasic/Basic1.aspx?sort=INN2_CN"
                , '볼넷': "/Record/Player/PitcherBasic/Basic1.aspx?sort=BB_CN", 'WHIP': "/Record/Player/PitcherBasic/Basic1.aspx?sort=WHIP_RT"
                , '완투': "/Record/Player/PitcherBasic/Basic2.aspx?sort=CG_CN", '완봉': "/Record/Player/PitcherBasic/Basic2.aspx?sort=SHO_CN"
                , '퀄스': "/Record/Player/PitcherBasic/Basic2.aspx?sort=QS_CN", '피안타율': "/Record/Player/PitcherBasic/Basic2.aspx?sort=OAVG_RT"}


        if kwargs['category'] not in kbocategory:
            return None

        async with aiosqlite.connect(cwd + "\db\EurKBODB.db") as db:
            async with db.execute("SELECT * FROM Etcdata WHERE name='{}' LIMIT 1".format(kwargs['category'])) as cursor:
                entry = await cursor.fetchone()
                if entry[2] != time.strftime('%Y-%m-%d %H'):
                    async with aiohttp.ClientSession() as kboses:
                        async with kboses.get("https://www.koreabaseball.com/{}".format(kbocategory.get(kwargs['category'], ''))) as kbohtml:
                            html = await kbohtml.text()
                            await db.execute("UPDATE Etcdata SET last_checked='{}', cache='{}' WHERE name='{}'"\
                                            .format(time.strftime('%Y-%m-%d %H'), html.replace(chr(39),""), kwargs['category']))
                            await db.commit()
                else:
                    html = entry[3]

        soup = bs(html, 'lxml')
        key = kbocategory.get(kwargs["category"]).split(chr(61))[1]
        res = []
        for i in soup.find_all("tr")[1:11]:
            temp = []
            childs = i.findChildren()
            temp.extend(list(map(lambda x: x.get_text(), childs[0:4])))
            for j in childs:
                if j.attrs.get("data-id", None) == key:
                    temp.append(j.get_text())
            res.append(temp)

        wrapped = "{:^30}\n".format(kwargs['category'] + "랭킹")
        wrapped += "{:>4} {:>5} {:>8} {:>5}\n====================================\n".format("순위", "이름", "소속팀", kwargs['category'])
        for k in res:
            wrapped += "{:>4} {:>6} {:>6} {:>7}\n".format(k[0], k[1].rjust(5, "ㅤ"), kboteam.get(k[3], k[3]), k[4])

        return wrapped

async def player(*args, **kwargs):
    async with aiosqlite.connect(cwd + "\db\EurKBODB.db") as db:
        async with db.execute("SELECT * FROM Players WHERE name='{}'".format(kwargs['name'])) as cursor:
            kbotgt = await cursor.fetchall()
            kbores = []
            if len(kbotgt) < 1:
                await kakasi(name = kwargs['name'])
                cursor = await db.execute("SELECT * FROM Players WHERE name='{}'".format(kwargs['name']))
                kbotgt = await cursor.fetchall()

        res = []
        for i in kbotgt:
            photo_prefix = "https:"
            if i[5] == time.strftime('%Y-%m-%d'):
                temp = json.loads(i[6])
            else:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"http://www.koreabaseball.com/Record/Player/{i[3]}Detail/Basic.aspx?playerId={i[2]}") as resp:
                        html = await resp.text()

                    soup = bs(html, 'lxml')
                    stat_title = list(map(lambda x: x.getText().lower(), sum([tr.find_all('th') for tr in soup.find_all('thead', limit=2)], [])))
                    stat_data = list(map(lambda x: x.getText(), sum([tr.find_all('td') for tr in soup.find_all('tbody', limit=2)], [])))
                    temp = {i: j for i, j in zip(stat_title, stat_data)}
                    temp['type'] = i[3]
                    temp['name'] = kwargs['name']
                    temp['backno'] = soup.find(id="cphContents_cphContents_cphContents_playerProfile_lblBackNo").getText()
                    temp['birth'] = soup.find(id="cphContents_cphContents_cphContents_playerProfile_lblBirthday").getText()
                    temp['from_bt'] = divmod((datetime.datetime.now() - datetime.datetime.strptime('-'.join(re.findall(r'\d+', temp['birth'])), "%Y-%m-%d")).days, 365)
                    temp['pos'] = soup.find(id="cphContents_cphContents_cphContents_playerProfile_lblPosition").getText()
                    temp['pic'] = "https:" + soup.find(id="cphContents_cphContents_cphContents_playerProfile_imgProgile")['src']
                    temp['nick'] = i[4]
                    employer = soup.find("h4", {"class": lambda x: x and x.startswith('team regular')})
                    temp['teamname'] = employer.getText() if employer else "무소속"
                    if temp['팀명'] != "기록이 없습니다.":
                        temp['active'] = True
                        if temp['type'] == 'Pitcher':
                            temp['ip_f'] = eval(temp['ip'].replace(chr(32), chr(43)))
                            #FIP (13*HR+3*(HBP+BB)-2*K)/IP, plus a constant (usually around 3.2) to put it on the same scale as earned run average.
                            temp['fip'] = round((13 * int(temp['hr']) + 3 * int(temp['bb']) - 2 * int(temp['so'])) /temp['ip_f'] + 3.3, 2)
                            temp['babip'] = round((int(temp['h'])-int(temp['hr']))/(int(temp['tbf']) - int(temp['sac']) + int(temp['sf']) -int(temp['bb']) - int(temp['ibb'])-int(temp['so'])-int(temp['hr'])),3)
                        else:
                            temp['babip'] = round((int(temp['h'])-int(temp['hr']))/(int(temp['ab']) - int(temp['sac']) + int(temp['sf']) - int(temp['so']) - int(temp['hr'])),3)
                            temp['woba'] = round((0.690 * (int(temp['bb'])-int(temp['ibb'])) + 0.722 * int(temp['hbp']) + 0.888 * (int(temp['h']) - int(temp['2b']) - int(temp['3b']) - int(temp['hr']))\
                                            + 1.271 * int(temp['2b']) + 1.616 * int(temp['3b']) + 2.101 * int(temp['hr'])) / (int(temp['ab']) + int(temp['bb']) - int(temp['ibb'])  + int(temp['sf']) + int(temp['hbp'])),3)
                    else:
                        temp['active'] = False

                    await db.execute("UPDATE Players SET last_checked='{}', cache='{}' Where id='{}'".format(time.strftime('%Y-%m-%d'), json.dumps(temp), i[2]))
                    await db.commit()

            res.append(temp)

        return res

async def kakasi(**kwargs):
    async with aiosqlite.connect(cwd + "\db\EurKBODB.db") as db:
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.koreabaseball.com/Player/Search.aspx?searchWord={}'.format(kwargs['name'])) as kbocs:
                kbohtml = await kbocs.text()
                soup = bs(kbohtml, 'lxml')
                for i in soup.find('tbody').find_all('tr'):
                    base = list(map(lambda x: x.getText(), i.findChildren()))
                    if base[0] == "#":
                        continue
                    elif base[1] == kwargs['name']:
                        link = i.find('a')['href']
                        id_ = link.split("=")[1]
                        pos = "Pitcher" if base[4] == "투수" else "Hitter"
                        await db.execute(f"INSERT INTO Players (id, name, type, nick) VALUES ('{id_}', '{base[1]}', '{pos}', '')")

        await db.commit()

def tdrem(a):
    return str(a).strip('<td/>')

'''
#Test Driver
if __name__ == "__main__":
    a = asyncio.get_event_loop()
    a.run_until_complete(kbo())
'''
