from bs4 import BeautifulSoup as bs
import asyncio
import aiohttp
#<ul class="sch_vs" id="todaySchedule">
#id="todaySchedule"
async def kbo():
    ns_prefix = "https://sports.news.naver.com"
    target = "https://sports.news.naver.com/kbaseball/schedule/index.nhn"
    async with aiohttp.ClientSession() as session:
        async with session.get(target) as resp:
            raw = await resp.text()

    soup = bs(raw, "lxml") #can i make it an async?
    games = soup.find_all("li", class_="before_game")

    #broadcast = a, btn_ltr
    res = []
    for i in games:
        temp, etc = {}, []
        for j in i.findChildren():
            if j.name == 'em':
                temp['start_time'] = j.text.replace("\n","").replace(chr(32),"")
            elif j.name == 'a':
                if j.get('href').startswith('http://'):
                    temp[j.text.replace("\n","").replace(chr(32),"")] = j.get('href')
                else:
                    temp[j.text.replace("\n","").replace(chr(32),"")] = ns_prefix + j.get('href')
            else:
                if len(j.get_text().replace("\n", "").replace(chr(32), "")) != 0:
                    etc.append(j.get_text().replace("\n", "").replace(chr(32), ""))
        temp['etc'] = etc
        res.append(temp)
    print(res)

if __name__ == "__main__":
    a = asyncio.get_event_loop()
    a.run_until_complete(kbo())
    #print(a.run_until_complete(x.jindo2(a.run_until_complete(x.get_area_code("대구광역시", "달성군")))))
