import discord 
from discord.ext import commands

class Moderation(commands.Cog):
    def __init__(self,client):
        self.client = client 
    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation.py is online")
    
    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, count: int):
        await ctx.channel.purge(limit=count)
        await ctx.send(f"{count} message(s) cleared")

    @commands.command()
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, *, modreason):
        await ctx.guild.kick(member)

        conf_embed = discord.Embed(title="Success!", color = discord.Color.green())
        conf_embed.add_field(name="Kicked:", value=f"{member.mention} has been kicked from the server by {ctx.author.mention}.", inline=False)
        conf_embed.add_field(name="Reason:", value=modreason, inline=False)

        await ctx.send(embed=conf_embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, modreason):
        
        await ctx.guild.ban(member)

        conf_embed = discord.Embed(title="Success!", color = discord.Color.green())
        conf_embed.add_field(name="Banned:", value=f"{member.mention} id: {member.id} has been banned from the server by {ctx.author.mention}.", inline=False)
        conf_embed.add_field(name="Reason:", value=modreason, inline=False)

        await ctx.send(embed=conf_embed)

    @commands.command(name="unban")
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, discordID):
        #banned_users = await ctx.guild.bans()
        if '#' not in discordID:   
            print("end")
            await ctx.send("Not a banned person")        
            
        name, number = discordID.split('#')

        async for ban_entrys in ctx.guild.bans():
            entry = ban_entrys.user
            if((entry.name, entry.discriminator) == (name, number)):
                await ctx.guild.unban(entry)
                conf_embed = discord.Embed(title="Success!", color = discord.Color.green())
                conf_embed.add_field(name="Unbanned:", value=f"{entry.display_name} id: {entry.id} has been unbanned from the server by {ctx.author.mention}.", inline=False)
                await ctx.send(embed=conf_embed)
                return
        print("end")
        await ctx.send("Not a banned person")        
        """
        user = discord.Object(id=userId)
        await ctx.guild.unban(user)
        """

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Error: Missing Required Arguments. You must pass in a whole number in order to run the clear command.")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Error: Missing permissions: You must have permission manage messages.")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Error: Missing Required Arguments. You must pass in a userID or a @ mention and a reason. ")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Error: Missing permissions: You must have permission to kick members.")            
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Error: Missing Required Arguments. You must pass in a userID or a @ mention and a reason.")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Error: Missing permissions: You must have permission to ban members.")       

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Error: Missing Required Arguments. You must pass in a userID or a @ mention.")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Error: Missing permissions: You must have permission to unban members.")

async def setup(client):
    await client.add_cog(Moderation(client))