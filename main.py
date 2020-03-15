'''
Requirement:
Python 3.7 or up, discord-py, BeautifulSoup4, pil

'''

@client.event
async def on_ready():
    client.loop.create_task(bluebird())
    client.loop.create_task(saryunan())
    client.loop.create_task(mandubird())
    print('Eurika NEXT Main activated')
    print(client.user.name)
    print('------')

client.run(id)
