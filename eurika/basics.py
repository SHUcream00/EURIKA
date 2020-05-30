import re
import random
import time
import datetime
import asyncio
import aiohttp
import ast
import string
import aiosqlite
import collections
from bs4 import BeautifulSoup as bs
import json
from math import *

#__import__('os').system('rm -rf /dir')

cwd = r'C:\EurikaMkIII'

async def rand_name_gen(length):
    '''Create random string from upper, lower alphabets with numbers for dummy names'''
    template = string.ascii_letters + string.digits
    return ''.join(random.choice(template) for _ in range(length))

async def rand_select(opts):
    '''return a random element from iterables.'''
    return random.choice(opts)

async def ordered_select(iterables) -> str:
    '''Returns a string with iterables ordered randomly'''
    iterables = list(map(str, iterables))
    random.shuffle(iterables)
    return '->'.join(iterables)

async def dice_roll(*dice):
    '''NdN dice, if NdN is not given'''
    if len(dice) == 1:
        return random.randint(1, dice[0])
    if len(dice) >= 2:
        res = [random.randint(1, dice[1]) for _ in range(0,dice[0])]
        res_text = list(map(str, res))
        if len(dice) >= 3:
            return " ".join(res_text) , sum(res)+int(dice[2]), dice[2]
        return " ".join(res_text), sum(res), 0


async def dday(first: datetime.date, second:datetime.date):
    '''Tells difference between two given dates in days'''
    return (first-second).days

async def calc(exp:str):
    #THIS USES EVAL PERIOD
    '''Calculate the given expression without eval()'''
    math_constant = {'tan':'', 'sin':'','cos':'','acos':'','asin':'','atan':'','pi':"3.141592653589793238",'e':"2.71828",
                'tau':'', 'inf':'', 'nan':'', "^": "**", "x": "*"}
    for i in math_constant.keys():
        if i in exp:
            exp = exp.replace(i, math_constant[i])

    def check_legit(exp):
        for i in math_constant.keys():
            if i in exp:
                exp = exp.replace(i, "")
        exp = re.sub('[()+*/%^. ]', '', exp.replace('-',''))
        return exp.isdigit()

    return eval(exp) if check_legit(exp) else False

async def jaegi():
    '''Get Han River's current water temperature'''
    async with aiohttp.ClientSession() as session:
        async with session.get('http://hangang.dkserver.wo.tc/') as jaegi:
            return json.loads(await jaegi.text())['temp']

async def upside_dn(alnum: str):
    #unfinished - unicode related problem
    '''Prints text upside down, should be alphabet or arabic numbers'''
    alts = {'a':'ɐ', 'b':'q', 'c':'ɔ', 'd':'p', 'e':'ǝ', 'f':'ɟ', 'g':'ƃ', 'h':'ɥ', \
            'i':'ᴉ', 'j':'ɾ', 'k':'ʞ', 'l':'l', 'm':'ɯ', 'n':'u', 'o':'o', 'p':'d', \
            'q':'b', 'r':'ɹ', 's':'s', 't':'ʇ', 'u':'n', 'v':'ʌ', 'w':'ʍ', 'x':'x', \
            'y':'ʎ', 'z':'z', '1':'Ɩ', '2':'ᄅ', '3':'Ɛ', '4':'ㄣ', '5':'ϛ', '6':'9', \
            '7':'ㄥ', '8':'8', '9':'6'}
    return list(alts.get(i, 'X') for i in alnum[::-1])

async def is_image(link):
    '''under work'''
    async with aiohttp.ClientSession() as session:
        async with session.get(str(link)) as resp:
            print(resp)

async def sig_n(server, key = None, **kwargs):
    '''By Swift Image Generator for printing out some meme images quickly as possible - Not actual generator'''
    if server == 88844446929547264:
        dbname = "EurDB"
    elif server == 360292207552626688:
        dbname = "TempShiho"

    async with aiosqlite.connect(cwd + f'\db\{dbname}.db') as db:
        async with db.execute(f"SELECT * FROM SImage WHERE initializer='{key}' COLLATE NOCASE") as cursor:
            res = await cursor.fetchone()
            if res:
                return cwd + '\image\\' + res[2], res[3], res[1]
            else:
                return None

async def keep_sig_integrity():
    '''Background task to make sure image is still up'''
    while True:
        async with aiosqlite.connect(cwd + '\db\EurDB.db') as db:
            async with db.execute("SELECT * FROM SImage WHERE cache != NULL OR cache != ''") as cursor:
                targets = await cursor.fetchall()
                for i in targets:
                    async with aiohttp.ClientSession() as session:
                        async with session.get(i[3]) as resp:
                            if resp.status in range(400,405) or (resp.headers["content-type"] in ["image/png", "image/jpeg", "image/jpg", "image/gif", 'image/webp']) == False:
                                await db.execute(f"UPDATE SImage SET cache=NULL WHERE initializer={i[1]}")

                await db.commit()
        await asyncio.sleep(144000)


