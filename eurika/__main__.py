'''
Requirement:
Python 3.7 or up, discord-py, BeautifulSoup4, pil

'''
import os
from bs4 import BeautifulSoup as bs
import aiohttp
import asyncio
import discord
from discord.ext import tasks, commands
from PIL import Image
import sqlite3
import eurika

client = discord.Client()

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return



@client.event
async def on_ready():
    #test2
    #client.loop.create_task(bluebird())
    #client.loop.create_task(saryunan())
    #client.loop.create_task(mandubird())
    print('Eurika Activated')
    print(client.user.name)
    print('--------------------------')

client.run(id)
