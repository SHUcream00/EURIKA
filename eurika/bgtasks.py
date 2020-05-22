'''
discord-specific modules
more specifically, modules intended to be background tasks
'''

import discord
import aiosqlite
import json
import datetime
import asyncio
import re
from point import *
from basics import get_alarm, time_to_sec
from ext import idolmaster, azura
from essentials import translate
from ext import cuckoo

cwd = r'C:\EurikaMkIII'

async def bluebird(client):
    x = cuckoo.cuckoobird()
    async with aiosqlite.connect(cwd + '\db\EurDB.db') as db:
        async with db.execute("SELECT * FROM TwitterCache") as cursor:
            cands = await cursor.fetchall()
            try:
                while True:
                    for j in cands:
                        for i in await x.cry(ID = j[1]):
                            if j[6] == 1:
                                trans = translate('auto', 'ko')
                                em = discord.Embed(title=f'GMT {i[6]}', description=await trans.actual(i[1]), colour = discord.Colour(int(i[4],16)))
                            elif j[6] == 2:
                                trans = translate('auto', 'ko')
                                twtres = await trans.actual(i[1]) + '\n' + i[1]
                                em = discord.Embed(title=f'GMT {i[6]}', description=twtres, colour = discord.Colour(int(i[4],16)))
                            else:
                                em = discord.Embed(title=f'GMT {i[6]}', description=i[1], colour = discord.Colour(int(i[4],16)))

                            em.set_author(name = i[2], icon_url = i[3])
                            em.set_thumbnail(url=i[3].replace("_normal", ""))
                            if i[7]:
                                em.set_image(url=i[7])
                            if '|' in str(i[8]):
                                for k in str(i[8]).split('|'):
                                    await client.get_channel(int(k)).send(embed=em)
                            else:
                                await client.get_channel(int(i[8])).send(embed=em)
                    await asyncio.sleep(30)

            except Exception as e:
                print("BLUEBIRD ERROR", repr(e))
                if '503' in str(e) or '130' in str(e) or 'NoneType' in str(e) or 'database' in str(e) or '131' in str(e) or 'UnboundLocalError' in str(e):
                    print('retrying in 60 seconds')
                    await asyncio.sleep(60)
                else:
                    print('retrying in half an hour')
                    await asyncio.sleep(1800)
                client.loop.create_task(bluebird(client))
                pass

async def saryunan(client):
    try:
        channel = client.get_guild(88844446929547264).get_channel(88844446929547264)
        em = await idolmaster.deresute.kakasi()
        await channel.send(embed = em)
        em = await idolmaster.milisita.kakasi()
        await channel.send(embed = em)
        await azura.azurelane.update()
        em = discord.Embed(title='덤으로 아주라 레인 DB업데이트를 수행중입니다...', description="어쩌면 새 함선들이 발견되었을 수도 있습니다.", color=0x221277)
        await channel.send(embed=em)

    except Exception as e:
        print("SARYUNAN ERROR", repr(e))
        pass
    await asyncio.sleep(86400)
