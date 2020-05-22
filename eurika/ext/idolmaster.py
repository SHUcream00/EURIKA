import sqlite3
import aiosqlite
import discord
import os
import asyncio
import aiohttp
import random
import re
import json
from math import ceil
import ast
from bs4 import BeautifulSoup as bs

cwd = r'C:\EurikaMkIII'

class idm():
    async def rank():
        idmevelist = ['7', '9']
        idmres = []
        for i,j in enumerate(idmevelist):
            async with aiohttp.ClientSession() as session:
                async with session.get('https://days.765prolive.theater/event/' + j) as idms:
                    idmhtml = await idms.text()
                    soup = bs(idmhtml, 'lxml')
                    idmres.append(soup.find('li', {"class" : 'active'}).get_text())
                async with session.get('https://days.765prolive.theater/api/event/' + j + '/score_ranking.json') as idms:
                    if i == 0:
                        idmjson = await idms.json()
                    else:
                        idmjson2 = await idms.json()
                        idmlat = len(idmjson2['data']) -1
                        idmres.extend([len(idmjson2['data']) -1, idmjson2['data'][idmlat]['date'], idmjson2['data'][idmlat-1]['reward1'], idmjson2['data'][idmlat]['reward1'], idmjson2['data'][idmlat]['reward1'] - idmjson2['data'][idmlat-1]['reward1'], idmjson['data'][idmlat]['reward1'], idmjson2['data'][idmlat]['reward1'] - idmjson['data'][idmlat]['reward1']])
                async with session.get('https://days.765prolive.theater/api/event/' + j + '/point_ranking.json') as idms:
                    if i == 0:
                        idmjson3 = await idms.json()
                    else:
                        idmjson4 = await idms.json()
                        idmlat2 = len(idmjson4['data']) -1
                        idmres.extend([len(idmjson4['data']) -1, idmjson4['data'][idmlat2]['date'], idmjson4['data'][idmlat2-1]['reward1'], idmjson4['data'][idmlat2]['reward1'], idmjson4['data'][idmlat2]['reward1'] - idmjson4['data'][idmlat2-1]['reward1'], idmjson3['data'][idmlat2]['reward1'], idmjson4['data'][idmlat2]['reward1'] - idmjson3['data'][idmlat2]['reward1']])
        idmres2 = '```python\n' + str(idmres[1]) + '[스코어 랭킹] 2000위\n' + '지난 집계 대비: ' + str(idmres[4]) + ' -> ' + str(idmres[5]) + '(' + str(idmres[6]) + ')\n' + '지난 이벤트 동 시점 대비: ' + str(idmres[7]) + ' -> ' + str(idmres[5]) + '(' + str(idmres[8]) + ')' + '```' \
                + '```python\n' + str(idmres[1]) + '[포인트 랭킹] 2000위\n' + '지난 집계 대비: ' + str(idmres[11]) + ' -> ' + str(idmres[12]) + '(' + str(idmres[13]) + ')\n' + '지난 이벤트 동 시점 대비: ' + str(idmres[14]) + ' -> ' + str(idmres[12]) + '(' + str(idmres[15]) + ')' + '```\n'
        em = discord.Embed(title=idmres[3] + ' 집계', description=idmres2, colour=0xFF9900)
        em.set_author(name = '난토! ' + idmres[1], icon_url='https://pbs.twimg.com/profile_images/882108935846494208/Dt4Z0cKT_400x400.jpg')
        return em

