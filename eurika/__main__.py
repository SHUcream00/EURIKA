
'''

EURIKA main Driver
:copyright: (c) 2009-2020 SHUcream00
Requirement:
Python 3.7 or up, discord-py, BeautifulSoup4, pil

'''

import os
from bs4 import BeautifulSoup as bs
import aiohttp
import asyncio
import discord
#from discord.ext import tasks, commands

import sqlite3

from basics import *
from images import *
from ext import ark, pbm 

client = discord.Client()

@client.event
async def on_message(msg):
    '''
    Don't answer to own call
    '''
    if msg.author == client.user:
        return

    if msg.startswith('Memory'):
        if msg.count(chr(32)) < 2: pass #raiseerror
        else: msg.channel.send()

    if msg.startswith('Dice'):


@client.event
async def on_ready():
    #client.loop.create_task(bluebird())
    #client.loop.create_task(saryunan())
    #client.loop.create_task(mandubird())
    print('Eurika Activated')
    print(client.user.name)
    print('--------------------------')

#client.run(id)

print(rand_select([1,2,3,4,5]))
