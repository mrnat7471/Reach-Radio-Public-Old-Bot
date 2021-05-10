import discord
from discord.ext import commands, tasks
import datetime
import ffmpeg
import json
import requests
import time
from itertools import cycle
import os
from os import listdir
from os.path import isfile, join
import logging
import asyncio
from discord.ext.commands import AutoShardedBot, CommandNotFound

logger = logging.getLogger('discord')
logger.setLevel(logging.ERROR)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

def get_prefix(client, message):
        with open('config.json', 'r') as f:
            prefixes = json.load(f)

        return prefixes['prefix']

bot = AutoShardedBot(command_prefix=get_prefix, pm_help=True, fetch_offline_members=False)
bot.remove_command('help')

@bot.event
async def on_ready():
    print("Bot has been started")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="rr!help | Reach Radio"))
    with open('config.json', 'r') as f:
        logger = json.load(f)
        log = logger['logger']
        for user in log:
            user = await bot.fetch_user(user)
            await user.send("Reach Radio Public Bot is now ready!")
    change_status.start()

@bot.event
async def on_shard_ready(shard_id):
    print(f"Shard: {shard_id} is ready")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

@tasks.loop(seconds=15)
async def change_status():
    i = 0
    for vc in bot.voice_clients:
            members = len(vc.channel.members)

            i = i + members
    jsonFile = open("listeners.json", encoding='utf-8')
    data = json.load(jsonFile)
    data["icestats"]["source"]["listeners"] = i
    with open('listeners.json','w+') as newJSON:
        json.dump(data, newJSON)

    r = requests.get("#")
    response = r.json()
    currentsong = response["_embedded"][0]["song"]
    title = currentsong["title"]
    artist = currentsong["artist"]
    print(f"{artist} - {title}")
    game = discord.Game(f"{artist} - {title}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="rr!help | Reach Radio"))
    await asyncio.sleep(15)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{artist} - {title}"))
    await asyncio.sleep(15)

    #for vc in bot.voice_clients:
        #if vc.is_playing():
            #members = len(vc.channel.members) - 1
            #if members == 0:
                #await vc.disconnect()
            #else:
                #pass
        #elif not vc.is_playing():
            #await vc.disconnect()
        #else:
            #pass 

cogs_dir = "cogs"

if __name__ == '__main__':
    for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
        try:
            bot.load_extension(cogs_dir + "." + extension)
        except (discord.ClientException, ModuleNotFoundError):
            print(f'Failed to load extension {extension}.')

while True:
    try:
        with open('config.json', 'r') as f:
            timez = json.load(f)
            tokentxt = timez['token']
        bot.loop.run_until_complete(bot.run(tokentxt))
    except BaseException:
        pass
