'''
point management
'''
import sys
import aiosqlite
import aiohttp
import requests
import time
import discord
import math
import random
import datetime
from io import BytesIO
from PIL import Image
from basics import codeblock

from basics import rand_name_gen

cwd = r'C:\EurikaMkIII'

class sp():
    async def chklast(*args, **kwargs):
        async with aiosqlite.connect(cwd + '\db\EurDB.db') as db:
            async with db.execute("SELECT * FROM SHUPoint WHERE id='"+str(kwargs['user'])+"' COLLATE NOCASE") as cursor:
                curind = await cursor.fetchone()
                if not curind:
                    return 0
                else:
                    return 0 if curind[4] == time.strftime('%Y-%m-%d') else True

    async def incpoint(*args, **kwargs):
        async with aiosqlite.connect(cwd + '\db\EurDB.db') as db:
            async with db.execute("SELECT * FROM SHUPoint WHERE id={} COLLATE NOCASE".format(str(kwargs['user']))) as cursor:
                curind = await cursor.fetchone()
                if await sp.chklast(user=kwargs['user']) == 0 and kwargs['log'] != 'SHUCMD':
                    return 0
                else:
                    await db.execute("UPDATE SHUPoint SET pt='{}', log='{}', last_login='{}' Where id='{}' COLLATE NOCASE".format(curind[1] + int(kwargs['amnt']), datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + ' ' + kwargs['log'] + str(kwargs['amnt']) + ', ' + curind[2], datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'), str(kwargs['user'])))
                    await db.commit()
                    return 1

    async def inceverypoint(*args, **kwargs):
        async with aiosqlite.connect(cwd + '\db\EurDB.db') as db:
            await db.execute("UPDATE SHUPoint SET pt= pt + {}".format(kwargs['amnt']))

        return

    async def showpoint(*args, **kwargs):
        async with aiosqlite.connect(cwd + '\db\EurDB.db') as db:
            async with db.execute("SELECT * FROM SHUPoint WHERE id={} COLLATE NOCASE".format(str(kwargs['author'].id))) as cursor:
                curind = await cursor.fetchone()
                if not curind:
                    await sp.register_account(str(kwargs['author'].id))
                    em = discord.Embed(title='{}의 SHUPoint 시스템 등록 절차가 완료되었습니다.'.format(str(kwargs['author'].display_name)), colour=0x07ECBA)
                    return em, 0
                else:
                    cursor = await db.execute("SELECT * FROM SHUPoint WHERE id='"+str(kwargs['author'].id)+"' COLLATE NOCASE")
                    sptemp = await cursor.fetchone()
                    em = discord.Embed(title="{} (ID: {})".format(kwargs['author'].name, kwargs['author'].id)
                                        , description='```python\n현재 보유 슈포인트: {:,}pt```'.format(sptemp[1])
                                        , colour=0x07ECBA)
                    em.set_footer(text='포인트의 이용은 별도 커맨드, =상점 을 이용해주시기 바랍니다.')
                    return em, 0

    async def showpreregimage(*args, **kwargs):
        async with aiosqlite.connect(cwd + '\db\EurDB.db') as db:
            async with db.execute("SELECT * FROM SHUPoint WHERE id={} COLLATE NOCASE".format(str(kwargs['author'].id))) as cursor:
                curind = await cursor.fetchone()

                if not curind:
                    await db.execute("INSERT INTO SHUPoint (id, pt,log,created_date) VALUES ('"+str(kwargs['author'].id)+"', 0, '', '"+datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')+"')")
                    await db.commit()
                    em = discord.Embed(title=kwargs['author'].name + '의 SHUPoint 시스템 등록 절차가 완료되었습니다.', colour=0x07ECBA)
                    db.close()
                    return em, 0

                else:
                    res = ''
                    cursor = await db.execute("SELECT * FROM SImage WHERE registrator = {}".format(kwargs['author'].id))
                    reg = await cursor.fetchall()

                    for i in reg:
                        res += i[1] + ' '

                    em = discord.Embed(title="{}이(가) 등록한 짤 리스트".format(kwargs['author'])
                                        , description=await codeblock(res), colour=0x07ECBA)
                    em.set_footer(text='짤의 추가/삭제는 =상점 을 이용하시기 바랍니다.')

                    return em, 0

    async def showrank(client):
        async with aiosqlite.connect(cwd + '\db\EurDB.db') as db:
            async with db.execute("SELECT * FROM SHUPoint ORDER BY pt DESC LIMIT 15") as cursor:
                curdata = await cursor.fetchall()
                res = ''
                for i in curdata:
                    ranktgt = client.get_guild(88844446929547264).get_member(i[0]).name
                    if ranktgt != None:
                        res += "{:<4} : {} {}".format(ranktgt, '{:,}', "\n").format(i[1])
                    else:
                        res += "{:<4} : {} {}".format(str('이타치'), '{:,}', "\n").format(i[1])

                spem = discord.Embed(title='현 시점의 SHU포인트 보유자 상위 리스트입니다.'
                                            , description=await codeblock(res), colour=0x07ECBA)

                return spem

    async def showhrank(client):
        async with aiosqlite.connect(cwd + '\db\EurDB.db') as db:
            async with db.execute("SELECT * FROM SHUPoint ORDER BY hillarystreak DESC LIMIT 10") as cursor:
                curdata = await cursor.fetchall()
                res = ''
                for i in curdata:
                    sptemp = client.get_guild(88844446929547264).get_member(i[0]).name
                    res += "{:<4} : {} {}".format(str(sptemp), '{:,}', "\n").format(i[5])
                spem = discord.Embed(title='현 시점에서 가장 운이 없는 놈 순위입니다.'
                                    , description=await codeblock(res), colour=0x07ECBA)
                spem.set_footer(text = '역대 랭킹은 =힐러리전당 커맨드를 이용하시기 바랍니다.')

                return spem

    async def showhlegend(client):
        async with aiosqlite.connect(cwd + '\db\EurDB.db') as db:
            async with db.execute("SELECT * FROM SHUPoint ORDER BY hillariest DESC LIMIT 10") as cursor:
                curdata = await cursor.fetchall()
                res = ''
                for i in curdata:
                    if i[7] != None:
                        sptemp = client.get_guild(88844446929547264).get_member(i[0]).name
                        res += "{:<4} : {} {} {}".format(str(sptemp), '{:,}', '[LAST: ' + i[7] + ']',"\n").format(i[6])
                spem = discord.Embed(title='역대 가장 운이 없던 놈 순위입니다.'
                                    , description=await codeblock(res), colour=0x07ECBA)
                return spem

    async def register_account(id_:str):
        async with aiosqlite.connect(cwd + '\db\EurDB.db') as db:
            await db.execute("INSERT INTO SHUPoint (id, pt,log,created_date) VALUES ('{}', 0, '', '{}')".format(id_, datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')))
            await db.commit()

    async def regcom(self, client, *args, **kwargs):

        embed_nofund = discord.Embed(title="{}, [키움]이시네요 ㅅㄱ".format(kwargs['author'].nick), colour=0xd4eff6)
        embed_cancel = discord.Embed(title="{}, 취소되었습니다.".format(kwargs['author'].nick), colour=0xd4eff6)

        async with aiosqlite.connect(cwd + '\db\EurDB.db') as db:
            async with db.execute("SELECT COUNT(*) FROM SImage WHERE registrator = {}".format(kwargs['author'].id)) as cursor:
                curdata = await cursor.fetchone()
                price = math.floor(13 * math.log(max(curdata[0], 1)) + 1)

            if len(kwargs) == 2:
                cursor = await db.execute("SELECT COUNT(*) FROM SHUPoint WHERE id={} COLLATE NOCASE".format(str(kwargs['author'].id)))
                spcnt = await cursor.fetchone()
                spcnt = spcnt[0]
                if spcnt == 0:
                    await self.register_account(str(kwargs['author'].id))
                    em = discord.Embed(title=kwargs['author'].name + '의 SHUPoint 시스템 등록 절차가 완료되었어요.', colour=0x07ECBA)
                    return em, 0
                else:
                    cursor = await db.execute("SELECT * FROM SHUPoint WHERE id={} COLLATE NOCASE".format(str(kwargs['author'].id)))
                    sptemp = await cursor.fetchone()
                    em = discord.Embed(title=f"{kwargs['author'].name} (ID: {kwargs['author'].id})"
                                                       , description='등록일자: {}\n```python\n현재 보유 슈포인트: {:,}pt```'.format(sptemp[3], sptemp[1]), colour=0x07ECBA)
                    em.add_field(name = '**[옵션 넘버][소모되는 포인트] 각 옵션 설명 및 명칭 **', value = '선택가능한 각 옵션의 설명입니다.')
                    em.add_field(name = f'[1][{price}pt] 신규 짤 등록 - 현재까지 추가한 짤: {curdata[0]}개'
                                , value = '-로 시작하는 짤 명령어목록에 신규 명령어를 추가할 수 있습니다. 가격은 기존 등록짤 수에따라 상승합니다.')
                    em.add_field(name = '[2][5pt] 기존 짤 삭제', value = "자신이 등록한 짤 하나를 삭제할 수 있습니다.")
                    em.add_field(name = '[3][100pt] 숏 소드 신규 발급', value = '테러방지 수단을 입수할 수 있습니다.')
                    em.add_field(name = '[4][1,000pt] 셀펠매 탈출권', value = '셀프펠라매니아 상태의 남은 기간에 상관 없이 즉시 벗어날 수 있습니다.')
                    em.add_field(name = '[5][1,000pt] 다른 마을로의 이주', value = '정해진 색상 내에서 유저 한 명의 색을 바꿀 수 있습니다.')
                    em.add_field(name = '[6][20,000pt] 신규 마을 생성권', value = '새로운 마을사람 등급을 생성합니다. 생성과 동시에 해당 마을으로 이주하게 됩니다.')
                    em.add_field(name = '[7] 관두자', value = '그래')
                    em.set_footer(text='몇 번으로 할까? 숫자만 입력하세요. 60초가 주어집니다.')
                    return em, 1

            else:
                cursor = await db.execute("SELECT * FROM SHUPoint WHERE id={} COLLATE NOCASE".format(str(kwargs['author'].id)))
                sptemp = await cursor.fetchone()
                if kwargs['selection'] == '1':
                    if sptemp[1] >= price:
                        if kwargs['phase'] == '0':
                            em = discord.Embed(title=f"{kwargs['author']}, 새로 추가할 커맨드의 이름과 링크를 설정하세요."
                            , description='지금은 -는 붙이지 말도록 하세요. 명령어의 최대 길이는 10자, 파일 확장자는 jpg, gif, png만 허용됩니다.\n[예시] 피카츄 http://gobo.ziding/test.gif'
                            , colour=0xd4eff6)
                            em.set_footer(text=' 취소하려면 아무거나 치도록 하세요.')
                            return em, 2

                        elif kwargs['phase'] == '1':
                            cursor = await db.execute("SELECT * FROM SImage WHERE initializer='{}' COLLATE NOCASE".format(kwargs['detail'].split()[0].replace('-', '')))
                            sigtemp = await cursor.fetchone()
                            if len(kwargs['detail'].split()) != 2:
                                em = discord.Embed(title="{}, 이상한걸 넣지 말아주세요.".format(kwargs['author'].nick), colour=0xd4eff6)
                            elif len(kwargs['detail'].split()[0]) > 10:
                                em = discord.Embed(title="{}, 명령어가 너무 깁니다. 10자 이하로 줄여서 다시 해주세요.".format(kwargs['author'].nick), colour=0xd4eff6)
                            #elif (len(kwargs['detail'].split()[0]) == 1) and (str(kwargs['detail'].split()[0]).isalpha() == True):
                                #em = discord.Embed(title="{} 왜구련아".format(kwargs['author'].nick), colour=0xd4eff6)
                            elif sigtemp:
                                em = discord.Embed(title="{}, 이미 그 이름으로 등록된 커맨드가 존재해요.".format(kwargs['author'].nick)
                                                , description='~~[-리스트] 를 입력해 현재 등록된 리스트를 확인한 후~~삭제됨, 처음부터 다시 시도해주세요.', colour=0xd4eff6)
                            else:
                                em = await sp.addsig(author=kwargs['author'], detail=kwargs['detail'], price=price)
                            return em, 0

                        else:
                            return embed_cancel, 0

                    else:
                        return embed_nofund, 0

                elif kwargs['selection'] == '2':
                    if sptemp[1] >= 5:
                        if kwargs['phase'] == '0':
                            cursor = await db.execute("SELECT * FROM SImage WHERE registrator ='{}'".format(kwargs['author'].id))
                            reg = await cursor.fetchall()
                            prereg_list = await codeblock(' '.join(map(lambda x: x[1], reg)))
                            em = discord.Embed(title="{}, 삭제할 짤의 이름을 말하세요".format(kwargs['author'].nick)
                                                , description='당신이 지금까지 등록한 리스트입니다.\n{}\n당연하지만 자신이 등록한 것만 가능하니까 주의하세요\n[예시] 캬루10'.format(prereg_list)
                                                , colour=0xd4eff6)
                            em.set_footer(text='취소하려면 "취소"를 담아 아무거나 입력하세요.')
                            return em, 'sel2p2'

                        elif kwargs['phase'] == '1':
                            cursor = await db.execute("SELECT * FROM SImage WHERE initializer='{}' COLLATE NOCASE".format(kwargs['detail'].split()[0].replace('-', '')))
                            sigtemp = await cursor.fetchone()
                            if len(kwargs['detail'].split()) != 1:
                                em = discord.Embed(title='{}, 입력한 내용에 문제가 있어 취소되었어요.'.format(kwargs['author'].nick), colour=0xd4eff6)
                            elif not sigtemp:
                                em = discord.Embed(title='{}, 확인 결과 그 이름으로 등록된 커맨드가 없네요.'.format(kwargs['author'].nick)
                                                    , description='~~[-리스트] 를 입력해 현재 등록된 리스트를 확인한 후~~삭제됨, 처음부터 다시 시도해주세요.', colour=0xd4eff6)
                            elif sigtemp[4] != str(kwargs['author'].id):
                                em = discord.Embed(title='{}, 당신이 등록한 짤이 아닌 것 같네요. 재확인해주세요.'.format(kwargs['author'].nick), colour=0xd4eff6)
                            else:
                                em = await self.delsig(author=kwargs['author'], detail=kwargs['detail'])
                            return em, 0

                        else:
                            return embed_cancel, 0
                    else:
                        return embed_nofund, 0

                elif kwargs['selection'] == '3':
                    if sptemp[1] >= 100:
                        em = await self.ssword(client, author=kwargs['author'])
                        return em, 0
                    else:
                        return embed_nofund, 0

                elif kwargs['selection'] == '4':
                    if sptemp[1] >= 1000:
                        em = await self.escape(client, author=kwargs['author'])
                        return em, 0
                    else:
                        return embed_nofund, 0

                elif kwargs['selection'] == '5':
                    color_max = 18
                    if sptemp[1] >= 1000:
                        if kwargs['phase'] == '0':
                            em = discord.Embed(title='{}, 원하는 색상을 고르세요. 이하의 선택지 외에는 선택 불가능하며 환불은 택도 없으니 신중하게 하세요'.format(kwargs['author'].nick)
                                                , colour=0x07ECBA)
                            em.set_image(url='https://cdn.discordapp.com/attachments/415417437916495872/454124723140296719/Untitled-3.png')
                            em.set_footer(text='취소하려면 선택지가 아닌 아무거나 입력하세요.')
                            return em, 'immigrate'

                        elif kwargs['phase'].isdigit() and int(kwargs['phase']) == 1 and int(kwargs['detail']) in range(1,19):
                            em = discord.Embed(title='{}, 대상의 아이디를 입력하시기 바랍니다.'.format(kwargs['author'].nick)
                                            , description='아이디는 설정에서 개발자 모드를 활성화 시킨 후\n대상을 우클릭 시 나오는 드랍다운 메뉴에서 복사할 수 있습니다.\n\n당신의 코드는 {} 입니다.'.format(kwargs['author'].id)
                                            , colour=0x07ECBA)
                            return em, 'immigrate', str(kwargs['detail'])

                        elif kwargs['phase'].isdigit() and int(kwargs['phase']) == 2 and int(kwargs['detail']) in range(1,color_max+1):
                            em = await self.immigrate(client, author=kwargs['author'], target=kwargs['target'], choice=kwargs['detail'])
                            return em, 0
                        else:
                            return embed_cancel, 0
                    else:
                        return embed_nofund, 0

                elif kwargs['selection'] == '6':
                    if sptemp[1] >= 20000:
                        em = discord.Embed(title="{}, 축하해요 관리자를 부르세요!", colour=0x07ECBA)
                        em.set_image(url='https://cdn.discordapp.com/attachments/296519249134878720/397222940292284417/Untitled-2.jpg')
                        return em, 0
                    else:
                        return embed_nofund, 0

                elif kwargs['selection'] == '7':
                    em = discord.Embed(title='구랭.', colour=0x07ECBA)
                    return em, 0

                else:
                    return embed_cancel, 0

    async def ssword(self, client, *args, **kwargs):

        #print(kwargs['author'].roles)
        has_sword = any(map(lambda x: x.id == 295021019851128842, kwargs['author'].roles))

        if not has_sword:
            async with aiosqlite.connect(cwd + '\db\EurDB.db') as db:
                async with db.execute(f"SELECT * FROM SHUPoint WHERE id='{kwargs['author'].id}' COLLATE NOCASE") as cursor:
                    curind = await cursor.fetchone()
                    await db.execute("UPDATE SHUPoint SET pt=?, log=? Where id=? COLLATE NOCASE", (curind[1] - 100, datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + ' SSWORD-100,' + curind[2], kwargs['author'].id))
                    await db.commit()
                    em = discord.Embed(title=f"{kwargs['author'].nick} 은(는) 100pt를 사용해 날카로운 +1 숏 소드를 얻었다!"
                                        , description='\n\n크큭... 선이 보인다...\n\n```python\n======================================================\n                         RULES\n======================================================\n1. 숏 소드를 배포하는 것은 자유입니다.(예외: 캐부, 셀펠매)\n2. 흰색 닉과 자신 외에는 사체로 만들어선 안됩니다.\n3. 신규 등급을 생성해서는 안됩니다.\n4. 사체를 소생시켜서는 안됩니다. 시체는 잘 묻어놔야죠.\n5. 자신 혹은 타인을 사체를 제외한 타 마을으로 옮기거나 타인의 숏 소드를 제외한 등급을 삭제해선 안됩니다.```', colour=0x07ECBA)
                    em.set_footer(text='즐거운 소드마스터 라이프 되시기 바랍니다.')
                    await kwargs['author'].add_roles(client.get_guild(88844446929547264).get_role(295021019851128842))
        else:
            em = discord.Embed(title=f"{kwargs['author'].nick}, 넌 이미 숏 소드가 있는데?",colour=0xd4eff6)
        return em

    async def escape(self, client, *args, **kwargs):
        has_fella = any(map(lambda x: x.id == 88882661761773568, kwargs['author'].roles))
        if has_fella:
            async with aiosqlite.connect(cwd + '\db\EurDB.db') as db:
                async with db.execute(f"SELECT * FROM SHUPoint WHERE id='{kwargs['author'].id}' COLLATE NOCASE") as cursor:
                    curind = await cursor.fetchone()
                    await db.execute("UPDATE SHUPoint SET pt=?, log=? Where id=? COLLATE NOCASE", (curind[1] - 500, datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + ' RSFELM-500,' + curind[2], kwargs['author'].id))
                    await db.commit()
                    roles = []
                    roles.append(client.get_guild(88844446929547264).get_role(104124605085536256))
                    await kwargs['author'].edit(roles=roles)
            em = discord.Embed(title=f"{kwargs['author'].nick}은(는) 셀펠매 상태에서 벗어났다!", colour=0x07ECBA)
            em.set_footer(text='즐거운 자유인 라이프 되시기 바랍니다. 얼마나 오래갈지는 모르겠지만요.')
        else:
            em = discord.Embed(title=f"{kwargs['author'].nick}, 셀펠매 상태일때만 쓸 수 있어요.",colour=0xd4eff6)
        return em

    async def immigrate(self, client, *args, **kwargs):
        spc_roles = {"FlyingYSM": 562373620609974272}
        prv_roles = kwargs['author'].roles
        immschk = 0
        immwchk = 0

        for i in kwargs['target'].roles:
            if '295021019851128842' == i.id:
                immschk += 1
            if '319123448267931648' == i.id:
                immwchk += 1

        immsel = ''

        immsel_list = ['104124605085536256', '192692234393485313', '192695457086963712', '344768679575289857', '104124610450038784', '248742817021558784', '398068493502644234', '398068495507783681',
                       '398068486183845900', '398068483562405891', '344713031080607744', '398071183758721035', '451101759608455168', '450088070633488394', '450087460131831810', '450088471508418591',
                       '454119840752336896', '450089018831405067']

        if int(kwargs['choice']) in range(1,19):
            immsel = immsel_list[int(kwargs['choice']) - 1]
        else:
            em = discord.Embed(title=kwargs['author'].name + ', 너같이 왜구같은 번호야',colour=0xd4eff6)
            return em

        if immschk != 0:
            await client.replace_roles(kwargs['target'], discord.utils.get(client.get_server(str(88844446929547264)).roles, id=immsel), discord.utils.get(client.get_server(str(88844446929547264)).roles, id='295021019851128842'))
        elif immwchk != 0:
            await client.replace_roles(kwargs['target'], discord.utils.get(client.get_server(str(88844446929547264)).roles, id=immsel), discord.utils.get(client.get_server(str(88844446929547264)).roles, id='319123448267931648'))
        else:
            await client.replace_roles(kwargs['target'], discord.utils.get(client.get_server(str(88844446929547264)).roles, id=immsel))

        async with aiosqlite.connect(cwd + '\db\EurDB.db') as db:
            async with db.execute(f"SELECT * FROM SHUPoint WHERE id='{kwargs['author'].id}' COLLATE NOCASE") as cursor:
                curind = await cursor.fetchone()
                await db.execute("UPDATE SHUPoint SET pt=?, log=? Where id=? COLLATE NOCASE", (curind[1] - 1000, datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + ' IMMGRT-1000,' + curind[2], kwargs['author'].id))
                await db.commit()

        em = discord.Embed(title=f"{kwargs['target'].display_name}, 소속이 변경되었습니다.", colour=0x07ECBA)
        em.set_footer(text='변심으로 인한 변경은 불가능합니다.')
        return em

    async def geths(*args):
        async with aiosqlite.connect(cwd + '\db\EurDB.db') as db:
            async with db.execute("SELECT * FROM SHUPoint WHERE id={} COLLATE NOCASE".format(args[0])) as cursor:
                curdata = await cursor.fetchone()

        return curdata[5] if curdata[5] else 0

    async def updatehs(*args):
        async with aiosqlite.connect(cwd + '\db\EurDB.db') as db:
            async with db.execute("SELECT hillariest FROM SHUPoint WHERE id={} COLLATE NOCASE".format(args[0])) as cursor:
                curdata = await cursor.fetchone()
                hill_exist = curdata[0]

                if hill_exist:
                    if hill_exist < args[1]:
                        await db.execute('UPDATE SHUPoint SET hillariest=?, hillariest_at=? WHERE id=? COLLATE NOCASE', (str(args[1]), datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), args[0]))
                elif args[1] > 0:
                    await db.execute('UPDATE SHUPoint SET hillariest=?, hillariest_at=? WHERE id=? COLLATE NOCASE', (str(args[1]), datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), args[0]))

                await db.execute('UPDATE SHUPoint SET hillarystreak=? Where id=? COLLATE NOCASE', (str(args[1]), args[0]))
                await db.commit()
        return

    async def deleteroles(*args, **kwargs):
        await client.replace_roles(kwargs['author'], discord.utils.get(client.get_server(str(88844446929547264)).roles, id=str(88844446929547264)))

    async def addsig(*args, **kwargs):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(kwargs['detail'].split()[1]) as resp:
                    sigraw = await resp.read()
                    sigres = Image.open(BytesIO(sigraw))
                    signame = await rand_name_gen(12)
                    sigcmd = kwargs['detail'].split()[0].replace('-', '')
                    sigdest = "C:\EurikaMkIII\image\\" + signame + "." + sigres.format.lower()
                    if sigres.format.lower() == 'gif':
                        r = requests.get(kwargs['detail'].split()[1], headers={'User-Agent': 'Mozilla/5.0'})
                        with open(sigdest, 'wb') as siggif:
                            siggif.write(r.content)
                    else:
                        sigres.save(sigdest)

            async with aiosqlite.connect(cwd + '\db\EurDB.db') as db:
                async with db.execute("SELECT * FROM SHUPoint WHERE id={} COLLATE NOCASE".format(str(kwargs['author'].id))) as cursor:
                    curind = await cursor.fetchone()
                    await db.execute("INSERT INTO SImage (initializer, loc, registrator, cache) VALUES ('{}', '{}', '{}', '{}')".format(sigcmd, signame + "." + sigres.format.lower(), kwargs['author'].id, kwargs['detail'].split()[1]))
                    await db.execute("UPDATE SHUPoint SET pt=?, log=? Where id=? COLLATE NOCASE"
                                    , (curind[1] - kwargs['price'], datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + ' SIGADD-' + str(kwargs['price']) + ', ' + curind[2], kwargs['author'].id))
                    em = discord.Embed(title='{}이 신규 커맨드 -{}을(를) 등록했습니다.'.format(kwargs['author'].name, sigcmd)
                                        , description='{}pt가 소모됩니다.'.format(str(kwargs['price'])), colour=0x07ECBA)
                    await db.commit()

        except:
            print("ADDSIG Error:", sys.exc_info())
            em = discord.Embed(title='{}, 에러가 발생했습니다.'.format(kwargs['author'].name)
                                , colour=0xd4eff6)
        return em

    async def delsig(*args, **kwargs):
        try:
            async with aiosqlite.connect(cwd + '\db\EurDB.db') as db:
                async with db.execute("SELECT * FROM SHUPoint WHERE id={} COLLATE NOCASE".format(str(kwargs['author'].id))) as cursor:
                    curind = await cursor.fetchone()
                    await db.execute("DELETE FROM SImage WHERE initializer ='{}' COLLATE NOCASE".format(kwargs['detail']))
                    await db.execute("UPDATE SHUPoint SET pt=?, log=? Where id=? COLLATE NOCASE", (curind[1] - 5, datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + ' SIGDEL-05,' + curind[2], kwargs['author'].id))
                    em = discord.Embed(title='{}이 신규 커맨드 -{}을(를) 삭제했습니다.'.format(kwargs['author'].name, str(kwargs['detail'])), description='5pt가 소모됩니다.', colour=0x07ECBA)
                    await db.commit()
        except:
            print("DELSIG Error:", sys.exc_info())
            em = discord.Embed(title='{}, 에러가 발생했습니다.'.format(kwargs['author'].name), colour=0xd4eff6)

        return em

    async def fourdollar(cand):
        splpt = random.randint(15,20)
        spres = await sp.incpoint(user=cand.id, amnt=splpt, log='LOGPOI')
        if spres == 1:
            em = discord.Embed(title=f'오케이, 땡큐! 오케이! {str(splpt)}딸라!!'
                                , description=f'대충 타협한 결과에 따라 {cand.display_name}은(는) {str(splpt)}만큼의 슈포인트를 얻었다!'
                                , colour=0x07ECBA)
            em.set_image(url='https://cdn.discordapp.com/attachments/415417437916495872/447864754996903947/4dl.png')
        elif spres == 0:
            em = discord.Embed(title='이보게 오늘은 이미 임금을 받았구려. 내일 다시 오시게.'
                                ,description = f"{cand.display_name}는 묵묵히 발길을 뒤로 했다...", colour=0x07ECBA)
            #em.set_image(url='https://cdn.discordapp.com/attachments/415417437916495872/450813280357711882/fail-sm.png')
            em.set_image(url='https://cdn.discordapp.com/attachments/296519249134878720/399892492302155786/ef86189b9e2095706f58ffd9b8981bfd.jpg')
        elif spres == -1:
            em = discord.Embed(title='미안하네만 자네의 이름을 찾을 수가 없네. =포인트를 치고 다시 오게나'
                                ,description = f"장교는 쓸쓸히 떠나가는 {cand.display_name}의 등을 묵묵히 배웅했다...", colour=0x07ECBA)
            em.set_image(url='https://cdn.discordapp.com/attachments/415417437916495872/450813280357711882/fail-sm.png')
        return em
