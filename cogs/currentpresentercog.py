import discord
from discord.ext import commands, tasks
import asyncio
import datetime
import ffmpeg
import json
import requests
import time
from itertools import cycle

class currentpresenterCog(commands.Cog):
    def get_prefix(client, message):
        with open('config.json', 'r') as f:
            prefixes = json.load(f)

        return prefixes['prefix']

    bot = commands.Bot(command_prefix = get_prefix)

    def __init__(self, bot):
        self.bot = bot

    @bot.command(name='live')
    async def say_embed(self, ctx):
        try:
            r = requests.get("#")
            response = r.json()
            name = response['user']['firstName']
            avatar = response['user']['avatar']
            title = response['title']
            showtype = response['slotType']['name']
            start_json = response['start']
            end_json = response['end']

            start = time.strftime("%H:%M", time.localtime(int(start_json)))
            end = time.strftime("%H:%M", time.localtime(int(end_json)))

            if 'No Presenter' == str(showtype):
                embed = discord.Embed(colour=discord.Colour.blue(), description=f"**Show Title:** {title} \n {start} to {end} BST")
                embed.set_author(name='Reach Radio Currently Live')
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_footer(text=f'Reach Radio Bot', icon_url=self.bot.user.avatar_url)
                embed.set_thumbnail(url="https://reachradio.co.uk/_nuxt/img/r-small.3cf5e4e.png")
            else:
                embed = discord.Embed(colour=discord.Colour.blue(), description=f"**Presenter:** {name} \n **Show Title:** {title} \n {start} to {end} BST")
                embed.set_author(name='Reach Radio Currently Live')
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_footer(text=f'Reach Radio Bot', icon_url=self.bot.user.avatar_url)
                embed.set_thumbnail(url=avatar)

            embed.set_author(name='Reach Radio Currently Live')
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text=f'Reach Radio Bot', icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url=avatar)

            message = await ctx.channel.send(embed=embed)
            with open('config.json', 'r') as f:
                logger = json.load(f)
                log = logger['logger']
                for user in log:
                    user = await self.bot.fetch_user(user)
                    await user.send(f"[Live Command] ran by {ctx.message.author.name} in {ctx.message.author.guild}({ctx.guild.id})")
            print(f"[Live Command] ran by {ctx.message.author.name} in {ctx.message.author.guild}({ctx.guild.id})")
            await ctx.message.delete()
            await asyncio.sleep(120)
            await message.delete()
        except ValueError:
            embed = discord.Embed(colour=discord.Colour.blue(), description=f"Non Stop")
            embed.set_author(name='Reach Radio Currently Live')
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text=f'Reach Radio Bot', icon_url=self.bot.user.avatar_url)
            message = await ctx.channel.send(embed=embed)
            await ctx.message.delete()
            await asyncio.sleep(120)
            await message.delete()

def setup(bot):
    bot.add_cog(currentpresenterCog(bot))
