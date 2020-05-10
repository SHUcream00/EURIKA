'''
point management
'''
import aiosqlite
import time
import discord

class sp():
    def __init__(self, db):
        self.db = db

    async def chklast(*args, **kwargs):
        async with aiosqlite.connect(self.db) as db:
            async with db.execute("SELECT * FROM SHUPoint WHERE id='"+str(kwargs['user'])+"' COLLATE NOCASE") as cursor:
                curind = cursor.fetchone()
                if !curind:
                    return False
                else:
                    return False if curind[4] == time.strftime('%Y-%m-%d %H:%M:%S') else True

    async def incpoint(*args, **kwargs):
        async with aiosqlite.connect(self.db) as db:
            async with db.execute("SELECT * FROM SHUPoint WHERE id='"+str(kwargs['user'])+"' COLLATE NOCASE") as cursor:
                curind = await cursor.fetchone()
                if await sp.chklast(user=kwargs['user']) == 0 and kwargs['log'] != 'SHUCMD':
                    return False
                else:
                    await db.execute("UPDATE SHUPoint SET pt=?, log=?, last_login=? Where id=? COLLATE NOCASE", (curind[1] + int(kwargs['amnt']), datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + ' ' + kwargs['log'] + str(kwargs['amnt']) + ', ' + curind[2], datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d'), str(kwargs['user'])))
                    await db.commit()
                    return True

    async def inceverypoint(*args, **kwargs):
        async with aiosqlite.connect(self.db) as db:
            await db.execute("UPDATE SHUPoint SET pt= pt + {}".format(kwargs['amnt']))

        return

    async def showpoint(*args, **kwargs):
        db = sqlite3.connect(cwd + '\db\EurDB.db')
        cursor = db.cursor()
        if cursor.execute("SELECT COUNT(*) FROM SHUPoint WHERE id='"+str(kwargs['author'].id)+"' COLLATE NOCASE").fetchone()[0] == 0:
            cursor.execute("INSERT INTO SHUPoint (id, pt,log,created_date) VALUES ('"+str(kwargs['author'].id)+"', 0, '', '"+datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')+"')")
            db.commit()
            em = discord.Embed(title=kwargs['author'].name + '의 SHUPoint 시스템 등록 절차가 완료되었습니다.', colour=0x07ECBA)
            db.close()
            return em, 0
        else:
            sptemp = cursor.execute("SELECT * FROM SHUPoint WHERE id='"+str(kwargs['author'].id)+"' COLLATE NOCASE").fetchone()
            em = discord.Embed(title=kwargs['author'].name + "(ID: " + kwargs['author'].id + ")", description='```python\n현재 보유 슈포인트: {:,}pt```'.format(sptemp[1]), colour=0x07ECBA)
            em.set_footer(text='포인트의 이용은 별도 커맨드, [`]을 이용해주시기 바랍니다.')
            return em, 0

    async def showpreregimage(*args, **kwargs):
        db = sqlite3.connect(cwd + '\db\EurDB.db')
        cursor = db.cursor()
        if cursor.execute("SELECT COUNT(*) FROM SHUPoint WHERE id='"+str(kwargs['author'].id)+"' COLLATE NOCASE").fetchone()[0] == 0:
            cursor.execute("INSERT INTO SHUPoint (id, pt,log,created_date) VALUES ('"+str(kwargs['author'].id)+"', 0, '', '"+datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')+"')")
            db.commit()
            em = discord.Embed(title=kwargs['author'].name + '의 SHUPoint 시스템 등록 절차가 완료되었습니다.', colour=0x07ECBA)
            db.close()
            return em, 0
        else:
            prereg_list = '```python\n'
            reg = cursor.execute("SELECT * FROM SImage WHERE registrator = {}".format(kwargs['author'].id)).fetchall()
            for i in reg:
                prereg_list += i[1] + ' '
            prereg_list += '```'

            em = discord.Embed(title="{}이(가) 등록한 짤 리스트".format(kwargs['author']), description=prereg_list, colour=0x07ECBA)
            em.set_footer(text='짤의 추가/삭제는 =상점 을 이용하시기 바랍니다.')
            return em, 0

    async def showrank():
        db = sqlite3.connect(cwd + '\db\EurDB.db')
        cursor = db.cursor()
        splst = cursor.execute("SELECT * FROM SHUPoint ORDER BY pt DESC LIMIT 15").fetchall()
        spres = '```python\n'
        for i in splst:
            ranktgt = discord.utils.get(client.get_server(str(88844446929547264)).members, id=str(i[0]))
            if ranktgt != None:
                spres += "{:<4} : {} {}".format(str(ranktgt.name.strip()), '{:,}', "\n").format(i[1])
            else:
                spres += "{:<4} : {} {}".format(str('이타치'), '{:,}', "\n").format(i[1])
        spres += '```'
        spem = discord.Embed(title='현 시점의 SHU포인트 보유자 상위 리스트입니다.', description=spres, colour=0x07ECBA)
        db.close()
        return spem

    async def showhrank():
        db = sqlite3.connect(cwd + '\db\EurDB.db')
        cursor = db.cursor()
        splst = cursor.execute("SELECT * FROM SHUPoint ORDER BY hillarystreak DESC LIMIT 10").fetchall()
        spres = '```python\n'
        for i in splst:
            sptemp = discord.utils.get(client.get_server(str(88844446929547264)).members, id=str(i[0])).name.strip()
            spres += "{:<4} : {} {}".format(str(sptemp), '{:,}', "\n").format(i[5])
        spres += '```\n역대 랭킹은 =힐러리전당 커맨드를 이용하시기 바랍니다.'
        spem = discord.Embed(title='현 시점에서 가장 운이 없는 놈 순위입니다.', description=spres, colour=0x07ECBA)

        db.close()
        return spem

    async def showhlegend():
        db = sqlite3.connect(cwd + '\db\EurDB.db')
        cursor = db.cursor()
        splst = cursor.execute("SELECT * FROM SHUPoint ORDER BY hillariest DESC LIMIT 10").fetchall()
        spres = '```python\n'
        for i in splst:
            if i[7] != None:
                sptemp = discord.utils.get(client.get_server(str(88844446929547264)).members, id=str(i[0])).name.strip()
                spres += "{:<4} : {} {} {}".format(str(sptemp), '{:,}', '[LAST: ' + i[7] + ']',"\n").format(i[6])
        spres += '```'
        spem = discord.Embed(title='역대 가장 운이 없던 놈 순위입니다.', description=spres, colour=0x07ECBA)
        db.close()
        return spem

    async def regcom(*args, **kwargs):
        db = sqlite3.connect(cwd + '\db\EurDB.db')
        cursor = db.cursor()
        prereg_cnt = cursor.execute("SELECT COUNT(*) FROM SImage WHERE registrator = {}".format(kwargs['author'].id)).fetchone()[0]
        if prereg_cnt == 0:
            prereg_cnt = 1
        price = math.floor(13 * math.log(prereg_cnt) + 1)

        if len(kwargs) == 2:
            spcnt = cursor.execute("SELECT COUNT(*) FROM SHUPoint WHERE id='"+str(kwargs['author'].id)+"' COLLATE NOCASE").fetchone()[0]
            if spcnt == 0:
                cursor.execute("INSERT INTO SHUPoint (id, pt,log,created_date) VALUES ('"+str(kwargs['author'].id)+"', 0, '', '"+datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')+"')")
                db.commit()
                em = discord.Embed(title=kwargs['author'].name + '의 SHUPoint 시스템 등록 절차가 완료되었습니다.', colour=0x07ECBA)
                db.close()
                return em, 0
            else:
                sptemp = cursor.execute("SELECT * FROM SHUPoint WHERE id='"+str(kwargs['author'].id)+"' COLLATE NOCASE").fetchone()


                em = discord.Embed(title=kwargs['author'].name + "(ID: " + kwargs['author'].id + ") 등록일자: " + sptemp[3], description='```python\n현재 보유 슈포인트: {:,}pt```'.format(sptemp[1]), colour=0x07ECBA)
                em.add_field(name = '**[옵션 넘버][소모되는 포인트] 각 옵션 설명 및 명칭 **', value = '선택가능한 각 옵션의 설명입니다.')
                em.add_field(name = '[1][{}pt] 신규 짤 등록 - 현재까지 추가한 짤: {}개'.format(str(price), str(prereg_cnt)), value = '-로 시작하는 짤 명령어목록에 신규 명령어를 추가할 수 있습니다. 가격은 기존 등록짤 수에따라 상승합니다.')
                em.add_field(name = '[2][5pt] 기존 짤 삭제', value = "자신이 등록한 짤 하나를 삭제할 수 있습니다.")
                em.add_field(name = '[3][100pt] 숏 소드 신규 발급', value = '테러방지 수단을 입수할 수 있습니다.')
                em.add_field(name = '[4][500pt] 셀펠매 탈출권', value = '셀프펠라매니아 상태의 남은 기간에 상관 없이 즉시 벗어날 수 있습니다.')
                em.add_field(name = '[5][1,000pt] 다른 마을로의 이주', value = '정해진 색상 내에서 유저 한 명의 색을 바꿀 수 있습니다.')
                em.add_field(name = '[6][20,000pt] 신규 마을 생성권', value = '새로운 마을사람 등급을 생성합니다. 생성과 동시에 해당 마을으로 이주하게 됩니다.')
                em.add_field(name = '[7] 관두자', value = '그래')
                em.set_footer(text='몇 번으로 할까? 숫자만 입력하세요. 60초가 주어집니다.')
                return em, 1

        else:
            sptemp = cursor.execute("SELECT * FROM SHUPoint WHERE id='"+str(kwargs['author'].id)+"' COLLATE NOCASE").fetchone()
            if kwargs['selection'] == '1':
                if sptemp[1] >= price:
                    if kwargs['phase'] == '0':
                        em = discord.Embed(title=kwargs['author'].name + ', 새로 추가할 커맨드의 이름과 링크를 설정하시기 바랍니다.', description='-는 붙이지 말도록 하세요. 명령어의 최대 길이는 한영수불문 10자, 파일 확장자는 jpg, gif, png만 허용됩니다.\n[예시] 테스트 http://gozi.boding/test.gif', colour=0xd4eff6)
                        em.set_footer(text='취소하려면 "취소"를 담아 아무거나 입력하기 바랍니다.')
                        return em, 2
                    elif kwargs['phase'] == '1':
                        sigtemp = cursor.execute("SELECT * FROM SImage WHERE initializer='"+kwargs['detail'].split()[0].replace('-', '')+"' COLLATE NOCASE").fetchone()
                        if len(kwargs['detail'].split()) != 2:
                            em = discord.Embed(title=kwargs['author'].name + ', 입력한 내용에 문제가 있어 취소되었습니다.', colour=0xd4eff6)
                        elif len(kwargs['detail'].split()[0]) > 10:
                            em = discord.Embed(title=kwargs['author'].name + ', 명령어가 너무 깁니다. 10자 이하로 제한해주세요.', colour=0xd4eff6)
                        elif (len(kwargs['detail'].split()[0]) == 1) and (str(kwargs['detail'].split()[0]).isalpha() == True):
                            em = discord.Embed(title=kwargs['author'].name + ' 왜구련아', colour=0xd4eff6)
                        elif sigtemp != None:
                            em = discord.Embed(title=kwargs['author'].name + ', 이미 그 이름으로 등록된 커맨드가 존재합니다.', description='[-리스트] 를 입력해 현재 등록된 리스트를 확인한 후, 처음부터 다시 시도해주세요.', colour=0xd4eff6)
                        else:
                            em = await sp.addsig(cursor, author=kwargs['author'], detail=kwargs['detail'], price=price)
                            db.commit()
                            db.close()
                        return em, 0
                    else:
                        em = discord.Embed(title=kwargs['author'].name + ', 취소되었습니다.', colour=0xd4eff6)
                        return em, 0

                else:
                    em = discord.Embed(title=kwargs['author'].name + '님, [넥센]이시네요 ㅅㄱ', colour=0xd4eff6)
                    return em, 0

            elif kwargs['selection'] == '2':
                if sptemp[1] >= 5:
                    if kwargs['phase'] == '0':
                        prereg_list = '```python\n'
                        reg = cursor.execute("SELECT * FROM SImage WHERE registrator = {}".format(kwargs['author'].id)).fetchall()
                        for i in reg:
                            prereg_list += i[1] + ' '
                        prereg_list += '```'
                        em = discord.Embed(title=kwargs['author'].name + ', 삭제할 짤의 이름을 지정하기 바랍니다', description='당신이 지금까지 등록한 리스트입니다.' + prereg_list + '\n당연하지만 자신이 등록한 것만 가능하니까 주의\n[예시] Oohyyoucandanceyoucanjivehavingthetimeofyourlifeoohseethatgirlwatchthatscenediginthedancingqueen~ ', colour=0xd4eff6)
                        em.set_footer(text='취소하려면 "취소"를 담아 아무거나 입력하기 바랍니다.')
                        return em, 'sel2p2'
                    elif kwargs['phase'] == '1':

                        sigtemp = cursor.execute("SELECT * FROM SImage WHERE initializer='"+kwargs['detail'].split()[0].replace('-', '')+"' COLLATE NOCASE").fetchone()
                        if len(kwargs['detail'].split()) != 1:
                            em = discord.Embed(title=kwargs['author'].name + ', 입력한 내용에 문제가 있어 취소되었습니다.', colour=0xd4eff6)
                        elif sigtemp == None:
                            em = discord.Embed(title=kwargs['author'].name + ', 확인 결과 그 이름으로 등록된 커맨드가 없습니다.', description='[-리스트] 를 입력해 현재 등록된 리스트를 확인한 후, 처음부터 다시 시도해주세요.', colour=0xd4eff6)
                        elif sigtemp[4] != kwargs['author'].id:
                            em = discord.Embed(title=kwargs['author'].name + ', 당신이 등록한 짤이 아닌 것 같습니다. 재확인해주세요.', colour=0xd4eff6)
                        else:
                            em = await sp.delsig(cursor, author=kwargs['author'], detail=kwargs['detail'])
                            db.commit()
                            db.close()
                        return em, 0
                    else:
                        em = discord.Embed(title=kwargs['author'].name + ', 취소되었습니다.', colour=0xd4eff6)
                        return em, 0

                else:
                    em = discord.Embed(title=kwargs['author'].name + '님, [넥센]이시네요 ㅅㄱ', colour=0xd4eff6)
                    return em, 0

            elif kwargs['selection'] == '3':
                if sptemp[1] >= 100:
                    em = await sp.ssword(cursor, author=kwargs['author'])
                    db.commit()
                    db.close()
                    return em, 0
                else:
                    em = discord.Embed(title=kwargs['author'].name + '님, [넥센]이시네요 ㅅㄱ', colour=0xd4eff6)
                    return em, 0

            elif kwargs['selection'] == '4':
                if sptemp[1] >= 500:
                    em = await sp.escape(cursor, author=kwargs['author'])
                    db.commit()
                    db.close()
                    return em, 0
                else:
                    em = discord.Embed(title=kwargs['author'].name + '님, [넥센]이시네요 ㅅㄱ', colour=0xd4eff6)
                    return em, 0

            elif kwargs['selection'] == '5':
                if sptemp[1] >= 1000:
                    if kwargs['phase'] == '0':
                        em = discord.Embed(title=kwargs['author'].name + ', 이주할 색상을 고르시기 바랍니다. 이하의 선택지 외에는 선택 불가능하며 철회는 불가능합니다.', colour=0x07ECBA)
                        em.set_image(url='https://cdn.discordapp.com/attachments/415417437916495872/454124723140296719/Untitled-3.png')
                        em.set_footer(text='취소하려면 선택지가 아닌 아무거나 입력하시기 바랍니다.')
                        return em, 'immigrate'
                    elif kwargs['phase'].isdigit() and int(kwargs['phase']) == 1 and int(kwargs['detail']) in range(1,19):
                        em = discord.Embed(title=kwargs['author'].name + ', 대상의 아이디넘버를 입력하시기 바랍니다.', description='아이디넘버는 설정에서 개발자 모드를 활성화 시킨 후\n대상을 우클릭 시 나오는 드랍다운 메뉴에서 복사할 수 있습니다.\n\n당신의 넘버는 {} 입니다.'.format(
                            kwargs['author'].id), colour=0x07ECBA)
                        return em, 'immigrate', str(kwargs['detail'])
                    elif kwargs['phase'].isdigit() and int(kwargs['phase']) == 2 and int(kwargs['detail']) in range(1,19):
                        em = await sp.immigrate(cursor, author=kwargs['author'], target=kwargs['target'], choice=kwargs['detail'])
                        db.commit()
                        db.close()
                        return em, 0
                    else:
                        em = discord.Embed(title=kwargs['author'].name + ', 취소되었습니다.', colour=0xd4eff6)
                        return em, 0
                else:
                    em = discord.Embed(title=kwargs['author'].name + '님, [넥센]이시네요 ㅅㄱ', colour=0xd4eff6)
                    return em, 0

            elif kwargs['selection'] == '6':
                if sptemp[1] >= 20000:
                    if kwargs['phase'] == '0':
                        em = discord.Embed(title=kwargs['author'].name + ', 이주할 색상을 고르시기 바랍니다. 이하의 선택지 외에는 선택 불가능하며 철회는 불가능합니다.', colour=0x07ECBA)
                        em.set_image(url='https://cdn.discordapp.com/attachments/296519249134878720/397222940292284417/Untitled-2.jpg')
                        em.set_footer(text='취소하려면 선택지가 아닌 아무거나 입력하시기 바랍니다.')
                        return em, 1
                    elif kwargs['phase'].isdigit() and int(kwargs['phase']) in range(1,6):
                        em = await sp.immigrate(cursor, author=kwargs['author'], choice=kwargs['phase'])
                        db.commit()
                        db.close()
                        return em, 0
                    else:
                        em = discord.Embed(title=kwargs['author'].name + ', 취소되었습니다.', colour=0xd4eff6)
                        return em, 0
                else:
                    em = discord.Embed(title=kwargs['author'].name + '님, [넥센]이시네요 ㅅㄱ', colour=0xd4eff6)
                    return em, 0

            elif kwargs['selection'] == '7':
                em = discord.Embed(title='구랭.', colour=0x07ECBA)
                return em, 0
            else:
                em = discord.Embed(title=kwargs['author'].name + ', 취소되었습니다.', colour=0xd4eff6)
                return em, 0

    async def ssword(*args, **kwargs):
        spsschk = 0
        for i in kwargs['author'].roles:
            if '295021019851128842' == i.id:
                spsschk += 1
                break
        if spsschk == 0:
            args[0].execute("SELECT * FROM SHUPoint WHERE id='"+str(kwargs['author'].id)+"' COLLATE NOCASE")
            curind = args[0].fetchone()
            args[0].execute("UPDATE SHUPoint SET pt=?, log=? Where id=? COLLATE NOCASE", (curind[1] - 100, datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + ' SSWORD-100,' + curind[2], kwargs['author'].id))
            await client.add_roles(kwargs['author'], discord.utils.get(client.get_server(str(88844446929547264)).roles, id='295021019851128842'))
            em = discord.Embed(title=kwargs['author'].name + '은(는) 100pt를 사용해 날카로운 +1 숏 소드를 얻었다!', description='\n\n크큭... 선이 보인다...\n\n```python\n========================================================\n                         RULES\n========================================================\n1. 숏 소드를 배포하는 것은 자유입니다.(예외: 캐부, 셀펠매)\n2. 흰색 닉과 자신 외에는 사체로 만들어선 안됩니다.\n3. 신규 등급을 생성해서는 안됩니다.\n4. 사체를 소생시켜서는 안됩니다. 시체는 잘 묻어놔야죠.\n5. 자신 혹은 타인을 사체를 제외한 타 마을으로 옮기거나 타인의 숏 소드를 제외한 등급을 삭제해선 안됩니다.```', colour=0x07ECBA)
            em.set_footer(text='즐거운 소드마스터 라이프 되시기 바랍니다.')
        else:
            em = discord.Embed(title=kwargs['author'].name + ', 넌 이미 숏 소드가 있는데?',colour=0xd4eff6)
        return em

    async def escape(*args, **kwargs):
        spsschk = 0
        for i in kwargs['author'].roles:
            if '88882661761773568' == i.id:
                spsschk += 1
                break
        if spsschk == 1:
            args[0].execute("SELECT * FROM SHUPoint WHERE id='"+str(kwargs['author'].id)+"' COLLATE NOCASE")
            curind = args[0].fetchone()
            args[0].execute("UPDATE SHUPoint SET pt=?, log=? Where id=? COLLATE NOCASE", (curind[1] - 500, datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + ' RSFELM-500,' + curind[2], kwargs['author'].id))
            await client.remove_roles(kwargs['author'], discord.utils.get(client.get_server(str(88844446929547264)).roles, id='88882661761773568'))
            em = discord.Embed(title=kwargs['author'].name + '은(는) 셀펠매 상태에서 벗어났다!', colour=0x07ECBA)
            em.set_footer(text='즐거운 자유인 라이프 되시기 바랍니다. 얼마나 오래갈지는 모르겠지만요.')
        else:
            em = discord.Embed(title=kwargs['author'].name + ', 셀펠매 상태가 아니면 이 커맨드는 쓸 수 없어.',colour=0xd4eff6)
        return em

    async def immigrate(*args, **kwargs):
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

        args[0].execute("SELECT * FROM SHUPoint WHERE id='"+str(kwargs['author'].id)+"' COLLATE NOCASE")
        curind = args[0].fetchone()
        args[0].execute("UPDATE SHUPoint SET pt=?, log=? Where id=? COLLATE NOCASE", (curind[1] - 1000, datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + ' IMMGRT-1000,' + curind[2], kwargs['author'].id))
        em = discord.Embed(title=kwargs['target'].name + ', 소속이 변경되었습니다.', colour=0x07ECBA)
        em.set_footer(text='변심으로 인한 변경은 불가능합니다.')
        return em

    async def geths(*args):
        hillst = sqlite3.connect(cwd + '\db\EurDB.db').cursor().execute("SELECT * FROM SHUPoint WHERE id='"+args[0]+"' COLLATE NOCASE").fetchone()[5]
        if hillst is None:
            hillst = 0
        return hillst

    async def updatehs(*args):
        db = sqlite3.connect(cwd + '\db\EurDB.db')
        cursor = db.cursor()
        hill_exist = cursor.execute('SELECT hillariest FROM SHUPoint WHERE id=? COLLATE NOCASE', (args[0],)).fetchone()[0]
        if hill_exist != None:
            if hill_exist < args[1]:
                cursor.execute('UPDATE SHUPoint SET hillariest=?, hillariest_at=? WHERE id=? COLLATE NOCASE', (str(args[1]), datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), args[0]))
        elif args[1] > 0:
            cursor.execute('UPDATE SHUPoint SET hillariest=?, hillariest_at=? WHERE id=? COLLATE NOCASE', (str(args[1]), datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), args[0]))
        cursor.execute('UPDATE SHUPoint SET hillarystreak=? Where id=? COLLATE NOCASE', (str(args[1]), args[0]))
        db.commit()
        db.close()
        return

    async def deleteroles(*args, **kwargs):
        await client.replace_roles(kwargs['author'], discord.utils.get(client.get_server(str(88844446929547264)).roles, id=str(88844446929547264)))

    async def addsig(*args, **kwargs):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(kwargs['detail'].split()[1]) as resp:
                    sigraw = await resp.read()
                    sigres = Image.open(BytesIO(sigraw))
                    signame = await eurikabasics.uselessnamegen(12)
                    sigcmd = kwargs['detail'].split()[0].replace('-', '')
                    sigdest = "C:\EurikaMkIII\image\\" + signame + "." + sigres.format.lower()
                    if sigres.format.lower() == 'gif':
                        r = requests.get(kwargs['detail'].split()[1], headers={'User-Agent': 'Mozilla/5.0'})
                        with open(sigdest, 'wb') as siggif:
                            siggif.write(r.content)
                    else:
                        sigres.save(sigdest)
                    args[0].execute("SELECT * FROM SHUPoint WHERE id='"+str(kwargs['author'].id)+"' COLLATE NOCASE")
                    curind = args[0].fetchone()
                    args[0].execute("INSERT INTO SImage (initializer, loc, registrator) VALUES ('" + sigcmd + "', '" + signame + "." + sigres.format.lower() + "', '" + kwargs['author'].id + "')")
                    args[0].execute("UPDATE SHUPoint SET pt=?, log=? Where id=? COLLATE NOCASE", (curind[1] - kwargs['price'], datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + ' SIGADD-' + str(kwargs['price']) + ', ' + curind[2], kwargs['author'].id))
                    em = discord.Embed(title=kwargs['author'].name + '이 신규 커맨드 -' + sigcmd + '을(를) 등록했습니다.', description='{}pt가 소모됩니다.'.format(str(kwargs['price'])), colour=0x07ECBA)

        except:
            #print("Unexpected error:", sys.exc_info())
            em = discord.Embed(title=kwargs['author'].name + ', 에러가 발생했습니다.', colour=0xd4eff6)

        return em

    async def delsig(*args, **kwargs):
        try:
            args[0].execute("SELECT * FROM SHUPoint WHERE id='"+str(kwargs['author'].id)+"' COLLATE NOCASE")
            curind = args[0].fetchone()
            args[0].execute("DELETE FROM SImage WHERE initializer ='{}'".format(kwargs['detail']))
            args[0].execute("UPDATE SHUPoint SET pt=?, log=? Where id=? COLLATE NOCASE", (curind[1] - 5, datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') + ' SIGDEL-05,' + curind[2], kwargs['author'].id))
            em = discord.Embed(title='{}이 신규 커맨드 -을(를) 삭제했습니다.'.format(kwargs['author'].name, str(kwargs['detail'])), description='5pt가 소모됩니다.', colour=0x07ECBA)
        except:
            #print("Unexpected error:", sys.exc_info())
            em = discord.Embed(title=kwargs['author'].name + ', 에러가 발생했습니다.', colour=0xd4eff6)
        return em
