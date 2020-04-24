import random
import sqlite3
import datetime

'''
170903 생성

Originally created on 3rd of September, 2017 by Joon Choi aka SHUcream
Database Managing script for Python-3 based Discord bot based on sql

'''

cwd = r'C:\EurikaMkIII'

class memento():
    async def recall(memtgt):
        db = sqlite3.connect(cwd + "\db\EurDB.db")
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM Memory WHERE Name='"+memtgt+"' COLLATE NOCASE")
        tgtcnt = cursor.fetchone()[0]
        if tgtcnt > 0:
            cursor.execute("SELECT * FROM Memory WHERE Name='"+memtgt+"' COLLATE NOCASE")
            tgttxt = cursor.fetchone()
            return tgttxt, 0x07ECBA
        else:
            return memtgt + "? 들어본 적도 없는 걸. 확실히 기억나지 않는다면 =찾아 (키워드) 를 써봐", 0xB5002B

    async def memorize(memtgt, memdet, **kwargs):
        db = sqlite3.connect(cwd + "\db\EurDB.db")
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM Memory WHERE Name='"+memtgt+"'")
        tgtcnt = cursor.fetchone()[0]
        if tgtcnt > 0:
            return memtgt + "은(는) 이미 저장되어있는데?", 0xB5002B
        else:
            cursor.execute("INSERT INTO Memory (Name, Value, User, Date) VALUES ('" + memtgt + "', '" + memdet + "', '"+ kwargs['author'] +"', '"+ datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') +"')")
            db.commit()
            db.close()
            return memtgt + "을(를) 기억했어.", 0x07ECBA

    async def find(memtgt):
        db = sqlite3.connect(cwd + "\db\EurDB.db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Memory WHERE Name Like'%"+memtgt+"%' COLLATE NOCASE")
        tgtlist = ''
        for row in cursor :
            tgtlist = tgtlist + ' ' + row[1]
        if ' ' in tgtlist:
            return tgtlist, 0x07ECBA, str(len(tgtlist.split(' ')) -1)
        else:
            return memtgt + "? 들어본 적도 없는 걸", 0xB5002B, '0'

    async def append(memtgt, memdet, **kwargs):
        db = sqlite3.connect(cwd + "\db\EurDB.db")
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM Memory WHERE Name='"+memtgt+"' COLLATE NOCASE")
        tgtcnt = cursor.fetchone()[0]
        if tgtcnt == 0:
            return memtgt + "? 들어본 적도 없는 걸. 기억나지 않는다면 =찾아 를 써보렴.", 0xB5002B
        else:
            cursor.execute("SELECT * FROM Memory WHERE Name='"+memtgt+"' COLLATE NOCASE")
            tgttxt = cursor.fetchone()
            tgtfin = (tgttxt[2]+" - "+memdet, kwargs['author'], datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), memtgt)
            cursor.execute("UPDATE Memory SET value=?, User=?, Date=? Where Name=? COLLATE NOCASE", tgtfin)
            db.commit()
            db.close()
            return memtgt + "에 관한 기억을 추가했어." , 0x07ECBA

    async def own(**kwargs):
        db = sqlite3.connect(cwd + "\db\EurDB.db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM Memory WHERE User='"+kwargs['author']+"'")
        tgtlist = ''
        for row in cursor :
            tgtlist = tgtlist + ' ' + row[1]
        if ' ' in tgtlist :
            return tgtlist, 0x07ECBA, str(len(tgtlist.split(' '))-1)
        else:
            return kwargs['author'] + "(이)가 가르쳐준 건 아무것도 없는걸. 다른 사람에게 NTR 당했을지도 몰라", 0xB5002B, '0'

    async def rand():
        db = sqlite3.connect(cwd + "\db\EurDB.db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM sqlite_sequence WHERE Name='Memory'")
        tgtnum = cursor.fetchone()[1]
        tgtnum2 = random.randint(1,int(tgtnum))
        cursor.execute("SELECT * FROM Memory WHERE Number="+format(tgtnum2))
        tgttxt = cursor.fetchone()
        return tgttxt, 0x07ECBA


    '''
    레거시

    if message.content.startswith('=기억') or message.content.startswith('=알려') or message.content.startswith('=찾아') or message.content.startswith('=붙여') or message.content.startswith('=내기억') or message.content.startswith('=랜덤기억') or message.content.startswith('=mem'):
        db = sqlite3.connect(cwd + '\db\EurDB.db')
        cursor = db.cursor()
        #tgt = (message.content.lstrip('=기억 ').lstrip('=알려 ').lstrip('=찾아 ').lstrip('=붙여 '))
        tgt = message.content[4:]
        if message.content.count(' ') == 0 and '기억' not in message.content:
            await client.send_message(message.channel,"에러가 났지 시프요")
            return
        elif message.content.count(' ') < 2 and '=기억' in message.content:
            await client.send_message(message.channel,"기억은 언제나 [=기억 표제 내용] 식으로 해주새오.")
            return
        else :
            if message.content.startswith('=기억') :
                tgtArr = tgt.split(' ',1)
                cursor.execute("SELECT COUNT(*) FROM Memory WHERE Name='"+tgtArr[0]+"'")
                tgtcnt = cursor.fetchone()[0]
                if tgtcnt > 0:
                    await client.send_message(message.channel, tgtArr[0] + "은(는) 이미 저장되어있는데?")
                else :
                    cursor.execute("INSERT INTO Memory (Name, Value, User, Date) VALUES ('" + tgtArr[0] + "', '" + tgtArr[1] + "', '"+ message.author.id +"', '"+ datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S') +"')")
                    await client.send_message(message.channel, tgtArr[0] + "을(를) 기억했어.")
            if message.content.startswith('=알려') or message.content.startswith('=mem'):
                cursor.execute("SELECT COUNT(*) FROM Memory WHERE Name='"+tgt.replace(" ", "")+"'")
                tgtcnt = cursor.fetchone()[0]
                if tgtcnt > 0:
                    cursor.execute("SELECT * FROM Memory WHERE Name='"+tgt.replace(" ", "")+"'")
                    tgttxt = cursor.fetchone()
                    await client.send_message(message.channel, "[**" + tgttxt[1] + "**] " + tgttxt[2] + " | " + tgttxt[4] + "의 순간에 각인된 기억.")
                    #await client.send_message(message.channel, "[**" + tgttxt[1] + "**]" + " " + tgttxt[2] + " " + "(" + tgttxt[4] + ")")
                else :
                    await client.send_message(message.channel, tgt.replace(" ", "") + "? 들어본 적도 없는 걸.")
            if message.content.startswith('=찾아') :
                cursor.execute("SELECT * FROM Memory WHERE Name Like'"+"%"+tgt+"%"+"'")
                tgtlist = ''
                for row in cursor :
                    tgtlist = tgtlist + ' ' + row[1]
                if ' ' in tgtlist :
                    await client.send_message(message.channel, "[**" + tgt + "에 관련된 기억 목록**]" + tgtlist)
                else :
                    await client.send_message(message.channel, tgt + "에 관련된 것은 기억하고 있지 않아.")

            if message.content.startswith('=붙여') :
                tgtArr = tgt.split(' ',1)
                cursor.execute("SELECT COUNT(*) FROM Memory WHERE Name='"+tgtArr[0]+"'")
                tgtcnt = cursor.fetchone()[0]
                if tgtcnt > 0:
                    cursor.execute("SELECT * FROM Memory WHERE Name='"+tgtArr[0]+"'")
                    tgttxt = cursor.fetchone()
                    tgtfin = (tgttxt[2]+" - "+tgtArr[1], message.author.id, datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S'), tgtArr[0])
                    cursor.execute("UPDATE Memory SET value=?, User=?, Date=? Where Name=?", tgtfin)
                    await client.send_message(message.channel, tgtArr[0] + "에 관한 기억을 추가했어.")
                else :
                    await client.send_message(message.channel, tgtArr[0] + "? 들어본 적도 없는 걸. 기억나지 않는다면 =찾아 를 써보렴. ")
        if message.content.startswith('=내기억') :
            cursor.execute("SELECT * FROM Memory WHERE User='"+message.author.id+"'")
            tgtlist = ''
            for row in cursor :
                tgtlist = tgtlist + ' ' + row[1]
            if ' ' in tgtlist :
                await client.send_message(message.channel, "[" + message.author.name + "이 가르쳐준 기억 목록]" + tgtlist)
            else :
                await client.send_message(message.channel, message.author.name + "에 관련된 것은 기억하고 있지 않아. 기억나지 않는다면 =찾아 를 써보렴. ")
        if message.content.startswith('=랜덤기억') :
            cursor.execute("SELECT * FROM sqlite_sequence WHERE Name='Memory'")
            tgtnum = cursor.fetchone()[1]
            tgtnum2 = random.randint(1,int(tgtnum))
            cursor.execute("SELECT * FROM Memory WHERE Number="+format(tgtnum2))
            tgttxt = cursor.fetchone()
            await client.send_message(message.channel, "[**" + tgttxt[1] + "**] " + tgttxt[2] + " | " + tgttxt[4] + "의 순간에 각인된 기억.")
        db.commit()
        db.close()
        '''
