import discord
from discord.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("HelpCommand.py is online")
    
    @commands.command()
    async def help(self, ctx):
        help_embed = discord.Embed(title= "Help Desk for Jaden Bot", description="All available commands", color=discord.Color.random())
        help_embed.set_author(name="Jaden Bot", icon_url= ctx.guild.icon)
        help_embed.add_field(name="setprefix", value="Changes the prefix of this bot(default is !)", inline=False)
        help_embed.add_field(name="magic_eightball", value="Ask the magic eightball a question!", inline=False)
        help_embed.add_field(name="ping", value="Pings the bot.", inline=False)
        help_embed.add_field(name="clear", value="Deletes a specified amount of messages.", inline=False)
        help_embed.add_field(name="kick", value="Kicks user from guild/server.", inline=False)
        help_embed.add_field(name="ban", value="Ban user from guild/server.", inline=False)
        help_embed.add_field(name="unban", value="Unban user from guild/server.", inline=False)
        help_embed.add_field(name="setmuterole", value="Sets the default mute role", inline=False)
        help_embed.add_field(name="mute", value="Mutes specified user.", inline=False)
        help_embed.add_field(name="unmute", value="Unmutes specified user.", inline=False)
        help_embed.add_field(name="level", value="Check the level of a specified user.", inline=False)
        help_embed.add_field(name="joinrole", value="Sets the automatic join role for new members.", inline=False)
        help_embed.add_field(name="play", value="Plays music (youtube url)", inline=False)
        help_embed.add_field(name="skip", value="Skips current song", inline=False)
        help_embed.add_field(name="pause", value="Pauses current song", inline=False)
        help_embed.add_field(name="resume", value="Resumes current song", inline=False)
        help_embed.add_field(name="queue", value="View the queue of all songs", inline=False)
        help_embed.set_footer(text=f"Requested by <@{ctx.author}>.", icon_url=ctx.author.avatar)
        help_embed.add_field(name="Need Help?", value="[Join support server]...", inline=False)

        await ctx.send(embed=help_embed)


async def setup(client):
    await client.add_cog(HelpCommand(client))