'''
Azurelane data for EURIKA
'''

import discord
import asyncio
import aiohttp
import random
import re
import aiosqlite

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, tools
from oauth2client import client as gclient


cwd = r'C:\EurikaMkIII'

class azurelane():
    def __init__(self):
        self.aldict = {'gun_BB': '전함포', 'gun_CA': '중순양함포', 'gun_CL': '경순양함포', 'gun_DD': '구축함포', 'plane_F': '전투기', 'plane_B': '폭격기'
                    , 'plane_T': '뇌격기', 'plane_W': '수상기', 'Torpedo': '어뢰', 'Flak': '대공포', 'gun_PS': '도이칠란트급 포', 'ETC': '보조장비', 'common': '일반탄'
                    , 'AP': '철갑탄', 'HE': '유탄', 'X': 'Dummy', 'P': '수평형', 'G': '유도형', 'AArad': '대공레이더', 'bulge': '벌지', 'SG_r': 'SG레이더', 'm_lifg': '양탄기'
                    , 'H_rud': '유압 조타', 'Boiler': '개량형 보일러', 'Camo': '미채', 'filter': '연료 필터', 'loader': '장전기', 'gyro': '자이로스코프', 'repair': '응급수리장치'
                    , 'fire_ex': '소화기', 'emblem_b': '비버 엠블렘', 'pearl': '진주의 눈물', 'neko': '고양이 펀치', 'o_torp': '산소 어뢰', 'FC_r': '화기관제 레이더', 'Zulu': 'Z기'
                    , 'Catapult': '캐터펄트', 'P_Fuel': '항공기연료탱크', 'crane': '크레인', 'Torpedo_SS': '잠수함어뢰', 'L': '라이트 아머', 'M': '미디엄 아머', 'H': '헤비 아머'
                    , '0': '불명', '1': '공격스킬', '2': '방어스킬', '3': '지원스킬'}

    async def codeblock(self, text: str):
        '''return text wrapped up in python codeblock for discord'''
        if text == "":
            text = "Empty"
        return f"```python\n{text}\n```"

    async def blueblock(self, text: str):
        '''return text wrapped up in python codeblock for discord'''
        if text == "":
            text = "Empty"
        return f"```ini\n{text}\n```"

    async def shipinfo(self, *args, **kwargs):
        kwargs['target'] = ''.join(kwargs['target'])

        async with aiosqlite.connect(cwd + "\db\EurALDB.db") as db:

            if str(kwargs['target'])[-1] in ['+', '개'] and str(kwargs['target']).isdigit() == False:
                kwargs.update({'target': str(kwargs['target'])[:-1] + '改'})

            cursor = await db.execute(f"SELECT * FROM Ships WHERE REPLACE(name, ' ', '') = REPLACE('{kwargs['target']}', ' ', '') OR no = '{kwargs['target']}' COLLATE NOCASE")
            alships = await cursor.fetchall()
            alwd = kwargs['target']
            cursor2 = await db.execute(f"SELECT * FROM Ships WHERE name like '%{alwd}%' OR nation like '%{alwd}%' OR illust like '%{alwd}%' OR voiceover like '%{alwd}%' OR etc like '%{alwd}%' OR class like '%{alwd}%' OR tag like '%{alwd}%'")
            matches = await cursor2.fetchall()

            if len(alships) == 0 and len(matches) >= 1:
                selections = ""
                for i, j in enumerate(matches):
                    selections += f"[{str(i+1)}] [{j[5]}][{str('★' * int(j[3]))}{j[2]}] {j[4]}\n"
                em = discord.Embed(description = await self.codeblock(selections), colour=0x221277)
                em.set_author(name = f"그건 못 찾았지만 비슷한 애들을 찾아봤어. 몇번을 원해?", icon_url="https://cdn.discordapp.com/attachments/296519249134878720/369393631129239553/lusty2.png")
                em.set_footer(text = '숫자만(1번을 원할 경우 1) 입력해.')
                return em, 1, list(map(lambda x: x[0], matches))

            elif len(alships) > 0:
                if len(alships) > 1:
                    albase = alships
                    selections = ""
                    for i, j in enumerate(albase):
                        selections += f"[{str(i+1)}] [{j[5]}][{str('★' * int(j[3]))}{j[2]}] {j[4]}\n"
                    em = discord.Embed(description = await self.codeblock(selections), colour=0x221277)
                    em.set_author(name = '같은 이름의 캐릭터가 여럿 발견되었어. 몇번을 원해?' , icon_url='https://cdn.discordapp.com/attachments/296519249134878720/369393631129239553/lusty2.png')
                    em.set_footer(text = '숫자만 (1번을 원할 경우 1) 입력해.')
                    return em, 1, list(map(lambda x: x[0], albase))

                else:
                    albase = alships[0]

                    if albase[14] == None or albase[14] == '':
                        cvtemp = '읍읍이'
                    else:
                        cvtemp = albase[14]

                    if albase[13] == None or albase[13] == '':
                        iltemp = '미상'
                    else:
                        iltemp = albase[13]

                    em = discord.Embed(colour=0x221277)
                    em.set_author(name = f"[{str(albase[0])}] {albase[4]} (CV. {cvtemp}, ILL. {iltemp})", icon_url='https://cdn.discordapp.com/attachments/296519249134878720/369393631129239553/lusty2.png')

                    alrat = albase[9].split('/')
                    altemp = ''
                    for h,i in enumerate(albase[6:9]):
                        altemp += '['
                        if '/' in i:
                            for j,n in enumerate(i.split('/')):
                                altemp += self.aldict[n]
                                if j+1 != len(i.split('/')):
                                    altemp += '/'
                        else:
                            altemp += self.aldict[i]
                        altemp += f" * {alrat[h]}%]"
                    altemp += f"\n[{self.aldict[albase[10]]}]"
                    em.add_field(name = f"[{albase[5]}][{str('★' * int(albase[3]))}{albase[2]}]", value = altemp)
                    cursor = await db.execute(f"SELECT * FROM Drops WHERE shipdrop like '%{albase[0]}%' COLLATE NOCASE")
                    aldrops = await cursor.fetchall()

                    altemp = ''
                    for m in aldrops:
                        if str(albase[0]) in m[2].split('/'):
                            altemp += f"[{m[1]}]"
                        else:
                            pass
                    if altemp == '' or not altemp:
                        altemp = '입수 불가'
                    if albase[16] != None and albase[16] != '0':
                        em.add_field(name = '입수', value = albase[14])
                    else:
                        if albase[15] != None and albase[15] != 0:
                            em.add_field(name = '건조시간 - [대형]' + albase[1], value = altemp)
                        else:
                            if albase[1] == '0:00':
                                altemp2 = '불가'
                            else:
                                altemp2 = albase[1]
                            em.add_field(name = '건조시간 - ' + altemp2, value = altemp)
                    em.add_field(name="뭐 넣을지", value="아직 결정 못함")
                    altemp=''
                    res_skill = ""
                    for k,l in enumerate(albase[11].split('/')):
                        cursor = await db.execute(f"SELECT * FROM Skill WHERE id='{l}' COLLATE NOCASE")
                        tgt = await cursor.fetchone()
                        res_skill += f"[{str(k+1)}] **{tgt[1]}** [{self.aldict[str(tgt[2])]}]\n{tgt[4]}\n\n"
                    em.add_field(name="**SKILL**", value=res_skill)

                    if albase[12] != None and albase[12] != '0':
                        em.set_image(url=albase[12])

                    cursor = await db.execute(f"SELECT * FROM Ships WHERE name='{kwargs['target']} 改' COLLATE NOCASE or nick like '%{kwargs['target']}%' COLLATE NOCASE")
                    kai_exist = await cursor.fetchone()
                    if kai_exist:
                        em.set_footer(text = kwargs['target'] + '의 개장 버전이 존재합니다. 이름 뒤에 改, +, 2 혹은 개 를 추가해서 검색해보세요.'
                            , icon_url='https://cdn.discordapp.com/attachments/296519249134878720/369393631129239553/lusty2.png')
                    return em, 0

            else:
                em = discord.Embed(description=f"{kwargs['target']}에 관련된 배는 뭔지 모르겠네요.\n개장은 이름 뒤에 2, +, 改, 혹은 개를 붙이는걸로 확인할 수 있어요.\n오탈자의 경우가 있을 수 있으니 =벽람 검색 을 활용해보는 것도 방법.", colour=0xB5002B)
                em.set_author(name = 'Error!' , icon_url='https://cdn.discordapp.com/attachments/296519249134878720/369393631129239553/lusty2.png')
                return em, 0


    async def search(self, alwd):
        alwd = "".join(alwd)
        async with aiosqlite.connect(cwd + "\db\EurALDB.db") as db:
            cursor = await db.execute(f"SELECT * FROM Ships WHERE name like '%{alwd}%' OR nation like '%{alwd}%' OR illust like '%{alwd}%' OR voiceover like '%{alwd}%' OR etc like '%{alwd}%' OR class like '%{alwd}%' OR tag like '%{alwd}%'")
            matches = await cursor.fetchall()
            if len(matches) > 0:
                res = ''

                for i in matches:
                    no_stars = '★' * i[3]
                    res += f"[{no_stars}{i[2]}] {i[4]}\n"

                em = discord.Embed(description = await self.blueblock(res), colour=0x221277)
                em.set_author(name = f"{alwd} 검색 결과야.", icon_url='https://pbs.twimg.com/profile_images/864408527640514560/i-1Y1zSK_400x400.jpg')
                em.set_footer(text = f"{len(matches)}명 발견되었어.")

            else:
                em = discord.Embed(title=f'{alwd}(으)로 검색해서 나온 것이 하나도 없는걸.', colour=0xB5002B)

            return em

    async def update():
        async with aiosqlite.connect(cwd + "\db\EurALDB.db") as db:
            SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
            store = file.Storage('/EurikaMkIII/tokens/token.json')
            creds = store.get()

            if not creds or creds.invalid:
                flow = gclient.flow_from_clientsecrets('/EurikaMkIII/tokens/credentials.json', SCOPES)
                creds = tools.run_flow(flow, store)

            service = build('sheets', 'v4', http=creds.authorize(Http()))

            #service = build('sheets', 'v4', developerKey='AIzaSyA4EmI2jcPp-L3lOAHmIGrsnFFiQkZUhiI')

            # Call the Sheets API
            SPREADSHEET_ID = '1b6WAd7kNQ7zkeUu9vZdSVsWOt2KItLUgvYJqzDREDUw'
            for ENTRY, RANGE_NAME in enumerate(['Update_Ship!A2:P500', 'Update_Skill!A2:E500']):
                result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID,
                                                            range=RANGE_NAME).execute()
                values = result.get('values', [])

                if not values:
                    pass
                else:
                    for row in values:
                        if len(row) >= 2:
                            if row[1] != '':
                                if ENTRY == 0:

                                    await db.execute("INSERT OR REPLACE INTO Ships (no, time, class, rarity, name, " \
                                                   + "nation, slot1, slot2, slot3, adjratio, armor, skill, imglink, " \
                                                   + "illust, voiceover, tag) VALUES (?, ?, ?, ?, ?, ?," \
                                                   + "?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (int(row[0]), row[1],
                                                   row[2], int(row[3]), row[4], row[5], row[6], row[7], row[8], row[9],
                                                   row[10], row[11], row[12], row[13], row[14], ''))

                                else:
                                    await db.execute("INSERT OR REPLACE INTO Skill (id, name, category, maxlv, desc) " \
                                                   + "VALUES (?, ?, ?, ?, ?)", (int(row[0]), row[1], int(row[2]), int(row[3]), row[4]))

                    #Set up the size of area that will be deleted
                    if ENTRY == 0:
                        PURGE_WIDTH = 16
                    else:
                        PURGE_WIDTH = 5

                    #Delete current entries
                    values = [[""]*PURGE_WIDTH]*499
                    body = { 'values': values }

                    result = service.spreadsheets().values().update(spreadsheetId=SPREADSHEET_ID,
                                                range=RANGE_NAME, valueInputOption='RAW',
                                                body=body).execute()

            await db.commit()
