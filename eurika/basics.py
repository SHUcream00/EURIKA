import re
import random
import time
import datetime
import asyncio
import aiohttp
import ast
import aiosqlite
from math import *

#__import__('os').system('rm -rf /dir')

cwd = r'C:\EurikaMkIII'

async def rand_name_gen(length):
    '''Create random string from upper, lower alphabets with numbers for dummy names'''
    template = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return ''.join(random.choice(template) for _ in range(length))

async def rand_select(opts):
    '''return a random element from iterables.'''
    return random.choice(opts)

async def ordered_select(iterables) -> str:
    '''Returns a string with iterables ordered randomly'''
    iterables = list(map(str, iterables))
    random.shuffle(iterables)
    return '->'.join(iterables)

async def dice_roll(times, head, adjust=0):
    '''NdN dice, if NdN is not given'''
    return times * head + adjust

async def dday(first: datetime.date, second:datetime.date):
    '''Tells difference between two given dates in days'''
    return (first-second).days

def calc(exp:str):
    #THIS USES EVAL PERIOD
    '''Calculate the given expression without eval()'''
    math_funcs = {'tan':'', 'sin':'','cos':'','acos':'','asin':'','atan':'','pi':'','e':'',\
                'tau':'', 'inf':'', 'nan':''}
    exp = exp.replace('^', '**').replace('x','*')

    def check_legit(exp):
        for i in math_funcs.keys():
            if i in exp: exp = exp.replace(i, "")
        exp = re.sub('[()+*/%^. ]', '', exp.replace('-',''))
        return exp.isdigit()

    return eval(exp) if check_legit(exp) else "Some Error"

async def jaegi():
    '''Get Han River's current water temperature'''
    async with session.get('http://hangang.dkserver.wo.tc/') as jaegi:
        async with aiohttp.ClientSession() as session:
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

async def sig_n(key = None, **kwargs):
    '''By Swift Image Generator for printing out some meme images quickly as possible - Not actual generator'''
    async with aiosqlite.connect(cwd + '\db\EurDB.db') as db:
        async with db.execute("SELECT * FROM SImage WHERE initializer='"+key+"' COLLATE NOCASE") as cursor:
            res = await cursor.fetchone()
            if res:
                return cwd + '\image\\' + res[2], res[3], res[1]
            else:
                return None

async def keep_sig_integrity(link):
    '''Background task to make sure image is still up'''
    async with aiosqlite.connect(cwd + '\db\EurDB.db') as db:
        async with db.execute("SELECT * FROM SImage where cache != NULL") as cursor:
            targets = await cursor.fetchall()
            for i in targets:
                async with aiohttp.ClientSession() as session:
                    async with session.get(deadlink) as resp:
                        if resp.status in range(400,405) or (resp.headers["content-type"] in ["image/png", "image/jpeg", "image/jpg"]) == False:
                            await db.execute("UPDATE SImage SET cache=NULL Where initializer=?", i[1])
            await db.commit()


async def updatesig_n(link = None, name = None, **kwargs):
    '''Update cache data for sig '''
    async with aiosqlite.connect(cwd + '\db\EurDB.db') as db:
        await db.execute("UPDATE SImage SET cache=? Where initializer=?", (link, name))
        await db.commit()

async def randsig_n():
    '''Get a random image from SIG table'''
    async with aiosqlite.connect(cwd + '\db\EurDB.db') as db:
        async with db.execute("SELECT * FROM SImage ORDER By RANDOM() LIMIT 1") as cursor:
            res = await cursor.fetchone()
            return cwd + '\image\\' + res[2], res[3], res[1]

async def listsig_n():
    '''Print whole list of column initializer values of Swift Image Generator(SIG) table'''
    async with aiosqlite.connect(cwd + '\db\EurDB.db') as db:
        async with db.execute("SELECT * FROM SImage ORDER By Initializer ASC") as cursor:
            res = cursor.fetchall()
            return res

async def retrieve_alarms(id_):
    '''Get the list of unfinished alarms from db'''
    async with aiosqlite.connect(cwd + '\db\EurAlmDB.db') as db:
        async with db.execute("SELECT * FROM SImage Where owner = {}".format(id_)) as cursor:
            return await cursor.fetchall()

async def alarm(id_, timestring, memo):
    async with aiosqlite.connect(cwd + '\db\EurAlmDB.db') as db:

        await db.execute("INSERT INTO Alarm (owner, time, memo) VALUES ({}, {}, {})".format(id_, timestring, memo))
        await db.commit()

async def time_to_sec(timestr):
    alm='0'
    if re.search('\d+시간', timestr):
        almtime += '+' + re.search('\d+시간', timestr).group(0).replace('시간', ' * 3600')
    if re.search('\d+분', timestr):
        almtime += '+' + re.search('\d+분', timestr).group(0).replace('분', ' * 60')
    if re.search('\d+초', timestr):
        almtime += '+' + re.search('\d+초', timestr).group(0).replace('초', ' * 1')

    
