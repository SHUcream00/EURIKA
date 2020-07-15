
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
from dscspec import *
from weatherkr import weatherf as wt
#from images import *
from point import sp
#from ext import ark, pbm
import concurrent.futures
from kbotoday import kbo

client = discord.Client()
client.init_switch = True
cwd = r'C:\EurikaMkIII'

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

#===========================================================================================================
#Channel management
    if msg.content.startswith("=닉"):
        try:
            split = msg.content.split(chr(32), 1)
            if len(split) == 1:
                em = discord.Embed(description="닉 바꿔주는 간이기능.\n[예시]=닉 알바성기", color=color_def)
                await msg.channel.send(embed=em)
            else:
                em = discord.Embed(description=f"닉 변경 완료.\n{msg.author.display_name} => {split[1]}", color=color_def)
                await msg.author.edit(nick=split[1])
                await msg.channel.send(embed=em)
        except Exception as e:
            print("NICKCHANGE ERROR", repr(e))

    if msg.channel.id in [92580086091366400, 360591565112082443, 509321410053799937, 732039740030844989]:
        if (len(msg.attachments) == 0 or msg.author.id == client.user.id) and str(msg.content).split(".")[msg.content.count(".")] not in ["png", "jpg", "gif", "mp4", "mov", "webm", "webp", "gifv"]:
            await msg.delete()

#===========================================================================================================
    if msg.content.startswith("=아주라"):
        await azura.azurelane.update()

