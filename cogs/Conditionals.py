import discord
from discord.ext import commands
import datetime
import time

#
class Conditionals(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Conditionals.py is online")
    
    @commands.command()
    async def hello(self, ctx):
        commands_channel = discord.utils.get(ctx.guild.channels, name="bot")
        if ctx.channel.id == commands_channel.id:
            await ctx.send("Command ran succesfully!")
    
    @commands.command()
    async def dev(self, ctx):

        if ctx.author.id == 738676736144703531: # list of ids = [738676736144703531, 738676736144703531, 738676736144703531]
            await ctx.send("Command ran sucessfully")
        else:
            await ctx.send("Can't run because you do not have permission")
    
    


async def setup(client):
    await client.add_cog(Conditionals(client))
