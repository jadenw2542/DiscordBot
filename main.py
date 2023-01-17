import discord
from discord.ext import commands, tasks
import random 
from itertools import cycle 
import os
import asyncio
import json

#returns server_prefix from prefixes.json
def get_server_prefix(client, message):
    with open("cogs/jsonfiles/prefixes.json", "r") as f:
        prefix = json.load(f)
    return prefix[str(message.guild.id)]

client = commands.Bot(command_prefix=get_server_prefix, intents=discord.Intents.all())
client.remove_command("help")


bot_status = cycle(["type in '!help' for help", "Status Two"])

#simple loop to change bot's status
@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(bot_status)))



#generates prefix for guild and stores in prefixes.json
@client.event
async def on_guild_join(guild):
    with open("cogs/jsonfiles/prefixes.json","r") as f:
        prefix = json.load(f)

    prefix[str(guild.id)] = "!"

    with open("cogs/jsonfiles/prefixes.json", "w") as f:
        json.dump(prefix, f , indent=4)


    with open("cogs/jsonfiles/mutes.json", "r") as f:
        mute_role = json.load(f)
        mute_role[str(guild.id)]= None

    with open("cogs/jsonfiles/mutes.json", "w") as f:
        json.dump(mute_role, f, indent=4)


    with open("cogs/jsonfiles/autorole.json", "r") as f:
        auto_role = json.load(f)
        auto_role[str(guild.id)] = None
    
    with  open("cogs/jsonfiles/autorole.json", "w") as f:
        json.dump(auto_role, f, indent=4)
    

    with open("cogs/jsonfiles/welcome.json", "r") as f:
        data = json.load(f)
        data[str(guild.id)] = {}
        data[str(guild.id)]["AutoRole"] = None
        data[str(guild.id)]["Channel"] = None
        data[str(guild.id)]["Message"] = None
        data[str(guild.id)]["ImageUrl"] = None
        
    with open("cogs/jsonfiles/welcome.json", "w") as f:
        json.dump(data, f, indent=4)


#deletes prefix from prefixes.json for guild when it is kicked from the server
@client.event
async def on_guild_remove(guild):
    with open("cogs/jsonfiles/prefixes.json","r") as f:
        prefix = json.load(f)

    prefix.pop(str(guild.id))

    with open("cogs/jsonfiles/prefixes.json", "w") as f:
        json.dump(prefix, f , indent=4)


    with open("cogs/jsonfiles/mutes.json", "r") as f:
        mute_role = json.load(f)
        mute_role.pop(str(guild.id))

    with open("cogs/jsonfiles/mutes.json", "w") as f:
        json.dump(mute_role, f, indent=4)


    with open("cogs/jsonfiles/autorole.json", "r") as f:
        auto_role = json.load(f)
    
    auto_role.pop(str(guild.id))
    
    with open("cogs/jsonfiles/autorole.json", "w") as f:
        json.dump(auto_role, f, indent=4)


    with open("cogs/jsonfiles/welcome.json", "r") as f:
        data = json.load(f)

    data.pop(str(guild.id))
    
    with open("cogs/jsonfiles/welcome.json", "w") as f:
        json.dump(data, f, indent=4)    

#sets prefix for server and stores data in prefixes.json
@client.command()
async def setprefix(ctx, *, newprefix: str):
    with open("cogs/jsonfiles/prefixes.json","r") as f:
        prefix = json.load(f)

    prefix[str(ctx.guild.id)] = newprefix

    with open("cogs/jsonfiles/prefixes.json", "w") as f:
        json.dump(prefix, f , indent=4)    

    await ctx.send(f"Prefix set to: {newprefix}")   

#prints out all commands 
@client.command()
async def all_commands(ctx):
    await ctx.send(f"Avaliable commands: \n !ping \n !magic_eightball (question) \n !kick (user#999) \n !ban (user#999) \n !unban (user#999) \n !setprefix (new prefix)" )

#magic eightball
@client.command(aliases=["8ball", "eightball", "eight ball", "8 ball"])
async def magic_eightball(ctx, *, question):
    with open("magic_eightball_responses.txt", "r") as f:
        random_responses = f.readlines()
        response = random.choice(random_responses)

    await ctx.send(response)

"""
#ping slash commmand
@client.tree.command(name="ping", description="shows the bot's latency in ms.") # slash command  uses interaction instead of ctx
async def ping(interaction: discord.Interaction):
    bot_latency = round(client.latency * 1000)
    await interaction.response.send_message(f"Pong! {round(bot_latency * 1000)} ms.)")
"""

@client.hybrid_command(name="ping", description= "Sends pong!")
async def ping(ctx):
    await ctx.send("pong!")


#loads in all cogs
async def load(): 
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")
            #print(f"{filename[:-3]} is loaded!")

async def main():
    async with client:
        await load()
        await client.start("YOUR TOKEN")


@client.event
async def on_ready():
    await client.tree.sync()
    print("Success: Bot is connected to Discord!")
    change_status.start()

#error handling
#@client.event
#async def on_command_error(ctx, error):
#    if isinstance(error, commands.MissingRequiredArgument):
#        await ctx.send("Error: Missing Required Arguments. Are you sure you provided __all__ required arguments")
#   #if isinstance(error, commands.)




asyncio.run(main())
#client.run("MTA1Njc1MzYyMTA4NzI4OTQwNQ.G731yq.JJF5MYLBx9ErJLxaIZreRaEV0XPUnuhHHWLLXU") #token 



"""
@client.event
async def on_ready():
    print("Success: Bot is connected to Discord")
    #change_status.start()
"""

"""
@client.command()
async def ping(ctx):

    bot_latency = round(client.latency * 1000)
    await ctx.send(f"Pong! {bot_latency} ms.")
    #await ctx.send("Pong!")
    #await ctx.author.send("Pong!")  msgs user
"""