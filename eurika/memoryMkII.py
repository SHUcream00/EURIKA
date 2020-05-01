import asyncio
import time
import aiosqlite
import datetime

'''
Async SQLite memoization management snippet for EURIKA
Author: 2020 SHUcream
'''

cwd = r'C:\EurikaMkIII'

class memento():
    async def recall(self, key):
        async with aiosqlite.connect(cwd + "\db\EurDB.db") as db:
            async with db.execute("SELECT * FROM Memory WHERE Name='"+key+"' COLLATE NOCASE") as cursor:
                res = await cursor.fetchone()
                text_color = 0x07ECBA

                if res == None:
                    async with db.execute("SELECT * FROM Memory WHERE Name Like'%"+key+"%' COLLATE NOCASE") as cursor:
                        res = list(map(lambda x: x[1], await cursor.fetchall()))
                        text_color = 0xB5002B

                return res, text_color

    async def memorize(key, value, **kwargs):
        async with aiosqlite.connect(cwd + "\db\EurDB.db") as db:
            async with db.execute("SELECT * FROM Memory WHERE Name='"+key+"' COLLATE NOCASE") as cursor:
                res = await cursor.fetchone()
                if res == None:
                    return False, 0xB5002B
                else:
                    await db.execute("INSERT INTO Memory (Name, Value, User, Date) VALUES ('" + key + "', '" + value + "', '"+ kwargs['author'] +"', '"+ time.strftime('%Y-%m-%d %H:%M:%S') +"')")
                    await db.commit()
                    await db.close()
                    return True, 0x07ECBA

    async def find(self, key):
        async with aiosqlite.connect(cwd + "\db\EurDB.db") as db:
            async with db.execute("SELECT * FROM Memory WHERE Name Like'%"+key+"%' COLLATE NOCASE") as cursor:
                res = list(map(lambda x: x[1], await cursor.fetchall()))
                return res, 0xB5002B

    async def append(self, key, value, **kwargs):
        async with aiosqlite.connect(cwd + "\db\EurDB.db") as db:
            async with db.execute("SELECT * FROM Memory WHERE Name='"+key+"' COLLATE NOCASE") as cursor:
                res = await cursor.fetchone()
                if res == None:
                    return False, 0xB5002B
                else:
                    tgt = (res[2]+" - "+value, kwargs['author'], time.strftime('%Y-%m-%d %H:%M:%S'), key)
                    await cursor.execute("UPDATE Memory SET value=?, User=?, Date=? Where Name=? COLLATE NOCASE", tgt)
                    await db.execute("UPDATE Memory SET value=?, User=?, Date=? Where Name=? COLLATE NOCASE", tgt)
                    await db.commit()
                    await db.close()
                    return True, 0x07ECBA

    async def own(self, **kwargs):
        async with aiosqlite.connect(cwd + "\db\EurDB.db") as db:
            async with db.execute("SELECT * FROM Memory WHERE User='"+str(kwargs['author'])+"'") as cursor:
                res = list(map(lambda x: x[1], await cursor.fetchall()))
                if res != []:
                    return res, 0x07ECBA
                else:
                    return False, 0xB5002B

    async def rand(self):
        async with aiosqlite.connect(cwd + "\db\EurDB.db") as db:
            async with db.execute("SELECT * FROM Memory ORDER BY RANDOM() LIMIT 1") as cursor:
                res = await cursor.fetchone()
                return res, 0x07ECBA
