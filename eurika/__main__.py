
'''

EURIKA main Driver
:copyright: (c) 2009-2020 SHUcream00
Requirement:
Python 3.7 or up, discord-py, BeautifulSoup4, pil

'''

import os
import aiohttp
import asyncio
import discord
#from discord.ext import tasks, commands

from basics import *
from weatherkr import get_area_code, jindo2
#from images import *
from point import sp
#from ext import ark, pbm
import concurrent.futures
from weatherkr import weatherf as wt

client = discord.Client()


@client.event
async def on_raw_reaction_add(payload):
    '''set up tutorial'''
    tutorial_channel = 703120166069731358
    tutorial_notice = 703736091961983028
    tutorial_guild = 88844446929547264

    if (payload.guild_id, payload.channel_id, payload.message_id) \
       == (tutorial_guild, tutorial_channel, tutorial_notice):

        tutorial_guild = client.get_guild(payload.guild_id)

        possible_roles = tutorial_guild.roles

        tutorial_ok = '👍' #:thumbs_up:
        tutorial_e = '🇪' #:regional_indicator_e:
        tutorial_j = '🇯' #:regional_indicator_j:
        tutorial_k = '🇰' #:regional_indicator_k:

        tutorial_text = ""
        if payload.emoji.name == tutorial_ok:
            newb = [].append(tutorial_guild.get_role(491410064838623232))
            await client.get_guild(payload.guild_id)\
            .get_member(payload.member.id)\
            .edit(newb)
            tutorial_text = "보지털"
        elif payload.emoji.name == tutorial_e:
            tutorial_text = "운지"
        elif payload.emoji.name == tutorial_j:
            tutorial_text = "아 섹스하고싶다!!!"
        elif payload.emoji.name == tutorial_k:
            tutorial_text = "나는자연인이다!!!"

        await client.get_channel(88844446929547264).send(tutorial_text)


master_id = 87776601239982080

@client.event
async def on_message(msg):
    '''
    Don't answer to own call
    '''
    if msg.author == client.user:
        return

    if msg.content.startswith("nimda"):
        if msg.author.id != master_id: return
        else:
            if msg.content.startswith("=ACAV"):
                '''changes profile image'''
                tgt = msg.content.split()[1]
                async with aiohttp.ClientSession() as session:
                    async with session.get(tgt) as resp:
                        indata = await resp.read()
                await client.user.edit(avatar=indata)
                await msg.channel.send("It shall be done")

    if msg.content.startswith('Memory'):
        if msg.count(chr(32)) < 2: pass #raiseerror
        else: await msg.channel.send()

    if msg.content.startswith('섹스'):
        await msg.channel.send("섹스!")

    if msg.content.startswith('Dice'):
        pass

    if msg.content.startswith('=날씨'):
        try:
            if len(msg.content.split()) == 3:
                country, city = msg.content.split()[1], msg.content.split()[2]
            else:
                country, city = msg.content.split()[1], ""

            def stringfy_w_res(date):
                res = ''
                for i in weather_text[date]:
                    temp = "**{}시** | {}°C, {}\n 습도 {}% 강수 {}%\n".format(i[0], i[2], emojify_wt(i[1]), i[3], i[4])
                    res += temp
                return res

            def emojify_wt(wtstring):
                return wtstring.replace("맑음",":sunny:").replace("흐림",":cloud:").replace("구름많음",":cloud:").replace("비",":cloud_rain:")

            weather = wt()
            weather_text = await weather.jindo3(await weather.get_area_code(country, city))
            praise_sun = "https://cdn.discordapp.com/attachments/88844446929547264/706440056671436830/Praise-the-Sun.png"

            today = datetime.date.today()
            today_str = today.strftime('%Y%m%d')
            tmr_str, twod_str = (today + datetime.timedelta(days=1)).strftime('%Y%m%d'), (today + datetime.timedelta(days=2)).strftime('%Y%m%d')
            em = discord.Embed(title="{} | {}°C, {} 습도 {}%".format(country+ " " + city, weather_text[today_str][0][2], emojify_wt(weather_text[today_str][0][1]), weather_text[today_str][0][3]),
                               description = "오늘 최고기온 {}°C 최저기온 {}°C :umbrella2: 강수 {}%".format(weather_text['maxTmpr'][0], weather_text['minTmpr'][0], weather_text[today_str][0][4]),
                               colour=0x07ECBA)

            if weather_text.get(today_str, False):
                em.add_field(name='오늘', value= stringfy_w_res(today_str))
            em.add_field(name='내일', value= stringfy_w_res(tmr_str))

            em.set_thumbnail(url=praise_sun)

            await msg.channel.send_message(embed=em)
        except:

            await msg.channel.send_message("ㅗ")

    if msg.content.startswith('=빠따'):
        def codeblock(text):
            '''return text wrapped up in python codeblock for discord'''
            return '```python\n'+str(text)+'\n```'

        jotkey = "https://cdn.discordapp.com/attachments/88844446929547264/706777124601856030/asdf_400x400.png"
        kbo_res = await kbo()

        text = ''
        for i in kbo_res:
            text += "**{} {} :regional_indicator_v: :regional_indicator_s: {} {} ** {} [**문자중계**]({})".format(i['etc'][3], i['etc'][5], i['etc'][10],i['etc'][8],i['start_time'],i['문자중계'])
            text += codeblock("\n[{}] {} VS {} [{}] \n".format(i['etc'][3], i['etc'][2].split(chr(58))[1], i['etc'][7].split(chr(58))[1], i['etc'][8]))
            #em.add_field(name="**{} vs {}**".format(i['etc'][3],i['etc'][8]), value="[**문자중계**]({})".format(i['문자중계']))
        em = discord.Embed(title=":baseball: 오늘의 상위리그", description=text, colour=0x07ECBA)

        em.set_thumbnail(url=jotkey)
        await msg.channel.send(embed=em)

    if msg.content.startswith(chr(45)):
        '''SIG driver, help users print meme images without big effort'''
        if 'random' not in message.content.split('-')[1].replace(' ', ''):
            sigret = await sig_n(msg.content.split('-')[1])
        else:
            sigret = await randsig_n()

        if sigret == None:
            return
        else:
            if sigret[1] not in [None, '']:
                em = discord.Embed(colour=0x07ECBA)
                em.set_author(name = sigret[2])
                em.set_image(url=sigret[1])
                await client.send_message(msg.channel, embed=em)
            else:
                filelink = await client.send_file(message.channel, sigret[0], content=sigret[2])
                await updatesig_n(filelink.attachments[0]['url'], sigret[2])

@client.event
async def on_ready():
    #client.loop.create_task(bluebird())
    #client.loop.create_task(saryunan())
    #client.loop.create_task(mandubird())
    print('Eurika Activated')
    print(client.user.name)
    print('--------------------------')
'''
class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # create the background task and run it in the background
        self.bg_task = self.loop.create_task(self.my_background_task())

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def my_background_task(self):
        await self.wait_until_ready()
        counter = 0
        channel = self.get_channel(1234567) # channel ID goes here
        while not self.is_closed():
            counter += 1
            await channel.send(counter)
            await asyncio.sleep(60) # task runs every 60 seconds
'''

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    token = ""
    loop.run_until_complete(client.start(token, bot=True, reconnect=True))
