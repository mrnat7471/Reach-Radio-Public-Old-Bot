import discord
from discord.ext import commands, tasks
import asyncio
import datetime
import json
import requests
import time
from itertools import cycle

class latestcog(commands.Cog):
    def get_prefix(client, message):
        with open('config.json', 'r') as f:
            prefixes = json.load(f)

        return prefixes['prefix']

    bot = commands.Bot(command_prefix = get_prefix)

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def latest(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.message.delete()
            message = await ctx.channel.send("I don't understand that command. Try: ``latest news``")
            with open('config.json', 'r') as f:
                logger = json.load(f)
                log = logger['logger']
                for user in log:
                    user = await self.bot.fetch_user(user)
                    user.send(f"[Latest Command] ran by {ctx.message.author.name} in {ctx.message.author.guild}({ctx.guild.id})")
            print(f"[Latest Command] ran by {ctx.message.author.name} in {ctx.message.author.guild}({ctx.guild.id})")
            await asyncio.sleep(5)
            await message.delete()

    @latest.command()
    async def news(self, ctx):
        r = requests.get("#")
        response = r.json()
        i = 0
        q = 1
        d = 2
        a = 3
        title0 = response['_embedded'][i]['title']
        slug0 = response['_embedded'][i]['slug']
        summary0 = response['_embedded'][i]['summary']

        title1 = response['_embedded'][q]['title']
        slug1 = response['_embedded'][q]['slug']
        summary1 = response['_embedded'][q]['summary']

        title2 = response['_embedded'][d]['title']
        slug2 = response['_embedded'][d]['slug']
        summary2 = response['_embedded'][d]['summary']

        title3 = response['_embedded'][a]['title']
        slug3 = response['_embedded'][a]['slug']
        summary3 = response['_embedded'][a]['summary']

        embed = discord.Embed(colour=discord.Colour.blue(), description="***" + title0 + "*** \n" + summary0 + " \n  [Read the Full Article](https://reachradio.co.uk/news/" + slug0 + ") \n \n" + "***" + title1 + "*** \n" + summary1 + " \n  [Read the Full Article](https://reachradio.co.uk/news/" + slug1 + ") \n \n" + "***" + title2 + "*** \n" + summary2 + "\n  [Read the Full Article](https://reachradio.co.uk/news/" + slug2 + ") \n \n" + "***" + title3 + "*** \n" + summary3 + " \n  [Read the Full Article](https://reachradio.co.uk/news/" + slug3 + ")")
        embed.set_author(name='Reach Radio News', icon_url=self.bot.user.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.channel.send(embed=embed)
        with open('config.json', 'r') as f:
            logger = json.load(f)
            log = logger['logger']
            for user in log:
                user = await self.bot.fetch_user(user)
                await user.send(f"[Latest News Comman]d ran by {ctx.message.author.name}({ctx.message.author.id}) ({ctx.guild.id})[{ctx.guild.name}]")
        print(f"[Latest News Command] ran by {ctx.message.author.name}({ctx.message.author.id}) ({ctx.guild.id})[{ctx.guild.name}]")
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(latestcog(bot))