async def updatesig_n(server, link = None, name = None, **kwargs):
    '''Update cache data for sig '''
    if server == 88844446929547264:
        dbname = "EurDB"
    elif server == 360292207552626688:
        dbname = "TempShiho"

    async with aiosqlite.connect(cwd + f'\db\{dbname}.db') as db:
        await db.execute("UPDATE SImage SET cache=? Where initializer=?", (link, name))
        await db.commit()

async def randsig_n(server, *args):
    '''Get a random image from SIG table'''

    if server == 88844446929547264:
        dbname = "EurDB"
    elif server == 360292207552626688:
        dbname = "TempShiho"

    async with aiosqlite.connect(cwd + f'\db\{dbname}.db') as db:
        if len(args) == 0:
            async with db.execute("SELECT * FROM SImage ORDER By RANDOM() LIMIT 1") as cursor:
                res = await cursor.fetchone()
                return cwd + '\image\\' + res[2], res[3], res[1]
        else:
            async with db.execute(f"SELECT * FROM SImage WHERE Initializer LIKE '%{args[0]}%' ORDER BY RANDOM() LIMIT 1 COLLATE NOCASE") as cursor:
                res = await cursor.fetchone()
                if res:
                    return cwd + '\image\\' + res[2], res[3], res[1]
                else:
                    return None


async def codeblock(text: str):
    '''return text wrapped up in python codeblock for discord'''
    if text == "":
        text = "Empty"
    return f"```python\n{text}\n```"

async def blueblock(text: str):
    '''return text wrapped up in python codeblock for discord'''
    if text == "":
        text = "Empty"
    return f"```ini\n{text}\n```"

async def listsig_n():
    '''Print whole list of column initializer values of Swift Image Generator(SIG) table'''
    async with aiosqlite.connect(cwd + '\db\EurDB.db') as db:
        async with db.execute("SELECT * FROM SImage ORDER By Initializer ASC") as cursor:
            res = cursor.fetchall()
            return res

async def get_alarm(id_ = None):
    '''Get the list of unfinished alarms from db which has been registered by id'''
    res = []
    async with aiosqlite.connect(cwd + '\db\EurAlmDB.db') as db:
        if id_:
            statement = "SELECT * FROM Alarm Where owner = {}".format(id_)
        else:
            statement = "SELECT * FROM Alarm"
        async with db.execute(statement) as cursor:
            for i in await cursor.fetchall():
                time_offset = (datetime.datetime.strptime(i[2], "%Y-%m-%d %H:%M:%S") - datetime.datetime.now()).total_seconds()
                if time_offset < 0:
                    await db.execute("DELETE FROM Alarm WHERE id = {}".format(i[0]))
                else:
                    res.append(i + (str(datetime.timedelta(seconds=time_offset)),))
        await db.commit()
    return res

async def alarm(id_, timestring, memo = "", **kwargs):
    '''Main driver function for alarm category methods'''
    timestring = await time_to_sec(timestring)
    await set_alarm(id_, timestring, memo, channel=kwargs['channel'], server=kwargs['server'])
    await asyncio.sleep(timestring)

async def set_alarm(id_, timestring, memo = "", **kwargs):
    async with aiosqlite.connect(cwd + '\db\EurAlmDB.db') as db:
        timestring = (datetime.datetime.now() + datetime.timedelta(seconds=timestring)).strftime("%Y-%m-%d %H:%M:%S")
        await db.execute("INSERT INTO Alarm (owner, time, memo, channel, server) \
                        VALUES ('{}', '{}', '{}', '{}', '{}')".format(id_, timestring, memo, kwargs['channel'], kwargs['server']))
        await db.commit()
    return

