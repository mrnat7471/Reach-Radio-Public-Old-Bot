import discord
from discord.ext import commands, tasks
import asyncio
import datetime
import ffmpeg
import json
import requests
import time
from itertools import cycle

class reachCog(commands.Cog):
    def get_prefix(client, message):
        with open('config.json', 'r') as f:
            prefixes = json.load(f)

        return prefixes['prefix']

    bot = commands.Bot(command_prefix = get_prefix)

    def __init__(self, bot):
        self.bot = bot

    @bot.command(name='recentlyplayed')
    async def say_embed(self, ctx):
        r = requests.get("#")
        response = r.json()
        a = 0
        b = 1
        c = 2
        d = 3
        e = 4

        title0 = response['_embedded'][a]['song']['artist']
        artist0 = response['_embedded'][a]['song']['title']

        title1 = response['_embedded'][b]['song']['artist']
        artist1 = response['_embedded'][b]['song']['title']

        title2 = response['_embedded'][c]['song']['artist']
        artist2 = response['_embedded'][c]['song']['title']

        title3 = response['_embedded'][d]['song']['artist']
        artist3 = response['_embedded'][d]['song']['title']

        title4 = response['_embedded'][e]['song']['artist']
        artist4 = response['_embedded'][e]['song']['title']

        embed = discord.Embed(colour=discord.Colour.blue())
        embed.add_field(name=title0, value=artist0, inline=False)
        embed.add_field(name=title1, value=artist1, inline=False)
        embed.add_field(name=title2, value=artist2, inline=False)
        embed.add_field(name=title3, value=artist3, inline=False)
        embed.add_field(name=title4, value=artist4, inline=False)
        embed.set_author(name='Reach Radio Latest Songs', icon_url=self.bot.user.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'Reach Radio Bot', icon_url=self.bot.user.avatar_url)

        message = await ctx.channel.send(embed=embed)
        with open('config.json', 'r') as f:
            logger = json.load(f)
            log = logger['logger']
            for user in log:
                user = await self.bot.fetch_user(user)
                await user.send(f"[Played Command] ran by {ctx.message.author.name}({ctx.message.author.id}) in {ctx.message.author.guild}({ctx.guild.id})")
        print(f"[Played Command] ran by {ctx.message.author.name}({ctx.message.author.id}) in {ctx.message.author.guild}({ctx.guild.id})")
        await ctx.message.delete()
        await asyncio.sleep(30)
        await message.delete()
def setup(bot):
    bot.add_cog(reachCog(bot))
