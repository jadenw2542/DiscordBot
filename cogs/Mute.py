import discord
from discord.ext import commands
import json
 
 #Sets a role to mute role
class Mute(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.Cog.listener()
    async def on_ready(self):
        print("Mute.py is online")
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setmuterole(self, ctx, role: discord.Role):
        print("test1")
        with open("cogs/jsonfiles/mutes.json","r") as f:
            print("test1")
            mute_role = json.load(f)
            print("test1")
            mute_role[str(ctx.guild.id)] = role.name
        
        with open("cogs/jsonfiles/mutes.json","w") as f:
            json.dump(mute_role, f, indent = 4)
        
        conf_embed = discord.Embed(title = "Success!", color = discord.Color.green())
        conf_embed.add_field(name = "Mute role has been set!", value = f"The mute role has been changed to '{role.mention}' for this guild. All members who are muted will be equipped with this role.")

        await ctx.send(embed=conf_embed)

    #gives mute role to discord member
    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member):

        with open("cogs/jsonfiles/mutes.json","r") as f:
            role = json.load(f)
            mute_role = discord.utils.get(ctx.guild.roles, name=role[str(ctx.guild.id)])

        #You must have manage_roles to use this, and the added Roles must appear lower in the list of roles than the highest role of the member.
        await member.add_roles(mute_role)

        conf_embed = discord.Embed(title="Success!", color=discord.Color.green())

        conf_embed.add_field(name="Muted", value=f"{member.mention} has been muted by {ctx.author.mention}.", inline=False)

        await ctx.send(embed = conf_embed)
        print("test 21059314746576355418")

    @commands.command()
    @commands.has_permissions(manage_roles=True)

    #removes mute role to discord member
    async def unmute(self, ctx, member: discord.Member):
        with open("cogs/jsonfiles/mutes.json","r") as f:
            role = json.load(f)

            mute_role = discord.utils.get(ctx.guild.roles, name=role[str(ctx.guild.id)])
        
        await member.remove_roles(mute_role)

        conf_embed = discord.Embed(title="Success!", color=discord.Color.green())
        conf_embed.add_field(name="Unmuted", value=f"{member.mention} has been unmuted by {ctx.author.mention}.", inline=False)
        await ctx.send(embed = conf_embed)


    @setmuterole.error
    async def setmuterole_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Error: Missing Required Arguments. You must pass in valid role to be set as the mute role.")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Error: Missing permissions: You must have adminstrator permissions.")
    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Error: Missing Required Arguments.  You must pass in a userID or a @ mention.")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Error: Missing permissions: You must have manage role permissions.")
    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Error: Missing Required Arguments.  You must pass in a userID or a @ mention.")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Error: Missing permissions: You must have manage role permissions.")    

async def setup(client):
    await client.add_cog(Mute(client))