import discord
from discord.ext import commands, tasks
import asyncio
import datetime
import json
import requests
import time
from itertools import cycle
import os
import sys

class devCog(commands.Cog):
    def get_prefix(client, message):
        with open('config.json', 'r') as f:
            prefixes = json.load(f)

        return prefixes['prefix']

    bot = commands.Bot(command_prefix = get_prefix)

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def dev(self, ctx):
        with open('config.json', 'r') as f:
            logger = json.load(f)
            users = logger['admin']
            for user in users:
                if ctx.message.author.id == user:
                    if ctx.invoked_subcommand is None:
                        embed = discord.Embed(colour=discord.Colour.blue(),
                        description=f"""
                        **Development Team + Admins Help Command**
                        
                        ◉ rr!dev reload <cog>
                        ◉ rr!dev tag <tag>
                        ◉ rr!dev restart
                        ◉ rr!dev guildlist""")
                        embed.timestamp = datetime.datetime.utcnow()
                        embed.set_footer(text=f'Posted by {ctx.message.author.name}', icon_url=ctx.message.author.avatar_url)
                        await ctx.channel.send(embed=embed)

    @dev.command()
    async def guildlist(self, ctx):
        with open("guildlist.txt", "w", encoding="utf-8") as text_file:
            for guild in self.bot.guilds:
                print(f"Guild Name: {guild.name} [ID: {guild.id}] - (Shard ID: {guild.shard_id}) - Member Count: {guild.member_count}", file=text_file)
        with open("guildlist.txt", "rb") as file:
                await ctx.send("As Requested, here is all the guilds the bot is in:", file=discord.File(file, "guildlist.txt"))

        with open('config.json', 'r') as f:
            logger = json.load(f)
            log = logger['logger']
            for user in log:
                user = await bot.fetch_user(user)
                await user.send(f"[Guildlist Command] ran by {ctx.message.author.name} in {ctx.message.author.guild}({ctx.guild.id})")

    @dev.command()
    async def reload(self, ctx, cog=None):
        with open('config.json', 'r') as f:
            logger = json.load(f)
            users = logger['admin']
        for user in users:
            if ctx.message.author.id == user:
                if not cog:
                    async with ctx.typing():
                        embed = discord.Embed(
                            title="Reloaded All Cogs!")
                        for ext in os.listdir("./cogs/"):
                            if ext.endswith(".py") and not ext.startswith("_"):
                                try:
                                    self.bot.unload_extension(f"cogs.{ext[:-3]}")
                                    self.bot.load_extension(f"cogs.{ext[:-3]}")
                                    embed.add_field(name=f"Reloaded {ext}", value='\uFEFF')
                                except Exception as e:
                                    embed.add_field(name=f"Failed to reload `{ext}``",value=e)
                                await asyncio.sleep(0.5)
                        await ctx.channel.send(embed=embed)
                        with open('config.json', 'r') as f:
                            logger = json.load(f)
                            log = logger['logger']
                            for user in log:
                                user = await self.bot.fetch_user(user)
                                await user.send(f"[Reload Command] ran by {ctx.message.author.name}({ctx.message.author.id}) in {ctx.message.author.guild}({ctx.guild.id})")
                else:
                    async with ctx.typing():
                        embed = discord.Embed(
                            title="Reloaded A Cogs!")
                        ext = f"{cog.lower()}.py"
                        if not os.path.exists(f"./cogs/{ext}"):
                            embed.add_field(name=f"failed to reload `{ext}`", value="this cog doesn't exist.")

                        elif ext.endswith(".py") and not ext.startswith("_"):
                                try:
                                    self.bot.unload_extension(f"cogs.{ext[:-3]}")
                                    self.bot.load_extension(f"cogs.{ext[:-3]}")
                                    embed.add_field(name=f"Reloaded {ext}", value='\uFEFF')
                                except Exception as e:
                                    embed.add_field(name=f"Failed to reload ``{ext}``",value=e)
                                await asyncio.sleep(0.5)
                    await ctx.channel.send(embed=embed)
                    with open('config.json', 'r') as f:
                        logger = json.load(f)
                        log = logger['logger']
                        for user in log:
                            user = await self.bot.fetch_user(user)
                            await user.send(f"[Reload Command] ran by {ctx.message.author.name}({ctx.message.author.id}) in {ctx.message.author.guild}({ctx.guild.id})")


    @dev.command()
    async def restart(self, ctx):
        with open('config.json', 'r') as f:
            logger = json.load(f)
            users = logger['admin']
            for user in users:
                if ctx.message.author.id == user:
                    embed = discord.Embed(colour=discord.Colour.blue(), description="Restarting bot...")
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_footer(text='Reach Radio Bot', icon_url=self.bot.user.avatar_url)
                    await ctx.channel.send(embed=embed)
                    await ctx.message.delete()
                    with open('config.json', 'r') as f:
                        logger = json.load(f)
                        log = logger['logger']
                        for user in log:
                            user = await self.bot.fetch_user(user)
                            await user.send("``` ```")
                            await user.send(f"Bot Connection Terminated by {ctx.message.author.name}")
                    print("Bot Connection Terminated")
                    path = sys.argv
                    path = path[0]
                    print(path)
                    os.execl(sys.executable, sys.executable, '"' + path + '"')
                        
    @dev.command()
    async def tag(self, ctx, message=None):
        with open('config.json', 'r') as f:
            logger = json.load(f)
            users = logger['admin']
            for user in users:
                if ctx.message.author.id == user:
                    embed = discord.Embed(colour=discord.Colour.blue())
                    embed.set_author(name='Reach Radio Tag Command', icon_url=self.bot.user.avatar_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_footer(text='Reach Radio Bot', icon_url=self.bot.user.avatar_url)
                    if message == "trumpdance":
                        embed.set_image(url=f"https://media.discordapp.net/attachments/615241939779846164/768587638428270652/1qXG8UkiGP.gif")
                        await ctx.channel.send(embed=embed)
                    elif message == "nathandance":
                        embed.set_image(url=f"https://media.discordapp.net/attachments/698172970237165588/768586240101580850/mVISTcsM7T.gif")
                        await ctx.channel.send(embed=embed)
                    elif message == "josephdance":
                        embed.set_image(url=f"https://i.gyazo.com/98ce0c8f8cb5a9ef1b00cca771b5cae8.gif")
                        await ctx.channel.send(embed=embed)
                    elif message == "shaydance":
                        embed.set_image(url=f"https://i.imgur.com/wKWscNp.gif")
                        await ctx.channel.send(embed=embed)
                    else:
                        await ctx.channel.send("**Tags:** \n ``rr!tag`` \n \n trumpdance \n nathandance \n josephdance \n crazyfrog \n shaydance")     

                    await ctx.message.delete()
                    
    @dev.command(name='play')
    async def play(self, ctx, message):
        with open('config.json', 'r') as f:
            logger = json.load(f)
            users = logger['admin']
            for user in users:
                if ctx.message.author.id == user:
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
                    VoiceClient.play(discord.FFmpegPCMAudio(message))

                    embed = discord.Embed(colour=discord.Colour.blue(), description=f"Now playing: {message}")
                    embed.set_author(name='Reach Radio Dev', icon_url=self.bot.user.avatar_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_footer(text=f'Reach Radio Bot', icon_url=self.bot.user.avatar_url)
                    message = await ctx.channel.send(embed=embed)

                    await ctx.message.delete()
                    await asyncio.sleep(30)
                    await message.delete()

   

def setup(bot):
    bot.add_cog(devCog(bot)) 