import random
import asyncio
import aiohttp
import math

from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def reallength(*args, **kwargs):
    size = ImageFont.truetype('NtreevSoft.ttf', 17).getsize(args[0])
    return size[0]

async def randomstats(**kwargs):
    stats = []

    if str(kwargs['user'].id) in ['470379253721202691', '90092507211243520']:
        jp = 200

    else:
        #age = int(await eurikabasics.ddayraw(str(kwargs['user'].joined_at).split(' ')[0].split('-')))
        #age2 = int(await eurikabasics.ddayraw(str(kwargs['server'].created_at).split(' ')[0].split('-')))
        jp = math.floor(round(age / age2, 2) * 100) - 1

    if jp < 0:
        stats.append(0)
    else:
        stats.append(jp)

    for i in range(6):
        stats.append(random.randint(1,120))

    return stats

async def pbm(*args, **kwargs):
    #variables

    altimg = "C:\EurikaMkIII\\resources\\pbm\\iriya.gif"

    #card backgrounds
    csel = kwargs['cardtypes']
    csela = random.choice(csel)
    result = Image.new("RGB", (228, 317))
    result.thumbnail((228, 317), Image.ANTIALIAS)
    img = Image.open("C:\EurikaMkIII\\resources\\pbm\\{}\\bg.png".format(csela))
    result.paste(img, (0, 0, 228, 317))
    layer = Image.new("RGB", (228, 317))
    if csela not in ['potential']:
        layer.paste(kwargs['color'], (0, 0, 228, 317)) #104 255 182 mint
        layer.putalpha(128)
        result.paste(layer, (0, 0, 228, 317), layer)

    #avatar background
    avbg = Image.new("RGBA",  (185, 185), (255,255,255,0))
    bgdim = 165
    draw = ImageDraw.Draw(avbg)
    draw.ellipse((10,10,175,175), fill=(0,0,0))
    avbg = avbg.filter(ImageFilter.GaussianBlur(radius=3))
    result.paste(avbg, (int((228-bgdim)/2) - 10, 6), avbg)

    #avatar et its mask
    if kwargs['target'] == None:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(kwargs['user'].avatar_url) as resp:
                    raw = await resp.read()
                    img = Image.open(BytesIO(raw))
        except:
            img = Image.open(altimg)
    else:
        img = Image.open(kwargs['target'])
    img = img.resize((150, 150), Image.ANTIALIAS)
    bigsize = (img.size[0] * 3, img.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=3))
    mask = mask.resize(img.size, Image.ANTIALIAS)
    img.putalpha(mask)
    result.paste(img, (38, 23), img)

    #card form
    img = Image.open("C:\EurikaMkIII\\resources\\pbm\\{}\\1st layer.png".format(csela))
    result.paste(img, (0, 0, 228, 317), mask=img)
    if csela == 'normal':
        layer = Image.new("RGBA", (228, 317))
        mask = Image.new('L', (228, 317), 0)
        mask.paste(Image.open("C:\EurikaMkIII\\resources\\pbm\\{}\\linemask.png".format(csela)))
        mask = mask.filter(ImageFilter.SMOOTH)
        layer.paste(kwargs['color'], (0, 0, 228, 317))
        layer.putalpha(mask)
        result.paste(layer, (0, 0, 228, 317), layer)

     #condition
    condition = random.randint(0,5)
    img = Image.open("C:\EurikaMkIII\\resources\\pbm\\conditions\\{}.png".format(str(condition)))
    result.paste(img, (13, 127), img)

    #name and team logo
    txt = Image.new('RGBA', result.size, (255,255,255,0))
    cnamlen = reallength(kwargs['user'].name)
    if len(kwargs['user'].name) < 8:
        cname = kwargs['user'].name
    else:
        cname = kwargs['user'].name[:9]

    if csela == 'gg':
        cnamsloc = (math.ceil(116 - cnamlen / 2), 170)
        cnamlocx = math.ceil(114 - cnamlen / 2)
        cnamlocy = 168
        cnamfil = (244,242,159,255)
        logoloc = (3, 170)
        fnt = ImageFont.truetype('NtreevSoft.ttf', 17)
        d = ImageDraw.Draw(txt)
        d.text((10,10), cname, font=fnt, fill=(0,0,0,196))
        result.paste(txt, cnamsloc, txt)
    else:
        cnamlocx = math.ceil(114 - cnamlen / 2)
        cnamlocy = 174
        logoloc = (7, 174)
        if csela in ['normal', 'potential', 'franchise', 'live', 'live1']:
            cnamfil = (255,255,255,255)
        else:
            cnamfil = (0,0,0,255)
    fnt = ImageFont.truetype('NtreevSoft.ttf', 17)
    d = ImageDraw.Draw(txt)
    d.text((10,10), cname, font=fnt, fill=cnamfil)
    result.paste(txt, (cnamlocx, cnamlocy), txt)
    img = Image.open("C:\EurikaMkIII\\resources\\pbm\\yagall.png")
    result.paste(img, logoloc, img)

    #stats - actual
    statloc = [(51, 222 + 0 * 12), (51, 222 + 1 * 12), (51, 222 + 2 * 12), (51, 222 + 2 * 12 + 11), (51, 222 + 3 * 12 + 11), (51, 222 + 4 * 12 + 11)]
    if kwargs['pbm'] == 1:
        stats = await randomstats(user = kwargs['user'], server=kwargs['server'])
    else:
        stats = [1,1,1,1,1,1]

    #stats - bar
    for i in range(6):
        bar = Image.new('L',(stats[i], 5), color=255)
        bar = bar.resize(bar.size, Image.ANTIALIAS)
        result.paste(bar, statloc[i], bar)

    #stats - stat name and number
    sname = kwargs['statlist']
    txt = Image.new('RGBA', result.size, (255,255,255,0))
    fnt = ImageFont.truetype('NtreevSoft.ttf', 10)
    d = ImageDraw.Draw(txt)
    for i in range(6):
         d.text((10, 10 + i * 12), sname[i], font=fnt, fill=(255,255,255,255))
         if stats[i] in range(110,121):
             d.text((177, 10 + i * 12), str(stats[i]), font=fnt, fill=(140,24,178,255))
         elif stats[i] in range(90, 110):
             d.text((177, 10 + i * 12), str(stats[i]), font=fnt, fill=(160,34,22,255))
         elif stats[i] in range(80, 90):
             d.text((177, 10 + i * 12), str(stats[i]), font=fnt, fill=(219,126,13,255))
         elif stats[i] in range(70, 80):
             d.text((177, 10 + i * 12), str(stats[i]), font=fnt, fill=(244,220,36,255))
         else:
             d.text((177, 10 + i * 12), str(stats[i]), font=fnt, fill=(255,255,255,255))
    result.paste(txt, (5, 208), txt)

    #cost
    img_s = Image.open("C:\EurikaMkIII\\resources\\pbm\\{}\\star.png".format(csela))
    rating = math.floor(sum(stats)/66)
    if rating == 0:
        rating = 1
    for i in range(rating):
        result.paste(img_s, (58 + 12 * i, 294), img_s)
    img_r = Image.open("C:\EurikaMkIII\\resources\\pbm\\numbers\{}.png".format(str(rating)))
    result.paste(img_r, (191, 291), img_r)

    #end
    if kwargs['pbm'] == 1:
        result.save('C:\EurikaMkIII\\temp\\pbm\\{}.png'.format(kwargs['user'].id), "PNG")
    elif kwargs['pbm'] == 0:
        result.save('C:\EurikaMkIII\\temp\\pbm2\\{}.png'.format(kwargs['user'].id), "PNG")
