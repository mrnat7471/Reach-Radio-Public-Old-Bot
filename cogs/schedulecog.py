import discord
from discord.ext import commands
import asyncio
import datetime
import requests
import time
import json


class schedulecog(commands.Cog):
    def get_prefix(client, message):
        with open('config.json', 'r') as f:
            prefixes = json.load(f)

        return prefixes['prefix']

    bot = commands.Bot(command_prefix = get_prefix)
    bot.remove_command('schedule')

    def __init__(self, bot):
        self.bot = bot

    @bot.command(name='schedule')
    async def schedule(self, ctx):
        r = requests.get(f"#")
        i = 0
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name='Reach Radio Schedule')
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'Reach Radio Public', icon_url=self.bot.user.avatar_url)
        for item in range(3):
            if i < 3:
                if i == 0:
                    fieldName = "Now"
                    r = requests.get(f"#")
                elif i == 1:
                    fieldName = "Next"
                    r = requests.get(f"#")
                else:
                    fieldName = "Later"
                    r = requests.get(f"#")
                response = r.json()
                title = response['title']
                name = response['user']['firstName']
                avatar = response['user']['avatar']
                showtype = response['slotType']['name']
                start_json = response['start']
                end_json = response['end']
                start = time.strftime("%H:%M", time.localtime(int(start_json)))
                end = time.strftime("%H:%M", time.localtime(int(end_json)))
                with open('config.json', 'r') as f:
                    timez = json.load(f)
                    timezone = timez['timezone']
                if str(name) == "Non Stop":
                    embed.add_field(name=fieldName, value=f"**Show Title:** {title} \n {start} to {end} {timezone} \n\uFEFF", inline=False)
                else:
                    embed.add_field(name=fieldName, value=f"**Presenter:** {name} \n **Show Title:** {title} \n {start} to {end} {timezone} \n\uFEFF", inline=False)
                i = i+1
            else:
                pass

        with open('config.json', 'r') as f:
            logger = json.load(f)
            log = logger['logger']
            for user in log:
                user = await self.bot.fetch_user(user)
                await user.send(f"[Schedule Command] ran by {ctx.message.author.name}({ctx.message.author.id}) in {ctx.message.author.guild}({ctx.guild.id})")
        await ctx.channel.send(embed=embed)
        await ctx.message.delete()

    @schedule.error
    async def schedule_error(self, ctx, error):
        await ctx.message.delete()
        embed = discord.Embed(colour=discord.Colour.red(), title="Error", description="Bot has encountered the following error:\n" + error)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text=f'Reach Radio Bot', icon_url=self.bot.user.avatar_url)
        with open('config.json', 'r') as f:
            logger = json.load(f)
            log = logger['logger']
            for user in log:
                user = await self.bot.fetch_user(user)
                await user.send(embed=embed)
        return
        print("\n\n" + str(error) + "\n\n")

def setup(bot):
    bot.add_cog(schedulecog(bot))
