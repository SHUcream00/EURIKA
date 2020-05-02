import aiohttp
import asyncio
import json
import aiosqlite

'''weather forecast script by parsing Naver weathers'''



async def get_area_code(county, city = ""):
    '''Finds the given area code'''
    top_region_dict = {'광주': '05', '경남': '03', '세종': '17',
                    '충남': '15', '대전': '07', '인천': '11', '경기': '02',
                    '울산': '10', '경북': '04', '충북': '16', '전북': '13',
                    '대구': '06', '부산': '08', '서울': '09', '제주': '14', '전남': '12', '강원': '01'}
    if county in top_region_dict.keys():
        temp = "https://weather.naver.com/json/rgnCat.nhn?_callback=window.__jindo2_callback._6128&m=naverRgnCat&upperRgnCd={}"
        async with aiohttp.ClientSession() as session:
            async with session.get(temp.format(top_region_dict[county])) as resp:
                raw = await resp.text()
                city_data = json.loads(raw[raw.index(chr(40))+1:raw.index(chr(41))])
                city_dict = {i['rgnNm']: i['rgnCd'] for i in city_data['rgnList']}

        if city in city_dict.keys():
            async with aiohttp.ClientSession() as session:
                async with session.get(temp.format(city_dict[city])) as resp:
                    raw = await resp.text()
                    city_data = json.loads(raw[raw.index(chr(40))+1:raw.index(chr(41))])
                    return city_data['rgnList'][0]['rgnCd']

async def jindo2(loc = "09710566"):
    '''Get the actual forecast data'''
    #alt = https://weather.naver.com/flash/naverRgnTownFcast.nhn?m=jsonResult&naverRgnCd=12910350 # 3 hours
    temp = "https://weather.naver.com/json/crntWetrDetail.nhn?_callback=window.__jindo2_callback._902&naverRgnCd={}"
    async with aiohttp.ClientSession() as session:
        async with session.get(temp.format(loc)) as resp:
            raw = await resp.text()
            w_data = json.loads(raw[raw.index(chr(40))+1:raw.index(chr(41))])

    res = {}
    res['region_str'] = "{} {}".format(w_data['wetrMap'][1][1]['lareaNm'], w_data['wetrMap'][1][1]['mareaNm'])
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
    w_2days = list(map(lambda x: ((x['applyYmd'], x['amWeatherText'], x['amTemperature'], x['amRainProbability']),
                            (x['applyYmd'], x['pmWeatherText'], x['pmTemperature'], x['pmRainProbability'])), w_data['wetrMap'][2][1]))
    #return w_rgnname, w_now, w_2days
    return res

if __name__ == "__main__":
    a = asyncio.get_event_loop()
    print(a.run_until_complete(jindo2(a.run_until_complete(get_area_code("서울", "강남구")))))
