from __future__ import absolute_import, print_function

import json
import tweepy
import discord
import sqlite3

cwd = r'C:\EurikaMkIII' #Do I really need this? can't i use cwd()?

description = '''Python Twitter wrapper for EURIKA'''

#fgo = 2968069742
class hototogisu():

    def __init__(self):
        consumer_key="KEY"
        consumer_secret="SECRET"
        access_token="TOKEN"
        access_token_secret="TOKEN_SECRET"

        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)

    async def cry(self, **kwargs):
        api = tweepy.API(self.auth)
        twtid = kwargs['ID']
        twtdet = api.user_timeline(id = twtid, count=10, tweet_mode='extended')
        twtres = []
        twtprv = ''
        db = sqlite3.connect(cwd + '\db\EurDB.db')
        cursor = db.cursor()
        for i, j in enumerate(twtdet):
            twtcache = cursor.execute("SELECT * FROM TwitterCache WHERE ID='"+str(twtid)+"' COLLATE NOCASE").fetchone()
            twttemp = []
            j = j._json

            twttemp.append(j['id'])
            twttemp.append(j['full_text'])
            twttemp.append(j['user']['name'])
            twttemp.append(j['user']['profile_image_url'])
            twttemp.append(j['user']['profile_sidebar_border_color'])
            if 'profile_banner_url' in j['user']:
                twttemp.append(j['user']['profile_banner_url'])
            else:
                twttemp.append(None)
            twttemp.append(j['created_at'])

            twtprv += ' | ' + str(twttemp[0])


            if 'media' in j['entities']:
                twttemp.append(j['entities']['media'][0]['media_url'])
            else:
                twttemp.append(None)
            twttemp.append(twtcache[4])

            if str(twttemp[0]) not in twtcache[2] and len(twtcache[2].split('|')) == 11:
                #print('<<Anomalyfound>>\n' + str(kwargs['ID']) + '\n', 'previous:\n' + str(twtcache[2]) + '\n', 'new:\n' + str(twttemp[0]))
                #print('length:' + str(len(twtcache[2].split('|'))))
                twtres.append(twttemp)

            if i == 0:
                if twtcache[5].strip() != j['user']['profile_image_url'].strip():
                    twtpfupdate = [j['id'], j['user']['name'] + '의 프사가 변경되었습니다.', j['user']['name'], twtcache[5], j['user']['profile_sidebar_border_color'], None, j['created_at'], j['user']['profile_image_url'].replace('_normal', ''), twtcache[4]]
                    twtres.append(twtpfupdate)
                cursor.execute("UPDATE TwitterCache SET Last=? Where ID=?", (j['full_text'], twtid))

        cursor.execute("UPDATE TwitterCache SET Previous=?, Profile=? Where ID=?", (twtprv, j['user']['profile_image_url'], twtid))
        db.commit()
        db.close()
        return twtres
