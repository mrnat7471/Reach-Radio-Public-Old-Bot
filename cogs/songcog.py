import discord
from discord.ext import commands, tasks
import asyncio
import datetime
import ffmpeg
import json
import requests
import time
from itertools import cycle

class songCog(commands.Cog):
    def get_prefix(client, message):
        with open('config.json', 'r') as f:
            prefixes = json.load(f)

        return prefixes['prefix']

    bot = commands.Bot(command_prefix = get_prefix)

    def __init__(self, bot):
        self.bot = bot

    @bot.command(name='song')
    async def say_embed(self, ctx):
        r = requests.get("#")
        response = r.json()
        title = response['song']['artist']
        artist = response['song']['title']
        songthumb = response['song']['graphic']['medium']

        embed = discord.Embed(colour=discord.Colour.blue(), message="Reach Radio is currently Playing")
        embed.add_field(name=title, value=artist, inline=True)
        embed.set_author(name='Reach Radio Song Information')
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'Reach Radio Bot', icon_url=self.bot.user.avatar_url)
        if songthumb == "CUSTOMSTUFFHERE":
            pass
        else:
            embed.set_thumbnail(url=songthumb)

        message = await ctx.channel.send(embed=embed)
        with open('config.json', 'r') as f:
            logger = json.load(f)
            log = logger['logger']
            for user in log:
                user = await self.bot.fetch_user(user)
                await user.send(f"[Song Command] (Common) ran by {ctx.message.author.name}({ctx.message.author.id}) in {ctx.message.author.guild}({ctx.guild.id})")
        print(f"[Song Command] (Common) ran by {ctx.message.author.name}({ctx.message.author.id}) in {ctx.message.author.guild}({ctx.guild.id})")
        await ctx.message.delete()
        await asyncio.sleep(30)
        await message.delete()
def setup(bot):
    bot.add_cog(songCog(bot))
