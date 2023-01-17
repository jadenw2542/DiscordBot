import discord
from discord.ext import commands
import json

#assigns role to member on server join
class Automation(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Automation.py is ready")
    
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        with open("cogs/jsonfiles/autorole.json", "r") as f:
            auto_role = json.load(f)    
            join_role = discord.utils.get(member.guild.roles, name=auto_role[str(member.guild.id)])
            #await member.add_roles(join_role) #replaced by Welcome.py



    #set role to assign to new members, role must be lower on hiearchy than the bot
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def joinrole(self, ctx, role: discord.Role): #!joinrole role_id
        with open("cogs/jsonfiles/autorole.json", "r") as f:
            auto_role = json.load(f)
        
        auto_role[str(ctx.guild.id)] = str(role.name)

        with open("cogs/jsonfiles/autorole.json", "w") as f:
            json.dump(auto_role, f, indent=4)
        
        conf_embed = discord.Embed(color=discord.Color.green())
        conf_embed.add_field(name="Success!", value=f"The automatic role for this guild/server has been set to {role.mention}.")
        conf_embed.set_footer(text=f"Action taken by {ctx.author.name}.")

        await ctx.send(embed=conf_embed)

    @joinrole.error
    async def joinrole(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("Error: Missing Required Arguments. You must pass in a valid role to be set as the join role.")
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("Error: Missing permissions: You must have adminstrator permissions.")   


async def setup(client):
    await client.add_cog(Automation(client))