import discord
from discord.ext import commands, tasks
import asyncio
import datetime
import ffmpeg
import json
import requests
import time
from itertools import cycle

class shoutoutCog(commands.Cog):
    def get_prefix(client, message):
        with open('config.json', 'r') as f:
            prefixes = json.load(f)

        return prefixes['prefix']

    bot = commands.Bot(command_prefix = get_prefix)


    def __init__(self, bot):
        self.bot = bot

    @bot.command(name='shoutout')
    async def message(self, ctx, *, message):
        h = open('config.json', 'r')
        h = json.load(h)
        header = h['headers']

        response = requests.post('#',
            data={ 
            "name": f"{ctx.message.author.name}",
            "type": "Message",
            "requestOrigin": "Reach Radio Public Bot",
            "message": f"{message}"
        }, headers=header)

        print(f"[Message Command] ran by {ctx.message.author.name}({ctx.message.author.id}) in {ctx.message.author.guild}({ctx.guild.id})")
        if response.status_code == 201:
            embed = discord.Embed(colour=discord.Colour.green(), title="Success", description="Your shoutout message was successfully sent!")
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text=f'Reach Radio', icon_url=self.bot.user.avatar_url)
            await ctx.message.delete()
            botmsg = await ctx.channel.send(embed=embed)
            await asyncio.sleep(10)
            botmsg.delete()
            with open('config.json', 'r') as f:
                logger = json.load(f)
                log = logger['logger']
                for user in log:
                    user = await self.bot.fetch_user(user)
                    await user.send(f"[Message Command] ran by {ctx.message.author.name}({ctx.message.author.id}) in {ctx.message.author.guild}({ctx.guild.id})")
            return
        else:
            r = response.content.decode('UTF-8')
            r = json.loads(r)
            embed = discord.Embed(colour=discord.Colour.red(), title="Error", description=f"{str(r['error'])} ({str(r['statusCode'])}) ```json\n{str(r['message'])}``` \n This has been reported to our development team so please try again later.")
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text=f'Reach Radio', icon_url=self.bot.user.avatar_url)
            with open('config.json', 'r') as f:
                logger = json.load(f)
                log = logger['logger']
                for user in log:
                    user = await self.bot.fetch_user(user)
                    await user.send(f"<@510238066829688832> [Message Command] ran by {ctx.message.author.name}({ctx.message.author.id}) in {ctx.message.author.guild}({ctx.guild.id})", embed=embed)
            await ctx.channel.send(embed=embed)
            await asyncio.sleep(10)
            await ctx.message.delete()
            return


def setup(bot):
    bot.add_cog(shoutoutCog(bot))
