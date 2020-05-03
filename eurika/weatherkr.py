import aiohttp
import asyncio
import json
import aiosqlite
import time

'''weather forecast script by parsing Naver weathers'''

class weatherf():
    def __init__(self):
        cwd = r'C:\EurikaMkIII' #fallback
        self.db = cwd + "\db\Jindo2.db"

    async def get_area_code(self, county, city = ""):
        '''Finds the given area code'''
        top_region_dict = {'광주': '05', '경남': '03', '세종': '17',
                        '충남': '15', '대전': '07', '인천': '11', '경기': '02',
                        '울산': '10', '경북': '04', '충북': '16', '전북': '13',
                        '대구': '06', '부산': '08', '서울': '09', '제주': '14', '전남': '12', '강원': '01'}

        async with aiosqlite.connect(self.db) as db:
            region_text = (county+city).replace(chr(32), "")
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

        return res
'''
if __name__ == "__main__":
    x = weatherf()
    a = asyncio.get_event_loop()
    print(a.run_until_complete(x.jindo2(a.run_until_complete(x.get_area_code("서울", "강남구")))))
    print(a.run_until_complete(x.jindo2(a.run_until_complete(x.get_area_code("대전")))))
'''
