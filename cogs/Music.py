import discord
from ast import alias
from discord.ext import commands
import youtube_dl 
from youtube_dl import YoutubeDL
import asyncio

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.YDL_OPTIONS = {'format': 'bestaudio'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.music_queue = []
        self.client.loop.create_task(self.playmusic()) #looping task
        self.voice = None
        self.channel = None

    @commands.Cog.listener()
    async def on_ready(self):
        print("Music.py is ready")  
        

    @commands.command()
    async def join(self, ctx):
        print("joined")
        if ctx.author.voice is None:
            await ctx.send("You are not in a voice channel!")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
            self.channel = ctx
            self.voice = ctx.voice_client
        else:
            await ctx.voice_client.move_to(voice_channel)
            self.channel = ctx
            self.voice = ctx.voice_client
    
    @commands.command(name="disconnet", alias = ["dc"])
    async def disconnect(self, ctx):
        self.music_queue = []
        self.voice = None
        self.channel = None
        await ctx.voice_client.disconnect()

    @commands.command(name = "play", alias=["p","music"])
    async def play(self, ctx, url = None):
        #ctx.voice_client.stop()
        #self.voice = ctx.voice_client
        with youtube_dl.YoutubeDL(self.YDL_OPTIONS) as ydl:
            if url is not None:
                info = ydl.extract_info(url, download=False)
                url2 = info['formats'][0]['url']
                source = await discord.FFmpegOpusAudio.from_probe(url2, **self.FFMPEG_OPTIONS)
                await ctx.send("Added to queue")
                self.music_queue.append([url, source])
            else:
                 await ctx.send("Error: Missing Required Arguments. You must pass in a valid youtube url")


    async def playmusic(self):
        await self.client.wait_until_ready()
        while not self.client.is_closed():
            
            print("loop")
            if self.voice != None:
                print("loop1")
                if not self.voice.is_playing() and not self.voice.is_paused():
                    print("loop3")
                    if len(self.music_queue) != 0:
                        print("play")
                        pop = self.music_queue.pop() #gets the source
                        await self.channel.send(f"Playing: {pop[0]}")
                        print("playing")
                        self.voice.play(pop[1])
            await asyncio.sleep(3)

    @commands.command()
    async def pause(self,ctx):
        await ctx.voice_client.pause()
        await ctx.send("Paused ")

    @commands.command()
    async def resume(self,ctx):
        await ctx.voice_client.resume()
        await ctx.send("Resumed")
    
    @commands.command()
    async def queue(self,ctx):
        await ctx.send("Current Queue:")
        for i in range(len(self.music_queue)):
            await ctx.send(f"{i} : {self.music_queue[i][0]}")

    @commands.command()
    async def skip(self,ctx):
        await ctx.voice_client.stop()  
        await ctx.send("Skipped")


async def setup(client):
    await client.add_cog(Music(client))

