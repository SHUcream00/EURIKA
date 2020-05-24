'''
Discord-specific functions
mostly for channel management to avoid writing long blahblahs in the original file
'''

import discord
import aiosqlite
import json
import datetime
import asyncio
import re
from point import *
from basics import get_alarm, time_to_sec, codeblock
from essentials import translate
from ext import cuckoo

async def restart_alarm(client):
    cur_alarms = await get_alarm()
    for i in cur_alarms:
        client.loop.create_task(restarted_alarm(client, *i))

async def restarted_alarm(client, *args):
    time_offset = (datetime.datetime.strptime(args[2], "%Y-%m-%d %H:%M:%S") - datetime.datetime.now()).total_seconds()
    channel = client.get_channel(args[4])
    user = await client.fetch_user(args[1])
    await asyncio.sleep(time_offset)
    await channel.send(f"{user.mention}, {args[3]} 시간이야")

async def get_info(username, joinchan):
    '''Get current shupoint, created date, joined date to show together.'''
    spem = await sp.showpoint(author=message.author, phase='0')
    em = spem[0]
    em.add_field(name='생성일', value= str(message.author.created_at).split()[0])
    em.add_field(name='가입일', value= str(message.author.joined_at).split()[0])
    em.set_thumbnail(url=message.author.avatar_url)
    await client.send_message(message.channel, embed=em)

async def shinan(client, msg, timestring, target):
    em = discord.Embed(title=f'천사의 섬 행 비행기가 출발하는구리!'
                    , description= f'{target.mention}, {timestring}동안 잘 지내는구리', colour=0x07ECBA)
    await msg.channel.send(embed=em)
    seconds = await time_to_sec(timestring)
    prv_roles = target.roles
    roles = []
    roles.append(client.get_guild(88844446929547264).get_role(295021155042197514))
    await target.edit(roles=roles)
    await asyncio.sleep(seconds)
    await target.edit(roles=prv_roles)
    em = discord.Embed(title=f'훌륭한 염전노예가 귀환한구리!'
                    , description= f'{target.mention}, 잘 돌아오는구리.', colour=0x07ECBA)
    await msg.channel.send(embed=em)
    return

async def cex(amnt, cur_fr, cur_to, comp=''):
    curdict = {'원':'KRW', '위안': 'CNY', '파운드': 'GBP', '유로': 'EUR', '달러': 'USD', '엔': 'JPY', '홍콩달러': 'HKD', '레알': 'BRL',
                '캐나다달러': 'CAD', '스위스프랑': 'CHF', '인도네시아루피': 'IDR', '페소': 'MXN', '필리핀페소': 'PHP', '레우': 'RON', '크로네': 'NOK',
                '포린트': 'HUF', '쿠나': 'HRK', '즈워티': 'PLN', '루피': 'INR', '링깃': 'MYR', '크로나': 'SEK', '루블': 'RUB', '싱가포르달러': 'SGD',
                '바트': 'THB', '리라': 'TRY', '랜드': 'ZAR', '달러': 'USD'}
    cexchecker = re.compile('\d+(\.\d+)?')
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://data.fixer.io/api/latest?access_key=8572d46f86bde368626be482bc7cc50f") as cexhtml: #curdict[cur_fr]
                cexbase = json.loads(await cexhtml.text())['rates']
                basecur = curdict[cur_fr]
                if comp != '':
                    if cexchecker.match(comp):
                        if (round(float(amnt) / cexbase[curdict[cur_fr]] * cexbase[curdict[cur_to]] - float(comp),3) > 0):
                            em = discord.Embed(title=f'{amnt} {cur_fr} => {cur_to} 환전 결과 (비교 대상: {comp} {cur_to})',
                            description= f'{amnt} {cur_fr}(이)가 {str(round(float(amnt) / cexbase[curdict[cur_fr]] * cexbase[curdict[cur_to]] - float(comp),3)) + cur_to} 만큼 더 비쌈', colour = 0x07ECBA)
                        else:
                            em = discord.Embed(title=f'{amnt} {cur_fr} => {cur_to} 환전 결과 (비교 대상: {comp} {cur_to})',
                            description= f'{amnt} {cur_to}(이)가 {str(round(float(amnt) / cexbase[curdict[cur_fr]] * cexbase[curdict[cur_to]] - float(comp),3)) + cur_to} 만큼 더 비쌈', colour = 0x07ECBA)
                else:
                    res = round(float(amnt) / cexbase[curdict[cur_fr]] * cexbase[curdict[cur_to]],3)
                    em = discord.Embed(title=f'{amnt}{cur_fr} => {cur_to} 환전 결과'
                                        , description= f":money_with_wings: {res:,}{cur_to}", colour = 0x07ECBA)
                if (cur_fr == '달러' or cur_to == '달러') and (float(amnt) == 4 or str(round(float(amnt) / cexbase[curdict[cur_fr]] * cexbase[curdict[cur_to]],3)).split('.')[0] == '4'):
                    em.set_image(url='https://cdn.discordapp.com/attachments/192692517827772417/345061938901811200/7798b46504e4a060.jpg')
    except:
        em = discord.Embed(title='난토! 에러가 났네요!', description = '[예시]\n=환율 (액수) (현재화폐) (바꿀화폐)\n혹은\n=환율 (액수) (현재화폐) (바꿀화폐) (비교액수)\n[사용가능한 화폐종류]\n' + ' '.join(curdict.items()), colour=0xB5002B)
    return em
