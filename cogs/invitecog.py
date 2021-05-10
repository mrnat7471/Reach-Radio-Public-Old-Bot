import discord
from discord.ext import commands
import asyncio
import datetime
import time
import json

start_time = time.time()

class inviteCog(commands.Cog):
    def get_prefix(client, message):
        with open('config.json', 'r') as f:
            prefixes = json.load(f)

        return prefixes['prefix']

    bot = commands.Bot(command_prefix = get_prefix)

    def __init__(self, bot):
        self.bot = bot

    @bot.command(name='invite')

    async def say_embed(self, ctx):
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name='Reach Radio Invite', icon_url=self.bot.user.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_image(url='https://media1.tenor.com/images/24aaee6aef322e6dee41f029b233c8cc/tenor.gif')
        embed.set_footer(text=f'Reach Radio Bot', icon_url=self.bot.user.avatar_url) 
        embed.add_field(name="Invite Me:", value="Thanks for wanting to invite me: [Invite Link](#)", inline=True)

        await ctx.channel.send(embed=embed)
        with open('config.json', 'r') as f:
            logger = json.load(f)
            log = logger['logger']
            for user in log:
                user = await self.bot.fetch_user(user)
                await user.send(f"[Invite Command] ran by {ctx.message.author.name}({ctx.message.author.id}) in {ctx.message.author.guild}({ctx.guild.id})")
        print(f"[Invite Command] ran by {ctx.message.author.name}({ctx.message.author.id}) in {ctx.message.author.guild}({ctx.guild.id})")
        await ctx.message.delete()
def setup(bot):
    bot.add_cog(inviteCog(bot)) 