class deresute():
    async def info(idname, **kwargs):
        async with aiosqlite.connect(cwd + "\db\EurIDDB.db") as db:
            cursor = await db.execute(f"SELECT * FROM Dere WHERE name like '%{idname}%' or rname like '%{idname}%' or sdesc like '%{idname}%'")
            idlist = await cursor.fetchall()
            idres, idtemp = '', ''
            if len(idlist) == 1 and len(kwargs) == 0:
                return await deresute.info(idname, choice=str(1))
            if len(idlist) >= 1:
                if len(kwargs) == 0:
                    idtemp = ''
                    for i, j in enumerate(idlist):
                        name = j[1].replace('\n', '')
                        idtemp += f"[{str(i+1)}] {name} {j[3]}\n"

                    em = discord.Embed(description=f"```python\n{idtemp}```", colour=0xd4eff6)
                    em.set_author(name = f'[346 Production Database] {idname}', icon_url='https://cdn.discordapp.com/attachments/296519249134878720/361295374096400395/985ece29109645dfc2f4eab2670814f6c2da91be29fb5bf16718ace517392269c7940d364597217251b3fa7bdacc1582bc97.png')
                    em.set_thumbnail(url=idlist[0][16])
                    em.set_footer(text='몇 번으로 할까? 숫자만 입력해')
                    return 1, em
                else:
                    idtgt = idlist[int(kwargs['choice']) -1]
                    name = idtgt[1].replace('\n', '')
                    em = discord.Embed(colour=0xd4eff6)
                    em.set_author(name = f"{name} {idtgt[4]} {idtgt[3]}", icon_url='https://cdn.discordapp.com/attachments/88844446929547264/361259695375384586/7KdUBWma_400x400.jpg')
                    em.add_field(name = '**Stat**', value = f"**Life** {idtgt[6]} **Vocal** {idtgt[7]} **Dance** {idtgt[8]} **Visual** {idtgt[9]}")
                    em.set_thumbnail(url=idtgt[16])
                    if idtgt[10] != '':
                        em.add_field(name = f'**Leader Skill** {idtgt[10]}', value = idtgt[11])
                    if idtgt[12] != '':
                        em.add_field(name = f'**Skill** {idtgt[12]}', value = f"{idtgt[13]} [MAX]")
                    if idtgt[14] != '':
                        em.set_image(url=idtgt[14])
                    else:
                        em.set_image(url=idtgt[15])
                    return 0, em

            else :
                em = discord.Embed(title=f'{idname}? 모르는 아이네.', colour=0xB5002B)
                return 0, em

    async def kakasi(**kwargs):
        newscouts = 0
        newscoutnames = '\n```python\n'
        async with aiosqlite.connect(cwd + "\db\EurIDDB.db") as db:
            async with aiohttp.ClientSession() as idses:
                async with idses.get('http://imas.inven.co.kr/dataninfo/card/sl_list.php') as idcs:
                    idshtml = await idcs.text()
                    soup = bs(idshtml, 'lxml')
                    idsl = soup.find_all('a', {"onmouseover" : lambda L: L and L.startswith('IMAS.Db')})
                    for i, j in enumerate(idsl):
                        idsprb = str(j['href']).split('=')[2]
                        cursor = await db.execute(f"SELECT * FROM Dere WHERE id='{idsprb}' COLLATE NOCASE")
                        idscres = await cursor.fetchall()
                        if len(idscres) == 0:
                            idskil = j.find('span')
                            idskil.extract()
                            idsdata = await deresute.chidori(link = j['href'], code = idsprb, name = j.get_text())
                            await db.execute("INSERT INTO Dere (id, name, rname, grade, type, maxlevel, life, vocal, dance, visual, lsname, lsdesc, sname, sdesc, illustbig, illustcard, illustsd) VALUES ('" + idsdata[0] +"', '"+ idsdata[1].replace(chr(39), '') +"', '"+ idsdata[5][0] +"', '"+ idsdata[5][1] +"', '"+ idsdata[5][2] +"', '"+ idsdata[5][3] +"', '"+ idsdata[5][4] +"', '"+ idsdata[5][5] +"', '"+ idsdata[5][6] +"', '"+ idsdata[5][7] +"', '"+ idsdata[5][8] +"', '"+ idsdata[5][9] +"', '"+ idsdata[5][10] +"', '"+ idsdata[5][11] +"', '"+ idsdata[2] +"', '"+ idsdata[3] +"', '"+ idsdata[4] + "')")

                            newscouts += 1
                            newscoutnames += idsdata[1] + '\n'

            await db.commit()

        if newscouts > 0:
            em = discord.Embed(title='유리카가 길거리에서 좆데돌들을 찾기 시작합니다.', description='난토!\n신규 좆데돌이 ' + str(newscouts) + '명 발견되었습니다!\n대상은 다음과 같습니다: ' + newscoutnames + '\n```', colour=0x9117A1)
            em.set_thumbnail(url='https://cdn.discordapp.com/attachments/88844446929547264/391102821392580609/1507101018_3.png')
        else:
            em = discord.Embed(title='유리카가 길거리에서 좆데돌들을 찾기 시작합니다.', description='안타깝게도 좆데돌은 발견되지 않았습니다.', colour=0x9117A1)
        return em

    async def chidori(**kwargs):
        async with aiohttp.ClientSession() as idses:
            async with idses.get(kwargs['link']) as idcs:
                idshtml = await idcs.text()
                soup = bs(idshtml, 'lxml')
                idsimgb = soup.find('div', {'class': 'details'}).find('img')['src']
                idsimgc = soup.find('div', {'class': 'image1'}).find('img')['src']
                idsimgp = soup.find('div', {'class': 'petit'}).find('img')['src']
                idsdat = []
                for i in soup.find_all('td', {'colspan': '3'}):
                    if '<b>' in str(i):
                        idstmp = str(i).replace('</b>', '`').split('`')
                        idsdat.append(re.sub('<[^<]+?>', '', idstmp[0]))
                        idsdat.append(re.sub('<[^<]+?>', '', idstmp[1]))
                    else:
                        if '->' in i.get_text():
                            idsdat.append(re.sub('<[^<]+?>', '', str(i.get_text().split('->')[1].strip())))
                        else:
                            idsdat.append(re.sub('<[^<]+?>', '', str(i)))

                return kwargs['code'], kwargs['name'], idsimgb, idsimgc, idsimgp, idsdat



