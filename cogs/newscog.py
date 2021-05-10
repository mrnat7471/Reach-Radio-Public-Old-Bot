import discord
from discord.ext import commands
import asyncio
import datetime
import json
import requests
import time
import os

class newsCog(commands.Cog):
    def get_prefix(client, message):
        with open('config.json', 'r') as f:
            prefixes = json.load(f)

        return prefixes['prefix']

    bot = commands.Bot(command_prefix = get_prefix)

    def __init__(self, bot):
        self.bot = bot

    @bot.command(name='news')
    async def say_embed(self, ctx):
        r = requests.get("#")
        response = r.json()
        i = 0
        title = response['_embedded'][i]['title']
        image = response['_embedded'][i]['featuredImage']
        slug = response['_embedded'][i]['slug']
        first_name = response['_embedded'][i]['user']['firstName']
        last_name = response['_embedded'][i]['user']['lastName']
        summary = response['_embedded'][i]['summary']
        embed = discord.Embed(colour=discord.Colour.blue(), description="***" + title + "*** \n \n" + summary + "\n \n Read the Full Article: https://reachradio.co.uk/news/" + slug)
        embed.set_image(url=image)
        embed.set_author(name='Reach Radio News', icon_url=self.bot.user.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text='Posted by ' + first_name + " " + last_name)
        await ctx.channel.send(embed=embed)
        with open('config.json', 'r') as f:
            logger = json.load(f)
            log = logger['logger']
            for user in log:
                user = await self.bot.fetch_user(user)
                await user.send(f"[Last News Command] ran by {ctx.message.author.name}({ctx.message.author.id}) in {ctx.message.author.guild}({ctx.guild.id})")
        print(f"[Last News Command] ran by {ctx.message.author.name}({ctx.message.author.id}) in {ctx.message.author.guild}({ctx.guild.id})")
        await ctx.message.delete()


def setup(bot):
    bot.add_cog(newsCog(bot))
