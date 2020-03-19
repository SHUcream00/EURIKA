'''
Requirement:
Python 3.7 or up, discord-py, BeautifulSoup4, pil

'''
client = discord.Client()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await channel.send('Hello!')

@client.event
async def on_ready():
    #test2
    #client.loop.create_task(bluebird())
    #client.loop.create_task(saryunan())
    #client.loop.create_task(mandubird())
    print('Eurika NEXT Main activated')
    print(client.user.name)
    print('------')

client.run(id)
