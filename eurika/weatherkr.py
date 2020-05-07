import aiohttp
import asyncio
import json
import aiosqlite
import ast
import time
from collections import defaultdict
import xmltodict

'''weather forecast script by parsing Naver weathers'''

class weatherf():
    def __init__(self):
        cwd = r'C:\EurikaMkIII' #fallback
        self.db = cwd + "\db\Jindo2.db"

    async def recover_abbr(self, name):
        kr_abbr_dict = {'광주광역시, 광주시': '광주', '경상남도': '경남', '세종시': '세종',
                        '충청남도': '충남', '충청북도': '충북', '경기도': '경기', '대전광역시, 대전시': '대전',
                        '인천광역시, 인천시': '인천', '울산광역시, 울산시': '울산', '경상북도': '경북', '충청북도': '충북',
                        '전라북도': '전북', '대구광역시, 대구시, 머구, 머구광역시, 머구팡역시': '대구',
                        '부산광역시, 붓산, 쓰까, 부산시': '부산', '서울특별시, 서울시': '서울', '제주도': '제주',
                        '전라남도': '전남', '강원도' : '강원'}
        for i in kr_abbr_dict.keys():
            if name in i:
                return kr_abbr_dict[i]

        return name

    async def get_area_code(self, county, city = ""):
        '''Finds the given area code'''
        top_region_dict = {'광주': '05', '경남': '03', '세종': '17',
                        '충남': '15', '대전': '07', '인천': '11', '경기': '02',
                        '울산': '10', '경북': '04', '충북': '16', '전북': '13',
                        '대구': '06', '부산': '08', '서울': '09', '제주': '14', '전남': '12', '강원': '01'}

        county = await self.recover_abbr(county)
        city_text = city
        if city != "" and (city[-1] in ["시", "군"]):
            city_text = city[:len(city)-1]

        async with aiosqlite.connect(self.db) as db:
            region_text = (county+city_text).replace(chr(32), "")
            async with db.execute("SELECT * FROM NaverRegions WHERE Name='"+region_text+"' COLLATE NOCASE") as cursor:
                entry = await cursor.fetchone()

            if entry:
                return entry[0]
            else:
                if county in top_region_dict.keys():
                    temp = "https://weather.naver.com/json/rgnCat.nhn?_callback=window.__jindo2_callback._6128&m=naverRgnCat&upperRgnCd={}"
                    async with aiohttp.ClientSession() as session:
                        async with session.get(temp.format(top_region_dict[county])) as resp:
                            raw = await resp.text()
                            city_data = json.loads(raw[raw.index(chr(40))+1:raw.index(chr(41))])
                            city_dict = {i['rgnNm']: i['rgnCd'] for i in city_data['rgnList']}

                    if city == "":
                        city = list(city_dict.keys())[0]

                    if city in city_dict.keys():
                        async with aiohttp.ClientSession() as session:
                            async with session.get(temp.format(city_dict[city])) as resp:
                                raw = await resp.text()
                                city_data = json.loads(raw[raw.index(chr(40))+1:raw.index(chr(41))])

                        await db.execute("INSERT INTO NaverRegions (region_code, name) VALUES ('"+city_data['rgnList'][0]['rgnCd']+"', '"+region_text+"')")
                        await db.commit()

                        return city_data['rgnList'][0]['rgnCd']


    async def jindo2(self, loc = "09710566"):
        '''Get the actual forecast data'''
        #alt = https://weather.naver.com/flash/naverRgnTownFcast.nhn?m=jsonResult&naverRgnCd=12910350 # 3 hours
        temp = "https://weather.naver.com/json/crntWetrDetail.nhn?_callback=window.__jindo2_callback._902&naverRgnCd={}"

        async with aiosqlite.connect(self.db) as db:
            async with db.execute("SELECT * FROM NaverRegions WHERE region_code='"+loc+"' COLLATE NOCASE") as cursor:
                entry = await cursor.fetchone()

            if entry[2] != time.strftime('%Y-%m-%d %H'):
                async with aiohttp.ClientSession() as session:
                    async with session.get(temp.format(loc)) as resp:
                        raw = await resp.text()
                        await db.execute("UPDATE NaverRegions SET last_checked=?, cache=? Where region_code=?", (time.strftime('%Y-%m-%d %H'), raw, loc))
                        await db.commit()

            else:
                raw = entry[3]

        w_data = json.loads(raw[raw.index(chr(40))+1:raw.index(chr(41))])

        res = {}
        res['region_name'] = "{} {}".format(w_data['wetrMap'][1][1]['lareaNm'], w_data['wetrMap'][1][1]['mareaNm'])
        w_rgnname = "{} {}".format(w_data['wetrMap'][1][1]['lareaNm'], w_data['wetrMap'][1][1]['mareaNm'])

        temp = w_data['wetrMap'][1][1]
        res['cur_text'] = temp['wetrTxt']
        res['cur_rain'] = temp['rainAmt']
        res['cur_snow'] = temp['snowAmt']
        res['cur_temp'] = temp['tmpr']
        res['cur_delta'] = temp['ytmpr']
        res['today_mntext'] = w_data['wetrMap'][2][1][0]['amWeatherText']
        res['today_mntemp'] = w_data['wetrMap'][2][1][0]['amTemperature']
        res['today_mnrainpos'] = w_data['wetrMap'][2][1][0]['amRainProbability']
        res['today_antext'] = w_data['wetrMap'][2][1][0]['pmWeatherText']
        res['today_antemp'] = w_data['wetrMap'][2][1][0]['pmTemperature']
        res['today_anrainpos'] = w_data['wetrMap'][2][1][0]['pmRainProbability']
        res['tmr_mntext'] = w_data['wetrMap'][2][1][1]['amWeatherText']
        res['tmr_mntemp'] = w_data['wetrMap'][2][1][1]['amTemperature']
        res['tmr_mnrainpos'] = w_data['wetrMap'][2][1][1]['amRainProbability']
        res['tmr_antext'] = w_data['wetrMap'][2][1][1]['pmWeatherText']
        res['tmr_antemp'] = w_data['wetrMap'][2][1][1]['pmTemperature']
        res['tmr_anrainpos'] = w_data['wetrMap'][2][1][1]['pmRainProbability']

        return res

    async def jindo3(self, loc):
        '''Get the actual forecast data - better one'''
        temp = "https://weather.naver.com/flash/naverRgnTownFcast.nhn?naverRgnCd={}"

        async with aiosqlite.connect(self.db) as db:
            async with db.execute("SELECT * FROM NaverRegions WHERE region_code='"+loc+"' COLLATE NOCASE") as cursor:
                entry = await cursor.fetchone()

            if entry[2] != time.strftime('%Y-%m-%d %H'):
                async with aiohttp.ClientSession() as session:
                    async with session.get(temp.format(loc)) as resp:
                        raw = await resp.text()
                        await db.execute("UPDATE NaverRegions SET last_checked=?, cache=? Where region_code=?", (time.strftime('%Y-%m-%d %H'), str(raw), loc))
                        await db.commit()

            else:
                raw = entry[3]

        w_data = xmltodict.parse(raw)['message']['result']['townWetrFeed']

        res = defaultdict(list)
        for i in map(lambda x: (x['ymd'], x['hh'], x['wetrTxt'], x['tmpr'], x['humd']), w_data['townWetrs']['townWetr']):
            res[i[0]].append(i[1:])

        res['maxTmpr'].append(w_data['maxTmpr'])
        res['minTmpr'].append(w_data['minTmpr'])

        return
'''
if __name__ == "__main__":
    x = weatherf()
    a = asyncio.get_event_loop()
    #print(a.run_until_complete(x.jindo3(a.run_until_complete(x.get_area_code("서울", "강남구")))))
    #print(a.run_until_complete(x.jindo3(a.run_until_complete(x.get_area_code("대구광역시", "달성군")))))
    #print(a.run_until_complete(x.jindo3(a.run_until_complete(x.get_area_code("대구시")))))
    #print(a.run_until_complete(x.jindo3(a.run_until_complete(x.get_area_code(" 대구")))))
    print(a.run_until_complete(x.jindo3(a.run_until_complete(x.get_area_code("서울시")))))
'''
