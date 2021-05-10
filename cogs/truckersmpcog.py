import discord
from discord.ext import commands, tasks
import asyncio
import datetime
import json
import requests
import time
from itertools import cycle

class truckersmpCog(commands.Cog):
    def get_prefix(client, message):
        with open('config.json', 'r') as f:
            prefixes = json.load(f)

        return prefixes['prefix']

    bot = commands.Bot(command_prefix = get_prefix)

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def tmp(self, ctx):
        with open('config.json', 'r') as f:
            logger = json.load(f)
            log = logger['logger']
            for user in log:
                user = await self.bot.fetch_user(user)
                user.send(f"[TMP Command] ran by {ctx.message.author.name}({ctx.message.author.id}) in {ctx.message.author.guild}({ctx.guild.id})")
        if ctx.invoked_subcommand is None:
            await ctx.channel.send("Incorrect Command!!! \n \n You can try  ``tmp traffic`` \n ``tmp search (Stream 64ID or TruckersMP ID)`` \n ``tmp servers``")


    @tmp.group()
    async def traffic(self, ctx):
        print(f"[TMP Traffic Command] ran by {ctx.message.author.name}({ctx.message.author.id}) in {ctx.message.author.guild}({ctx.guild.id})")
        if ctx.invoked_subcommand is None:
            r = requests.get("#")
            response = r.json()
            i = 0
            embed = discord.Embed(colour=discord.Colour.blue())
            embed.set_author(name='TruckersMP Simulation 1 Top Locations', icon_url=self.bot.user.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text='Reach Radio Bot v0.0.1', icon_url=self.bot.user.avatar_url)
            for item in response['response']:
                title = response['response'][i]['name']
                player = response['response'][i]['players']
                severity = response['response'][i]['severity']
                trafficjam = response['response'][i]['trafficJams']
                playertrafficjam = response['response'][i]['playersInvolvedInTrafficJams']

                if trafficjam == 0:
                    embed.add_field(name="Location:", value=f"""{title} \n **Severity:** {severity} ({player} players) \n""", inline=True)
                else:
                    embed.add_field(name="Location:", value=f"""{title} \n **Severity:** {severity} ({player} players) \n **Traffic Jams:** {trafficjam} \n **Players In Jams:** {playertrafficjam} \n """, inline=True) 
                i = i+1  
                
            message = await ctx.channel.send(embed=embed)
            await ctx.message.delete()


    @traffic.group()
    async def promods(self, ctx):
        if ctx.invoked_subcommand is None:
            r = requests.get("#")
            response = r.json()
            i = 0
            embed = discord.Embed(colour=discord.Colour.blue())
            embed.set_author(name='TruckersMP ProMods Top Locations', icon_url=self.bot.user.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text='Reach Radio Bot v0.0.1', icon_url=self.bot.user.avatar_url)
            for item in response['response']:
                title = response['response'][i]['name']
                player = response['response'][i]['players']
                severity = response['response'][i]['severity']
                trafficjam = response['response'][i]['trafficJams']
                playertrafficjam = response['response'][i]['playersInvolvedInTrafficJams']

                if trafficjam == 0:
                    embed.add_field(name="Location:", value=f"""{title} \n **Severity:** {severity} ({player} players) \n""", inline=True)
                else:
                    embed.add_field(name="Location:", value=f"""{title} \n **Severity:** {severity} ({player} players) \n **Traffic Jams:** {trafficjam} \n **Players In Jams:** {playertrafficjam} \n """, inline=True) 
                i = i+1  
                    
            message = await ctx.channel.send(embed=embed)
            await ctx.message.delete()

    @traffic.group()
    async def ats(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(colour=discord.Colour.blue(), description="Please choose the following: \n \n ats eusim \n ats sim")
            embed.set_author(name='TruckersMP ATS Help', icon_url=self.bot.user.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text='Reach Radio Bot v0.0.1', icon_url=self.bot.user.avatar_url)
                
            message = await ctx.channel.send(embed=embed)
            await ctx.message.delete()

    @promods.command()
    async def arcade(ctx):
        r = requests.get("#")
        response = r.json()
        i = 0
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name='TruckersMP Promods Arcade Top Locations')
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text='Reach Radio Bot v0.0.1')
        for item in response['response']:
            title = response['response'][i]['name']
            player = response['response'][i]['players']
            severity = response['response'][i]['severity']
            trafficjam = response['response'][i]['trafficJams']
            playertrafficjam = response['response'][i]['playersInvolvedInTrafficJams']

            if trafficjam == 0:
                embed.add_field(name="Location:", value=f"""{title} \n **Severity:** {severity} ({player} players) \n""", inline=True)
            else:
                embed.add_field(name="Location:", value=f"""{title} \n **Severity:** {severity} ({player} players) \n **Traffic Jams:** {trafficjam} \n **Players In Jams:** {playertrafficjam} \n """, inline=True) 
            i = i+1  
            
        await ctx.channel.send(embed=embed)
        await ctx.message.delete()

    @traffic.command()
    async def sim1(self, ctx):
        r = requests.get("https://api.reachradio.co.uk/trucky_cache.php?url=https://api.truckyapp.com/v2/traffic/top&server=sim1&game=ets2")
        response = r.json()
        i = 0
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name='TruckersMP Simulation 1 Top Locations', icon_url=self.bot.user.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text='Reach Radio Bot v0.0.1', icon_url=self.bot.user.avatar_url)
        for item in response['response']:
            title = response['response'][i]['name']
            player = response['response'][i]['players']
            severity = response['response'][i]['severity']
            trafficjam = response['response'][i]['trafficJams']
            playertrafficjam = response['response'][i]['playersInvolvedInTrafficJams']

            if trafficjam == 0:
                embed.add_field(name="Location:", value=f"""{title} \n **Severity:** {severity} ({player} players) \n""", inline=True)
            else:
                embed.add_field(name="Location:", value=f"""{title} \n **Severity:** {severity} ({player} players) \n **Traffic Jams:** {trafficjam} \n **Players In Jams:** {playertrafficjam} \n """, inline=True) 
            i = i+1  
            
        message = await ctx.channel.send(embed=embed)
        await ctx.message.delete()

    @traffic.command()
    async def sim2(self, ctx):
        r = requests.get("#")
        response = r.json()
        i = 0
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name='TruckersMP Simulation 2 Top Locations', icon_url=self.bot.user.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text='Reach Radio Bot v0.0.1', icon_url=self.bot.user.avatar_url)
        for item in response['response']:
            title = response['response'][i]['name']
            player = response['response'][i]['players']
            severity = response['response'][i]['severity']
            trafficjam = response['response'][i]['trafficJams']
            playertrafficjam = response['response'][i]['playersInvolvedInTrafficJams']

            if trafficjam == 0:
                embed.add_field(name="Location:", value=f"""{title} \n **Severity:** {severity} ({player} players) \n""", inline=True)
            else:
                embed.add_field(name="Location:", value=f"""{title} \n **Severity:** {severity} ({player} players) \n **Traffic Jams:** {trafficjam} \n **Players In Jams:** {playertrafficjam} \n """, inline=True) 
            i = i+1  
            
        message = await ctx.channel.send(embed=embed)
        await ctx.message.delete()

    @ats.command()
    async def eusim(self, ctx):
        r = requests.get("#")
        response = r.json()
        i = 0
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name='TruckersMP ATS EU Simulation Top Locations', icon_url=self.bot.user.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text='Reach Radio Bot v0.0.1', icon_url=self.bot.user.avatar_url)
        for item in response['response']:
            title = response['response'][i]['name']
            player = response['response'][i]['players']
            severity = response['response'][i]['severity']
            trafficjam = response['response'][i]['trafficJams']
            playertrafficjam = response['response'][i]['playersInvolvedInTrafficJams']

            if trafficjam == 0:
                embed.add_field(name="Location:", value=f"""{title} \n **Severity:** {severity} ({player} players) \n""", inline=True)
            else:
                embed.add_field(name="Location:", value=f"""{title} \n **Severity:** {severity} ({player} players) \n **Traffic Jams:** {trafficjam} \n **Players In Jams:** {playertrafficjam} \n """, inline=True) 
            i = i+1  
            
        message = await ctx.channel.send(embed=embed)
        await ctx.message.delete()

    @ats.command()
    async def sim(self, ctx):
        r = requests.get("#")
        response = r.json()
        i = 0
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name='TruckersMP ATS Simulation Top Locations', icon_url=self.bot.user.avatar_url)
        embed.timestamp = datetime.datetime.utcnow()
        embed.set_footer(text='Reach Radio Bot v0.0.1', icon_url=self.bot.user.avatar_url)
        for item in response['response']:
            title = response['response'][i]['name']
            player = response['response'][i]['players']
            severity = response['response'][i]['severity']
            trafficjam = response['response'][i]['trafficJams']
            playertrafficjam = response['response'][i]['playersInvolvedInTrafficJams']

            if trafficjam == 0:
                embed.add_field(name="Location:", value=f"""{title} \n **Severity:** {severity} ({player} players) \n""", inline=True)
            else:
                embed.add_field(name="Location:", value=f"""{title} \n **Severity:** {severity} ({player} players) \n **Traffic Jams:** {trafficjam} \n **Players In Jams:** {playertrafficjam} \n """, inline=True) 
            i = i+1  
            
        message = await ctx.channel.send(embed=embed)
        await ctx.message.delete()

    @traffic.group()
    async def arcade(self, ctx):
        if ctx.invoked_subcommand is None:
            r = requests.get("#")
            response = r.json()
            i = 0
            embed = discord.Embed(colour=discord.Colour.blue())
            embed.set_author(name='TruckersMP Arcade Locations', icon_url=self.bot.user.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text='Reach Radio Bot v0.0.1', icon_url=self.bot.user.avatar_url)
            for item in response['response']:
                title = response['response'][i]['name']
                player = response['response'][i]['players']
                severity = response['response'][i]['severity']
                trafficjam = response['response'][i]['trafficJams']
                playertrafficjam = response['response'][i]['playersInvolvedInTrafficJams']

                if trafficjam == 0:
                    embed.add_field(name="Location:", value=f"""{title} \n **Severity:** {severity} ({player} players) \n""", inline=True)
                else:
                    embed.add_field(name="Location:", value=f"""{title} \n **Severity:** {severity} ({player} players) \n **Traffic Jams:** {trafficjam} \n **Players In Jams:** {playertrafficjam} \n """, inline=True) 
                i = i+1  
                    
            message = await ctx.channel.send(embed=embed)
            await ctx.message.delete()



    @tmp.command()
    async def servers(self, ctx):
        r = requests.get("#")
        response = r.json()
        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_footer(text='Provided by TruckersMP API')
        embed.set_author(name=f"TruckersMP Server Status", icon_url=self.bot.user.avatar_url)
        i = 0
        res = 'response'
        for server in response['response']:
            if response[res][i]['game'] == "ETS2":
                game = "ETS2"
            else:
                game = "ATS"

            if response[res][i]['shortname'] == "EVENT":
                embed.add_field(name='\u200b', value=f"""**Game: ** {game}
                    **Server:** {response[res][i]['name']}
                    **Players:** {response[res][i]['players']}/{response[res][i]['maxplayers']}""", inline=True)

            else:
                embed.add_field(name='\u200b', value=f"""**Game: ** {game}
                    **Server:** {response[res][i]['shortname']}
                    **Players:** {response[res][i]['players']}/{response[res][i]['maxplayers']}""", inline=True)

            i = i+1

        await ctx.channel.send(embed=embed)
        await ctx.message.delete()

    @tmp.command()
    async def search(self, ctx, message):
        r = requests.get("#"+message)
        response = r.json()
        i = 'response'
        steam = response[i]['steamID']
        vtcid = response[i]['vtc']['id']
        vtcname = response[i]['vtc']['name']
        tmpname = response[i]['name']
        tmpid = response['response']['id']

        embed = discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name=f"TruckersMP Profile Search", icon_url=self.bot.user.avatar_url)

        if response['response']['banned'] == False:
                ban = "Not Banned"
        else:
                ban = "Banned"

        embed.add_field(name='**ID:**', value=f"{response['response']['id']}", inline=True)
        embed.add_field(name='**Name:**', value="[" + str(tmpname) + "](https://truckersmp.com/user/" + str(tmpid) + ")", inline=True)
        embed.add_field(name='**Created Account:**', value=f"{response[i]['joinDate']}", inline=True)
        embed.add_field(name='**SteamID:**', value=f"[{steam}](https://steamcommunity.com/profiles/{steam})", inline=True)
        embed.add_field(name='**Team:**', value=f"{response[i]['groupName']}", inline=True)
        embed.add_field(name='**Banned:**', value=f"{ban}", inline=True)
        embed.add_field(name='**VTC:**', value="[" + str(vtcname) + "](https://truckersmp.com/vtc/" + str(vtcid) + ")", inline=True)
        embed.set_thumbnail(url=f"{response['response']['avatar']}")
        embed.set_footer(text='Provided by TruckersMP API')

        await ctx.channel.send(embed=embed)
        print(f"[TMP Search Command] ran by {ctx.message.author.name}({ctx.message.author.id}) in {ctx.message.author.guild}({ctx.guild.id})")
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(truckersmpCog(bot)) 