class milisita():
    async def info(idname, **kwargs):
        async with aiosqlite.connect(cwd + "\db\EurIDDB.db") as db:
            cursor = await db.execute(f"SELECT * FROM Mili WHERE name like '%{idname}%' or rname like '%{idname}%' or sdesc like '%{idname}%'")
            idlist = await cursor.fetchall()

            idres, idtemp = '', ''
            if len(idlist) == 1 and len(kwargs) == 0:
                return await milisita.info(idname, choice=str(1))
            if len(idlist) >= 1:
                if len(kwargs) == 0:
                    idtemp = ''

                    for i, j in enumerate(idlist):
                        name = j[1].replace('\n', '')
                        idtemp += f"[{str(i+1)}]{name} {j[3]}\n"

                    em = discord.Embed(description = f"```python\n{idtemp}```", colour=0xd4eff6)
                    em.set_author(name = f'[765 Production Database] {idname}', icon_url='https://cdn.discordapp.com/attachments/88844446929547264/448049256096333825/33593040.png')
                    em.set_footer(text='몇 번으로 할까? 숫자만 입력해')
                    return 1, em
                else:
                    em = discord.Embed(colour=0xd4eff6)
                    idtgt = idlist[int(kwargs['choice']) -1]
                    name = idtgt[1].replace('\n', '')
                    em.set_author(name = f"{name} {idtgt[4]} {idtgt[3]}", icon_url='https://cdn.discordapp.com/attachments/88844446929547264/361259695375384586/7KdUBWma_400x400.jpg')
                    em.add_field(name = '**Stat**', value = f"**Life** {idtgt[6]}\n**Vocal** {idtgt[7]}\n**Dance** {idtgt[9]}\n**Visual** {idtgt[11]}")
                    em.add_field(name = '**★4Stat**', value = f"**Life** {idtgt[6]}\n**Vocal** {idtgt[8]}\n**Dance** {idtgt[10]}\n**Visual** {idtgt[12]}")
                    if idtgt[10] != '':
                        em.add_field(name = "**Leader Skill**", value = f"**[{idtgt[13]}]**\n{idtgt[14]}")
                    if idtgt[12] != '':
                        em.add_field(name = f"**Skill**", value = f'**[{idtgt[15]}]**\n{idtgt[16]}[MAX]')
                    if idtgt[17] != '':
                        em.set_image(url=idtgt[random.randint(17,18)])
                    else:
                        em.set_image(url=idtgt[random.randint(19,20)])
                    return 0, em

            else :
                em = discord.Embed(title=f'{idname}? 모르는 아이네', colour=0xB5002B)
                return 0, em


    async def kakasi(**kwargs):
        newscouts = 0
        newscoutnames = '\n```python\n'
        async with aiosqlite.connect(cwd + "\db\EurIDDB.db") as db:
            async with aiohttp.ClientSession() as idses:
                async with idses.get('http://imas.inven.co.kr/dataninfo/card/mi_list.php') as idcs:
                    idshtml = await idcs.text()
                    soup = bs(idshtml, 'lxml')
                    idsl = soup.find_all('a', {"href" : lambda L: L and L.startswith('http://imas.inven.co.kr/dataninfo/card/mi_detail.php?d=124&c')})
                    for i, j in enumerate(idsl):
                        if j.get_text() != '':
                            idsprb = str(j['href']).split('=')[2]
                            cursor = await db.execute("SELECT * FROM Mili WHERE id={} COLLATE NOCASE".format(idsprb))
                            idscres = await cursor.fetchall()
                            if len(idscres) == 0:
                                idsdata = await milisita.chidori(link = j['href'], code = idsprb, name = '[' + j.get_text().split('[')[1])
                                await db.execute("INSERT INTO Mili (id, name, rname, grade, type, maxlevel, life, vocal, " \
                                               + "vocal4, dance, dance4, visual, visual4, lsname, lsdesc, sname, sdesc, illustbig, " \
                                               + "illustbigex, illustcard, illustcardex) " \
                                               + "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                               (idsdata[0], idsdata[1], idsdata[3][0], idsdata[3][1], idsdata[3][2], idsdata[3][4], idsdata[3][3],
                                                idsdata[3][10], idsdata[3][14], idsdata[3][11], idsdata[3][15], idsdata[3][12], idsdata[3][16],
                                                idsdata[3][5], idsdata[3][6], idsdata[3][7], idsdata[3][8], idsdata[2][0], idsdata[2][1],
                                                idsdata[2][2], idsdata[2][3]))
                                newscouts += 1
                                newscoutnames += idsdata[1] + '\n'
            await db.commit()

        if newscouts > 0:
            em = discord.Embed(title='유리카가 길거리에서 씹타돌들을 찾기 시작합니다.', description='난토!\n신규 씹타돌이 ' + str(newscouts) + '명 발견되었습니다!\n대상은 다음과 같습니다: ' + newscoutnames + '\n```', colour=0x9117A1)
            em.set_thumbnail(url='https://cdn.discordapp.com/attachments/88844446929547264/391102821392580609/1507101018_3.png')
        else:
            em = discord.Embed(title='유리카가 길거리에서 씹타돌들을 찾기 시작합니다.', description='안타깝게도 씹타돌은 발견되지 않았습니다.', colour=0x9117A1)
        return em

    async def chidori(**kwargs):
        idsdat = []
        img = []

        async with aiohttp.ClientSession() as idses:
            async with idses.get(kwargs['link']) as idcs:
                idshtml = await idcs.text()
                soup = bs(idshtml, 'lxml')
                image_bg = soup.find('div', {'class': 'details'}).find('img')['src']
                if 'bg' in image_bg:
                    img.append(image_bg)
                    img.append(image_bg.replace('bg', 'bgex'))
                else:
                    img.append('')
                    img.append('')
                image_card = soup.find('div', {'class': 'image1'}).find('img')['src']
                img.append(image_card)
                img.append(image_card.replace('card', 'cardex'))

                for i in soup.find_all('td', {'colspan': '3'}):
                    if '<b>' in str(i):
                        idstmp = str(i).replace('</b>', '`').split('`')
                        idsdat.append(re.sub('<[^<]+?>', '', idstmp[0]))
                        idsdat.append(re.sub('<[^<]+?>', '', idstmp[1]))
                    else:
                        idsdat.append(re.sub('<[^<]+?>', '', str(i)))

                for j, k in enumerate(soup.find_all('td')):
                    if j >= 11:
                        if k.get_text() != '':
                            idsdat.append(k.get_text())
                        else:
                            idsdat.append('')

                return kwargs['code'], kwargs['name'], img, idsdat


    async def statrank(*args, **kwargs):
        db = sqlite3.connect(cwd + "\db\EurIDDB.db")
        cursor = db.cursor()
        sortlist = cursor.execute("SELECT * FROM Mili ORDER BY {} DESC LIMIT 10".format(kwargs['stat'])).fetchall()
        #result = '```python\n'
        result = ''
        for i, j in enumerate(sortlist):
            result += '[{}]{} {}\n[보컬/비주얼/댄스]{}/{}/{}\n'.format(str(i+1), j[1], j[3], j[8], j[10], j[12])
        #result += '```'

        em = discord.Embed(description=result, colour=0xd4eff6)
        return 0, em
