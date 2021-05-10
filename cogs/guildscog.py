import discord
from discord.ext import commands
import asyncio
import datetime
import json

class guildsCog(commands.Cog):
    def get_prefix(client, message):
        with open('config.json', 'r') as f:
            prefixes = json.load(f)

        return prefixes['prefix']

    bot = commands.Bot(command_prefix = get_prefix)
    bot.remove_command('help')

    def __init__(self, bot):
        self.bot = bot

    @bot.command(name='guildlist')
    async def guidlist(self, ctx):
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
def setup(bot):
    bot.add_cog(guildsCog(bot))