#===========================================================================================================

    if msg.content.startswith("=계산"):
        try:
            ctx = "".join(msg.content.split(chr(32), 1)[1])
            res = await calc(ctx)
            em = discord.Embed(description=f"{await blueblock(f'[주어진 수식: {ctx}]')}{await codeblock(f'{res:,}')}", color=color_def)
            em.set_author(name = f"{client.user.display_name} 계산 서비스", icon_url=client.user.avatar_url)
            await msg.channel.send(embed=em)

        except Exception as e:
            print("CALC ERROR", repr(e))
            em = discord.Embed(description="왜구련아.", color=color_err)
            em.set_author(name = f"{client.user.display_name} 계산 서비스", icon_url=client.user.avatar_url)
            await msg.channel.send(embed=em)


    if msg.content.startswith("=선택"):
        try:
            ctx = str(await rand_select(msg.content.split()[1:]))
            em = discord.Embed(description="ㅤ\n**{}**\nㅤ".format(ctx.center(13, "ㅤ")), color=color_def)
            em.set_footer(text=f"{client.user.display_name}님의 선택")
            em.set_thumbnail(url=client.user.avatar_url)
            await msg.channel.send(embed=em)

        except Exception as e:
            print("RANDSELECT ERROR", repr(e))
            pass

    if msg.content.startswith("=우선순위"):
        try:
            ctx = await ordered_select(msg.content.split()[1:])
            em = discord.Embed(description=f"ㅤ\n**{ctx.center(20, 'ㅤ')}**\nㅤ", color=color_def)
            em.set_footer(text=f"{client.user.display_name}님의 선택")
            em.set_thumbnail(url=client.user.avatar_url)
            await msg.channel.send(embed=em)

        except Exception as e:
            print("ORDSELECT ERROR", repr(e))
            pass

    if msg.content.startswith("=명령"):
        em = discord.Embed(description=f"[유리카 커맨드 리스트](https://eurika.readthedocs.io/en/latest/)", color=color_def)
        await msg.channel.send(embed=em)


    if msg.content.startswith('Memory'):
        if msg.count(chr(32)) < 2:
            pass #raiseerror
        else:
            await msg.channel.send()

    if msg.content.startswith('Dice'):
        pass


    if msg.content == '=포인트랭킹':
        spem = await sp.showrank(client)
        await msg.channel.send(embed=spem)

    if msg.content == '=힐러리랭킹':
        spem = await sp.showhrank(client)
        await msg.channel.send(embed=spem)

    if msg.content == '=힐러리전당':
        spem = await sp.showhlegend(client)
        await msg.channel.send(embed=spem)

    if msg.content == '=카드':
        #loop = asyncio.get_event_loop()
        #with concurrent.futures.ProcessPoolExecutor() as pool:
        await pbm.maker(user=msg.author, server=msg.guild, color=msg.author.colour.to_rgb(),
              cardtypes = ['gg', 'normal', 'ex', 'allstar', 'rare', 'classic', 'franchise', 'legend', 'legendold', 'live', 'potential', 'live1'],
              statlist = ['적폐력', '페도력', '홍어력', '네덕력', '통베력', '한남력'],
              pbm = 1,
              target = None)

        await msg.channel.send(file=discord.File(f'C:\EurikaMkIII\\temp\\pbm\\{msg.author.id}.png'))

    if msg.content.startswith('=2알람'):
        try:
            alarm_amt = msg.content.split()[1:]
            if alarm_amt[0] == "리스트":
                alarm_list = await get_alarm(msg.author.id)
                await msg.channel.send("\n".join(map(lambda x: "예정시각: {}, 남은시간: {} 메모: {}".format(x[2],x[6],x[3])
                                                                                                , sorted(alarm_list, key=lambda x: x[2])))
            else:
                await msg.channel.send("{}, 시간이 되면 알려줄게!".format(msg.author.display_name))
                await alarm(msg.author.id, *alarm_amt, channel=msg.channel.id, server=msg.guild.id)
                await msg.channel.send("{}, 알람 종료야".format(msg.author.mention))
        except:
            await msg.channel.send("=알람 시간 메모")

    if msg.content.startswith('=영역') or msg.content.startswith('=trans'):
        if len(msg.content.split()) != 1:
            target_text = msg.content.split(' ', 1)[1]
            if translate.detect_korean(target_text) == 1:
                trans = translate('auto', 'en')
            else:
                trans = translate('auto', 'ko')

            em = discord.Embed(title='주어진 텍스트의 번역 결과입니다.', description = await trans.actual(target_text), colour=0x07ECBA)
            await msg.channel.send(embed=em)

        else:
            em = discord.Embed(title='영역 스크립트입니다.', description = '주어진 문장이 한국어면 영어로, 나머지는 한국어로 고칩니다.', colour=0x07ECBA)
            await msg.channel.send(embed = em)


    #Getchu module
    if msg.content.startswith('=겟츄'):
        try:
            linked = ["[{}]({})".format(i,j) for i,j in await gclister(msg.content.split()[1])]
            em = discord.Embed(description="\n".join(linked), colour=0xff9fde)
            em.set_author(name = f'[GETCHU] {msg.content.split()[1]}랭킹', icon_url = 'http://www.getchu.com/common/images/logo_com10th_1.gif')
            em.set_image(url='http://www.eukleia.co.jp/eushully/eu20/twitter/twitter_headereu20.jpg')
            await msg.channel.send(embed=em)
        except:
            em = discord.Embed(title='GETCHU의 현 예약, 선호, 매출 등 랭킹을 확인 가능한 스크립트야.', description= '=겟츄 예약\n' \
                   +'현 시점의 예약 랭킹이야. \n' \
                   +'\n' \
                   +'=겟츄 매출\n' \
                   +'현 시점의 주간 매출 랭킹을 보여줘 \n' \
                   +'\n' \
                   +'=겟츄 액세스\n' \
                   +'지난 24시간 내에 많은 사람들이 열람한 야겜 제품의 랭킹이야.\n' \
                   +'\n' \
                   +'=겟츄 선호작\n' \
                   +'가장 많은 사람들이 선호작으로 등록한 야겜의 랭킹이야. \n' \
                   +'\n' \
                   +'=겟츄 연간\n' \
                   +'지난해에 가장 많이 팔린 야겜의 랭킹이야. \n' \
                   +'\n' \
                   ,colour=0xff9fde)
            em.set_author(name="=겟츄 명령어 가이드북", icon_url='http://www.getchu.com/common/images/logo_com10th_1.gif')
            await msg.channel.send(embed=em)

    #Alarm module
    if msg.content.startswith('=알람'):
        #try:
        alarm_amt = msg.content.split()[1:]
        if alarm_amt[0] == "리스트":
            alarm_list = await get_alarm(msg.author.id)

            em = discord.Embed(title = f"{msg.author.display_name}의 알람리스트"
                                ,description = await codeblock ("\n".join(map(lambda x: f"{x[2]}에 {x[3]}알리기.\n잔여시간 앞으로... {x[6]}"
                                    , sorted(alarm_list, key=lambda x: x[2]))))
                                    , color = 0x07ECBA)
            em.set_thumbnail(url=msg.author.avatar_url)
            await msg.channel.send(embed = em)

        else:
            await msg.channel.send(f"{msg.author.display_name}, 시간이 되면 알려줄게!")
            await alarm(msg.author.id, alarm_amt[0], chr(32).join(alarm_amt[1:]), channel=msg.channel.id, server=msg.guild.id)
            await msg.channel.send(f"{msg.author.mention}, {' '.join(alarm_amt[1:])}시간이야")
        '''
        except:
            await msg.channel.send("=알람 시간 메모")'''

    #KRWeather module
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

            if weather_text.get(today_str, False):
                em = discord.Embed(title="{} | {}°C, {} 습도 {}%".format(country+ " " + city, weather_text[today_str][0][2], emojify_wt(weather_text[today_str][0][1]), weather_text[today_str][0][3]),
                                   description = "오늘 최고기온 {}°C 최저기온 {}°C :umbrella2: 강수 {}%".format(weather_text['maxTmpr'][0], weather_text['minTmpr'][0], weather_text[today_str][0][4]),
                                   colour=0x07ECBA)
            else:
                #21~24
                em = discord.Embed(title="{} | {}°C, {} 습도 {}%".format(country+ " " + city, weather_text[tmr_str][0][2], emojify_wt(weather_text[tmr_str][0][1]), weather_text[tmr_str][0][3]),
                                   description = "오늘 최고기온 {}°C 최저기온 {}°C :umbrella2: 강수 {}%".format(weather_text['maxTmpr'][0], weather_text['minTmpr'][0], weather_text[tmr_str][0][4]),
                                   colour=0x07ECBA)

            if weather_text.get(today_str, False):
                em.add_field(name='오늘', value= stringfy_w_res(today_str))
            em.add_field(name='내일', value= stringfy_w_res(tmr_str))

            em.set_thumbnail(url=praise_sun)

            await msg.channel.send(embed=em)

        except Exception as e:
            print("WEATHER ERROR", repr(e))
            em = discord.Embed(title="에러가 발생했어요", description="[사용법] **=날씨 지역명**\n :exclamation: 지역명은 군/구 단위까지만 가능!", color=color_err)
            await msg.channel.send(embed=em)

    #Youtube module 200524
    if msg.content.startswith('=유튜브'):
        #try:
        args = msg.content.split()
        if len(args) >= 2:
            res = ""
            string = " ".join(args[1:])
            videos = await youtube_vid(query=string, max=5)
            for i in videos[:5]:
                res += f"[{i['snippet']['title'][:25] + '...'}]({'https://www.youtube.com/watch?v=' + i['id']['videoId']})\n"\
                        + f":tv: [**{i['snippet']['channelTitle']}**]({'https://www.youtube.com/channel/' + i['snippet']['channelId']}) on {i['snippet']['publishedAt'].split('T')[0]}\n\n"
            em = discord.Embed(title=string, description=res, color=0xFF0000)
            em.set_image(url=videos[0]['snippet']['thumbnails']['high']['url'])
            em.set_author(name="YouTube on EURIKA", icon_url = "https://cdn.discordapp.com/attachments/695373167627337859/714386374899400734/3721679-youtube_108064.png")
            await msg.channel.send(embed = em)

        '''
        except Exception as e:
            print("Youtube Error:", repr(e))
        '''


    #New Baseball Score module 200605
    if msg.content.startswith('=빠따'):
        jotkey = "https://cdn.discordapp.com/attachments/88844446929547264/706777124601856030/asdf_400x400.png"
        kbo_res = await kbo2()

        text = ''
        for i in kbo_res:
            if i.get("score", False) or i['start_time'] in ["종료", "경기취소"]:
                if i['start_time'] == "종료":
                    text += f"**{i['etc'][0]}ㅤ{i['score'][0]}ㅤ:regional_indicator_v: :regional_indicator_s:ㅤ{i['score'][1]}ㅤ{i['etc'][2]} ** ㅤㅤ**경기 종료**"
                    text += await codeblock(f"\n[{i['etc'][0]}] {i['etc'][1]} VS {i['etc'][3]} [{i['etc'][2]}] \n")
                elif i['start_time'] == "경기취소":
                    text += f"**{i['etc'][0]}ㅤ0ㅤ:regional_indicator_v: :regional_indicator_s:ㅤ0ㅤ{i['etc'][2]} ** ㅤㅤ**경기 취소**"
                    text += await codeblock(f"\n[{i['etc'][0]}] {i['etc'][1]} VS {i['etc'][3]} [{i['etc'][2]}] \n")
                else:
                    text += f"**{i['etc'][0]}ㅤ{i['score'][0]}ㅤ:regional_indicator_v: :regional_indicator_s:ㅤ{i['score'][1]}ㅤ{i['etc'][2]} **ㅤ{i['start_time']} ㅤㅤ[**문자**]({i['문자']})ㅤ[**TV**]({i['TV']})"
                    text += await codeblock(f"\n[{i['etc'][0]}] {i['etc'][1]} VS {i['etc'][3]} [{i['etc'][2]}] \n")
            else:
                if len(i['etc']) >= 4:
                    text += f"**{i['etc'][0]}ㅤㅤ:regional_indicator_v: :regional_indicator_s:ㅤㅤ{i['etc'][2]} **ㅤ{i['start_time']} ㅤㅤ[**전력분석**]({i['전력']})"
                    text += await codeblock(f"\n[{i['etc'][0]}] {i['etc'][1]} VS {i['etc'][3]} [{i['etc'][2]}] \n")
                else:
                    text += f"**{i['etc'][0]}ㅤㅤ:regional_indicator_v: :regional_indicator_s:ㅤㅤ{i['etc'][1]} **ㅤ{i['start_time']} ㅤㅤ[**전력분석**]({i['전력']})"
                    text += await codeblock(f"\n[{i['etc'][0]}] 미정 VS 미정 [{i['etc'][1]}] \n")

        em = discord.Embed(title=":baseball: 오늘의 상위리그", description=text, colour=0x07ECBA)

        em.set_thumbnail(url=jotkey)
        await msg.channel.send(embed=em)


    if msg.content.startswith(chr(45)):
        '''SIG driver, help users print meme images without big effort'''
        if 'random' not in msg.content.split('-')[1].replace(' ', ''):
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
                filelink = await client.send_file(msg.channel, sigret[0], content=sigret[2])
                await updatesig_n(filelink.attachments[0]['url'], sigret[2])

@client.event
async def on_ready():
    if client.init_switch == True:
        client.loop.create_task(bluebird())
        client.loop.create_task(saryunan())
        client.loop.create_task(restart_alarm(client))
        client.init_switch = False
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
