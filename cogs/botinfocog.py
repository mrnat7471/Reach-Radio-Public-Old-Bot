import discord
from discord.ext import commands
import asyncio
import datetime
import time
import platform
import json
import requests

start_time = time.time()

class botinfoCog(commands.Cog):
    def get_prefix(client, message):
        with open('config.json', 'r') as f:
            prefixes = json.load(f)

        return prefixes['prefix']

    bot = commands.Bot(command_prefix = get_prefix)

    def __init__(self, bot):
        self.bot = bot

    @bot.command(name='botinfo')
    async def botinfo(self, ctx):
        with open('config.json', 'r') as f:
            logger = json.load(f)
            users = logger['admin']
            for user in users:
                if ctx.message.author.id == user:
                    with open('config.json', 'r') as f:
                        prefixes = json.load(f)
                        version = prefixes['version']
                    ms = self.bot.latency * 1000
                    current_time = time.time()
                    difference = int(round(current_time - start_time))
                    uptime = str(datetime.timedelta(seconds=difference))

                    guilds = len(list(self.bot.guilds))
                    pythonVersion = platform.python_version()
                    dpyVersion = discord.__version__

                    i = 0
                    for guild in self.bot.guilds:
                        i = i + guild.member_count

                    memberCount = i

                    i = 5
                    for vc in self.bot.voice_clients:
                        members = len(vc.channel.members)
                        i = i + members 
                    print("Bot Listeners: ",i)

                    r = requests.get("#")
                    response = r.json()
                    channels = response['icestats']['source']
                    for channel in channels:
                        i = i + channel['listeners']

                    print("All Listeners: ", i)

                    r = requests.get("#")
                    response = r.json()
                    channels = response['icestats']['source']
                    for channel in channels:
                        i = i + channel['listeners']

                    r = requests.get("#")
                    response = r.json()
                    channels = response['icestats']['source']
                    for channel in channels:
                        i = i + channel['listeners']

                    print("All Listeners: ", i)



                    embed = discord.Embed(colour=discord.Colour.blue())
                    embed.set_author(name='Reach Radio Bot Information', icon_url=self.bot.user.avatar_url)
                    embed.timestamp = datetime.datetime.utcnow()
                    embed.set_footer(text=f'Reach Radio Bot {version}', icon_url=self.bot.user.avatar_url)

                    embed.add_field(name="Bot Version", value=f"{version}", inline=True)
                    embed.add_field(name="Python Version", value=f"{pythonVersion}", inline=True)
                    embed.add_field(name="Discord PY Version", value=f"{dpyVersion}", inline=True)
                    embed.add_field(name="Uptime", value=uptime, inline=True)
                    embed.add_field(name="Guilds", value=guilds, inline=True)
                    embed.add_field(name="Members", value=memberCount, inline=True)
                    embed.add_field(name="Listeners", value=i, inline=True)
                    embed.add_field(name="Ping:", value='Pong! {0}ms'.format(round(ms)), inline=True)
                    embed.add_field(name="Website", value="[Reach Radio](https://reachradio.co.uk)", inline=True)
                    embed.add_field(name="Coded by", value="Matt#8038/Nathan7471#7471", inline=True)

                    t = await ctx.channel.send(embed=embed)

                    print(f"[Info Command] ran by {ctx.message.author.name}({ctx.message.author.id}) in {ctx.message.author.guild}({ctx.guild.id})")
                    with open('config.json', 'r') as f:
                        logger = json.load(f)
                        log = logger['logger']
                        for user in log:
                            user = await self.bot.fetch_user(user)
                            await user.send(f"[Info Command] ran by {ctx.message.author.name}({ctx.message.author.id}) in {ctx.message.author.guild}({ctx.guild.id})")

                    await ctx.message.delete()
def setup(bot):
    bot.add_cog(botinfoCog(bot))
