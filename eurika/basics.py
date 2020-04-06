import re
import random
import datetime
import aiohttp
import ast
from math import *

#__import__('os').system('rm -rf /dir')

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

#print(calc("1+2+32"))
#print(calc("32 // 5"))
print(calc("tan(60)"))
#print(calc("pi"))
#print(calc("inf"))
