import discord
from discord.ext import commands, tasks
from discord.ext.commands import AutoShardedBot
import asyncio
import datetime
import ffmpeg
import json
import requests
import time
from itertools import cycle
import os
from os import listdir
from os.path import isfile, join
import sys, traceback
import logging

class reachCog(commands.Cog):
    def get_prefix(client, message):
        with open('config.json', 'r') as f:
            prefixes = json.load(f)

        return prefixes['prefix']

    bot = commands.Bot(command_prefix = get_prefix)


    def __init__(self, bot):
        self.bot = bot

    @bot.command(name='play', aliases=['join', 'start'])
    async def play(self, ctx):
            try:
                try:
                    channel = ctx.author.voice.channel
                except:
                    channel = None

                voice = None
                for vc in self.bot.voice_clients:
                    if vc.guild == ctx.guild:
                        voice = vc

                if channel == None:
                    embed = discord.Embed(colour=discord.Colour.blue(), description="You're not in a voice channel")
                    embed.set_author(name='Reach Radio', icon_url=self.bot.user.avatar_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_footer(text=f'Reach Radio Bot', icon_url=self.bot.user.avatar_url)
                    await ctx.channel.send(embed=embed)
                    return
                if voice and voice.is_connected():
                    await voice.disconnect()
                    VoiceClient = await channel.connect()
                elif voice == channel:
                    pass
                else:
                    VoiceClient = await channel.connect()
                
                bot_channel =  ctx.guild.voice_client
                VoiceClient.play(discord.FFmpegPCMAudio('#'))

                r = requests.get("#")
                response = r.json()
                songs = response['song']['artist'] + " - " + response['song']['title']


                embed = discord.Embed(colour=discord.Colour.blue(), description="This bot is getting to it's retirement age! Want to stay up to date with all the latest bot features. Please invite our brand new bot [here](https://discord.com/oauth2/authorize?client_id=824979067656863766&permissions=37578816&scope=bot%20applications.commands) and kick our old one. \n \n Now playing Reach Radio \n **Current Song:** " + songs)
                embed.set_author(name='Reach Radio', icon_url=self.bot.user.avatar_url)
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_footer(text=f'Reach Radio Bot', icon_url=self.bot.user.avatar_url)
                message = await ctx.channel.send(embed=embed)


                with open('config.json', 'r') as f:
                    logger = json.load(f)
                    log = logger['logger']
                    for user in log:
                        user = await self.bot.fetch_user(user)
                        await user.send(f"[Play Command] Connected to Voice Channel ({ctx.author.voice.channel}) in guild: ({str(ctx.message.author.guild)}) ran by {ctx.message.author.name}({ctx.message.author.id})")
                print(f"[Play Command] Connected to Voice Channel ({ctx.author.voice.channel}) in guild: ({str(ctx.message.author.guild)}) ran by {ctx.message.author.name}({ctx.message.author.id})")

                await ctx.message.delete()
                await asyncio.sleep(30)
                await message.delete()
            
            except Exception as error:
                print(error)
                with open('config.json', 'r') as f:
                    logger = json.load(f)
                    log = logger['logger']
                if(error == "Already connected to a voice channel."):
                    pass
                else:
                    for user in log:
                        user = await self.bot.fetch_user(user)
                        await user.send(f"[Play Command] ERROR in guild: {ctx.message.author.guild} ran by {ctx.message.author.name}({str(ctx.message.author.id)}) \n" + "```diff\n- ERROR | command: Leave [FILE](playcog.py)```" + "```" + str(error) + "```")


def setup(bot):
    bot.add_cog(reachCog(bot))
