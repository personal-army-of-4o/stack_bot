# bot.py
import os
import discord
from Bot import Bot

with open('token','r') as file:
    TOKEN = file.read()

client = discord.Client()

cfg={}
cfg["state_file_name"]="state.json"
cfg["channel"]=789206550015246357

bot=Bot(cfg)

@client.event
async def clear(channel):
    messages = channel.history(limit=200)
    async for x in messages: # , limit = number
        await x.delete()
#    await client.delete_messages(mgs)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    channel = client.get_channel(cfg["channel"])
    print(channel)
    await clear(channel)
    await channel.send(bot.Dump())

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    (reply, report) = bot.Handle(message)
    if reply:
        await message.channel.send(reply)

    if report:
        channel = client.get_channel(cfg["channel"])
        await clear(channel)
        await channel.send(bot.Dump())
    return

#@client.event
#async def on_error(event, *args, **kwargs):
#    print(f'Unhandled message: {args[0]}\n')

client.run(TOKEN)