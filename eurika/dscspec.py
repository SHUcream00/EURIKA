'''
Discord-specific functions
mostly for channel management to avoid writing long blahblahs in the original file
'''

import discord
import sqlite3

async def codeblock(text):
    '''return text wrapped up in python codeblock for discord'''
    return '```python\n'+str(text)+'\n```'

async def joindate(username, joinchan):
    em = discord.Embed(title="본 계정이 슈크림딜라이트에 가입한 일자는 다음과 같습니다.", description=str(username.joined_at), colour=0x07ECBA)
    em.set_author(name=username.name, icon_url=username.avatar_url)
    return em

async def createdate(username, joinchan):
    em = discord.Embed(title="본 계정이 디스코드에 생성된 일자는 다음과 같습니다.", description=str(username.created_at) , colour=0x07ECBA)
    em.set_author(name=username.name, icon_url=username.avatar_url)
    return em

async def uselessnamegen(length):
    template = "abcdefghijklmnopqrstuvwxyz0123456789"
    res = ''
    for i in range(length):
        res += random.choice(template)
    return res

async def sig(*args, **kwargs):
    '''By Swift Image Generator for printing out some meme images quickly as possible'''
    db = sqlite3.connect(cwd + '\db\EurDB.db')
    cursor = db.cursor()
    sigres = cursor.execute("SELECT * FROM SImage WHERE initializer='"+kwargs['name']+"' COLLATE NOCASE").fetchone()

    if sigres != None:
        if sigres[3] != None:
            return 1, cwd + '\image\\' + sigres[2], sigres[3]
        else:
            return 1, cwd + '\image\\' + sigres[2]
    else:
        return 0, 0

async def listsig():
    '''Print whole list of column initializer values of Swift Image Generator(SIG) table'''
    db = sqlite3.connect(cwd + '\db\EurDB.db')
    cursor = db.cursor()
    sigtemp = cursor.execute("SELECT * FROM SImage ORDER By Initializer ASC").fetchall()
    return sigtemp

async def randsig():
    '''Get a random image from SIG table'''
    db = sqlite3.connect(cwd + '\db\EurDB.db')
    cursor = db.cursor()
    sigtemp = cursor.execute("SELECT * FROM SImage ORDER By RANDOM() LIMIT 1").fetchone()
    return 1, cwd + '\image\\' + sigtemp[2], sigtemp[1]


async def bitly(**kwargs):
    db = sqlite3.connect(cwd + '\db\EurDB.db')
    cursor = db.cursor()
    blycnt = cursor.execute("SELECT COUNT(*) FROM Bitly WHERE oridmn='"+kwargs['original']+"' COLLATE NOCASE").fetchone()[0]
    if blycnt >= 1:
        blytemp = cursor.execute("SELECT * FROM Bitly WHERE oridmn='"+kwargs['original']+"' COLLATE NOCASE").fetchone()
        return blytemp[2]
    else:
        blytkn = 'ec36cf5499eee7b6e20c9a0f817e0df5d2e1a265'
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api-ssl.bitly.com/v3/shorten', params={'Content-Type':'application/x-www-form-urlencoded', 'access_token': blytkn, 'longUrl': kwargs['original']}) as resp:
                blyres = json.loads(await resp.text())['data']['url']
                cursor.execute('INSERT INTO Bitly (oridmn, shtdmn) VALUES ("'+kwargs['original']+'", "'+blyres+'")')
                db.commit()
                db.close()
                return blyres