async def time_to_sec(timestr):
    '''to secs()'''
    if timestr and str(timestr).isdigit() == True:
        alm_sec = str(timestr)
    else:
        alm_sec='0'
        if re.search('\d+시간', timestr):
            alm_sec += '+' + re.search('\d+시간', timestr).group(0).replace('시간', ' * 3600')
        if re.search('\d+분', timestr):
            alm_sec += '+' + re.search('\d+분', timestr).group(0).replace('분', ' * 60')
        if re.search('\d+초', timestr):
            alm_sec += '+' + re.search('\d+초', timestr).group(0).replace('초', ' * 1')

    res = await calc(alm_sec)
    return res

    async def cex(*args):
        curdict = {'원':'KRW', '위안': 'CNY', '파운드': 'GBP', '유로': 'EUR', '달러': 'USD', '엔': 'JPY', '홍콩달러': 'HKD', '레알': 'BRL',
                    '캐나다달러': 'CAD', '스위스프랑': 'CHF', '인도네시아루피': 'IDR', '페소': 'MXN', '필리핀페소': 'PHP', '레우': 'RON', '크로네': 'NOK',
                    '포린트': 'HUF', '쿠나': 'HRK', '즈워티': 'PLN', '루피': 'INR', '링깃': 'MYR', '크로나': 'SEK', '루블': 'RUB', '싱가포르달러': 'SGD',
                    '바트': 'THB', '리라': 'TRY', '랜드': 'ZAR', '달러': 'USD'}
        cexchecker = re.compile('\d+(\.\d+)?')
        try:
        #if args[0][2] in curdict and cexchecker.match(args[0][1]) and len(args[0]) > 1:
            async with aiohttp.ClientSession() as session:
                async with session.get("http://data.fixer.io/api/latest?access_key=8572d46f86bde368626be482bc7cc50f") as cexhtml: #curdict[args[0][2]]
                    cexbase = json.loads(await cexhtml.text())['rates']
                    basecur = curdict[args[0][2]]
                    if len(args[0]) >= 5:
                        if cexchecker.match(args[0][4]):
                            if (round(float(args[0][1]) / cexbase[curdict[args[0][2]]] * cexbase[curdict[args[0][3]]] - float(args[0][4]),3) > 0):
                                em = discord.Embed(title=args[0][1] + ' '  + args[0][2] + ' => ' + args[0][3] + ' 환전 결과 (비교 대상: ' + args[0][4] + ' ' + args[0][3] + ')',
                                description= args[0][1] + ' ' + args[0][2] + '(이)가 ' + str(round(float(args[0][1]) / cexbase[curdict[args[0][2]]] * cexbase[curdict[args[0][3]]] - float(args[0][4]),3)) + args[0][3] + ' 만큼 더 비쌈', colour = 0x005CCC)
                            else:
                                em = discord.Embed(title=args[0][1] + ' '  + args[0][2] + ' => ' + args[0][3] + ' 환전 결과 (비교 대상: ' + args[0][4] + ' ' + args[0][3] + ')',
                                description= args[0][4] + ' ' + args[0][3] + '(이)가 ' + str(abs(round(float(args[0][1]) / cexbase[curdict[args[0][2]]] * cexbase[curdict[args[0][3]]] - float(args[0][4]),3))) + args[0][3] + ' 만큼 더 비쌈', colour = 0x005CCC)
                    else:
                        em = discord.Embed(title=args[0][1] + ' '  + args[0][2] + ' => ' + args[0][3] + ' 환전 결과', description= str(round(float(args[0][1]) / cexbase[curdict[args[0][2]]] * cexbase[curdict[args[0][3]]],3)) + args[0][3], colour = 0x005CCC)
                    if (args[0][2] == '달러' or args[0][3] == '달러') and (float(args[0][1]) == 4 or str(round(float(args[0][1]) / cexbase[curdict[args[0][2]]] * cexbase[curdict[args[0][3]]],3)).split('.')[0] == '4'):
                        em.set_image(url='https://cdn.discordapp.com/attachments/192692517827772417/345061938901811200/7798b46504e4a060.jpg')
        except:
            curlist  = ''
            for i,j in curdict.items():
                curlist += i + ' '
            em = discord.Embed(title='난토! 에러가 났네요!', description = '[예시]\n=환율 (액수) (현재화폐) (바꿀화폐)\n혹은\n=환율 (액수) (현재화폐) (바꿀화폐) (비교액수)\n[사용가능한 화폐종류]\n' + curlist, colour=0xB5002B)
        return em

async def bitly(**kwargs):
    async with aiosqlite.connect(cwd + '\db\EurDB.db') as db:
        async with db.execute("SELECT * FROM Bitly WHERE oridmn={} COLLATE NOCASE".format(kwargs['original'])) as cursor:
            pick = cursor.fetchone()
            if pick:
                return pick[2]
            else:
                blytkn = 'ec36cf5499eee7b6e20c9a0f817e0df5d2e1a265'
                async with aiohttp.ClientSession() as session:
                    async with session.get('https://api-ssl.bitly.com/v3/shorten', params={'Content-Type':'application/x-www-form-urlencoded', 'access_token': blytkn, 'longUrl': kwargs['original']}) as resp:
                        blyres = json.loads(await resp.text())['data']['url']
                        await db.execute("INSERT INTO Bitly (oridmn, shtdmn) VALUES ('{}', '{}')".format(kwargs['original'], blyres))
                        await db.commit()

                return blyres
