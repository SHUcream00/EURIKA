from __future__ import absolute_import, print_function

import json
import tweepy
import ast
import sqlite3

cwd = r'C:\EurikaMkIII' #Do I really need this? can't i use cwd()?

description = '''Python Twitter wrapper for EURIKA'''

#fgo = 2968069742
class hototogisu():

    def __init__(self):
        self.consumer_key="KEY"
        self.consumer_secret="SECRET"
        self.access_token="TOKEN"
        self.access_token_secret="TOKEN_SECRET"

        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)

    def cry(self, **kwargs):
        api = tweepy.API(self.auth)
        twtid = kwargs['ID']
        twtdet = api.user_timeline(id = twtid, count=10, tweet_mode='extended')
        twtres = []
        db = sqlite3.connect(cwd + '\db\EurDB.db')
        cursor = db.cursor()
        twtcur = set()

        for i, j in enumerate(twtdet):
            twtcache = cursor.execute("SELECT * FROM TwitterCache WHERE ID='"+str(twtid)+"' COLLATE NOCASE").fetchone()
            twttemp = []
            j = j._json

            twttemp.extend([j['id'], j['full_text'], j['user']['name'], j['user']['profile_image_url'],\
                            j['user']['profile_sidebar_border_color']])

            if 'profile_banner_url' in j['user']:
                twttemp.append(j['user']['profile_banner_url'])
            else:
                twttemp.append(None)
            twttemp.append(j['created_at'])

            twtcur.add(twttemp[0])

            if 'media' in j['entities']:
                twttemp.append(j['entities']['media'][0]['media_url'])
            else:
                twttemp.append(None)
            twttemp.append(twtcache[4])

            if twttemp[0] not in ast.literal_eval(twtcache[2]):
                twtres.append(twttemp)

            if i == 0:
                if twtcache[5].strip() != j['user']['profile_image_url'].strip():
                    twtpfupdate = [j['id'], j['user']['name'] + '의 프사가 변경되었습니다.', j['user']['name'], twtcache[5], j['user']['profile_sidebar_border_color'], None, j['created_at'], j['user']['profile_image_url'].replace('_normal', ''), twtcache[4]]
                    twtres.append(twtpfupdate)
                cursor.execute("UPDATE TwitterCache SET Last=? Where ID=?", (j['full_text'], twtid))

        twtprv = ast.literal_eval(cursor.execute("SELECT * FROM TwitterCache WHERE ID='"+str(twtid)+"' COLLATE NOCASE").fetchone()[2])
        cursor.execute("UPDATE TwitterCache SET Previous=?, Profile=? Where ID=?", (str(twtprv.union(twtcur)), j['user']['profile_image_url'], twtid))
        db.commit()
        db.close()
        return twtres

'''
if __name__ == "__main__":
    db = sqlite3.connect(cwd + '\db\EurDB.db')
    a = hototogisu()
    #a.cry()
    for j in db.cursor().execute("SELECT ID FROM TwitterCache").fetchall():
        print(j)
        a.cry(ID=j[0])
'''
