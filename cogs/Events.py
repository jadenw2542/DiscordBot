import discord
from discord.ext import commands
import datetime
import time

#logger
class Events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("Events.py is online")

    @commands.Cog.listener()
    async def on_message(self, message):
        '''
        log_channel = discord.utils.get(message.guild.channels,  name="log-channel")
        event_embed = discord.Embed(title="Message Logged", description="Message's contents and origin.", color=discord.Color.green())
        event_embed.add_field(name="Message Author: ", value=message.author.mention, inline=False)
        event_embed.add_field(name="Channel Origin:", value=message.channel.mention, inline=False)
        event_embed.add_field(name="Message Content:", value=message.content, inline=False)
        date = datetime.datetime.now()
        event_embed.add_field(name="Time sent:", value=date, inline=False)
        await log_channel.send(embed=event_embed)
        '''

    @commands.Cog.listener()
    async def on_member_join(self, member):
        log_channel = discord.utils.get(member.guild.channels,  name="log-channel")
        event_embed = discord.Embed(title="Arrival Logged", description="This user joined the server", color=discord.Color.green())
        event_embed.add_field(name="User Joined:", value= member.mention, inline=False)
        date = datetime.datetime.now()
        event_embed.add_field(name="Time Joined:", value=date, inline=False)
        await log_channel.send(embed=event_embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        log_channel = discord.utils.get(member.guild.channels,  name="log-channel")
        event_embed = discord.Embed(title="Departure Logged", description="This user left the server", color=discord.Color.green())
        event_embed.add_field(name="User Left:", value= member.mention, inline=False)
        date = datetime.datetime.now()
        event_embed.add_field(name="Time Left:", value=date, inline=False)

        await log_channel.send(embed=event_embed)

async def setup(client):
    await client.add_cog(Events(client))
