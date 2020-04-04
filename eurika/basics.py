import random
import datetime
import aiohttp

async def rand_select(selections):
    '''return a random element from iterables.'''
    return random.choice(selections)

async def dice_roll(times, head, adjust=0): -> int
    '''NdN dice, if NdN is not given'''
    return times * head + adjust

async def dday(first: datetime.date, second:datetime.date): -> int
    '''Tells difference between two given dates in days'''
    return (first-second).days

async def jaegi():
    '''Get Han River's current temperature'''
    async with session.get('http://hangang.dkserver.wo.tc/') as jaegi:
        async with aiohttp.ClientSession() as session:
            return json.loads(await jaegi.text())['temp']

async def upside_dn(alnum):
    '''Prints text upside down, should be alphabet or arabic numbers'''
    alts = {'a':'ɐ', 'b':'q', 'c':'ɔ', 'd':'p', 'e':'ǝ', 'f':'ɟ', 'g':'ƃ', 'h':'ɥ', \
            'i':'ᴉ', 'j':'ɾ', 'k':'ʞ', 'l':'l', 'm':'ɯ', 'n':'u', 'o':'o', 'p':'d', \
            'q':'b', 'r':'ɹ', 's':'s', 't':'ʇ', 'u':'n', 'v':'ʌ', 'w':'ʍ', 'x':'x', \
            'y':'ʎ', 'z':'z', 1:'Ɩ', 2:'ᄅ', 3:'Ɛ', 4:'ㄣ', 5:'ϛ', 6:'9', 7:'ㄥ', 8:'8', 9:'6'}
    return ''.join
