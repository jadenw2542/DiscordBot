import discord 
from discord.ext import commands

#testing embeds
class MyCog(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener() #evnet lisenter
    async def on_ready(self):
        print("MyCog.py is online")
    @commands.command()
    async def embed(self,ctx):
        embed_message = discord.Embed(title = "Title", description="description", color=discord.Color.gold())

        embed_message.set_author(name = f"Requested by {ctx.author.mention}", icon_url=ctx.author.avatar)
        embed_message.set_thumbnail(url=ctx.guild.icon)
        embed_message.set_image(url=ctx.guild.icon)
        embed_message.add_field(name="Field name", value="Field value", inline= False)
        embed_message.set_footer(text="Footer", icon_url= ctx.author.avatar)

        await ctx.send(embed=embed_message)


async def setup(client):
    await client.add_cog(MyCog(client))
