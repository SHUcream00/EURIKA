'''
Discord-specific functions
mostly for channel management to avoid writing long blahblahs in the original file
'''

import discord
import sqlite3
import datetime
import asyncio
from point import *
from basics import get_alarm

async def codeblock(text:str):
    '''return text wrapped up in python codeblock for discord'''
    return '```python\n'+str(text)+'\n```'

async def restart_alarm(client):
    cur_alarms = await get_alarm()
    for i in cur_alarms:
        client.loop.create_task(restarted_alarm(client, *i))

async def restarted_alarm(client, *args):
    time_offset = (datetime.datetime.strptime(args[2], "%Y-%m-%d %H:%M:%S") - datetime.datetime.now()).total_seconds()
    channel = client.get_channel(args[4])
    user = await client.fetch_user(args[1])
    await asyncio.sleep(time_offset)
    await channel.send("{}, 알람 종료야".format(user.mention, args[3]))

async def get_info(username, joinchan):
    '''Get current shupoint, created date, joined date to show together.'''
    spem = await sp.showpoint(author=message.author, phase='0')
    em = spem[0]
    em.add_field(name='생성일', value= str(message.author.created_at).split()[0])
    em.add_field(name='가입일', value= str(message.author.joined_at).split()[0])
    em.set_thumbnail(url=message.author.avatar_url)
    await client.send_message(message.channel, embed=em)
