import discord
from ast import alias
from discord.ext import commands
from youtube_dl import YoutubeDL

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.is_playing = False
        self.is_paused = False
        self.music_queue = []
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
        self.FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        self.vc = None
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Music.py is ready")
    
    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False
        
        print("search yt ")
        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())

        else:
            self.is_playing = False

    async def play_music(self, ctx):
        if len(self.music_queue) > 0:
            self.is_playing = True
            m_url = self.music_queue[0][0]['source']

            if self.vc == None or not self.vc.is_connected():
                self.vc = await self.music_queue[0][1].connect()

                if self.vc == None:
                    print("connection 1 ")
                    await ctx.send("Could not connect to the voice channel")
                    return
            else:
                await self.vc.move_to(self.music_queue[0][1])
            
            self.music_queue.pop(0)
            print("play ")
            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
            print("play 32")
        
        else:
            print("play no")
            self.is_playing = False
        
    @commands.command(name = "play", aliases = ["p", "playing"])
    async def play(self, ctx, *args):
        print("connection 0 ")
        query = " ".join(args)
        

        voice_channel = ctx.author.voice.channel
        print("connection 1 ")

        if voice_channel is None:
            print("connection 0 ")
            await ctx.send("Please connect to a voice channel")
        elif self.is_paused:
            print("connection 2 ")
            self.vc.resume()
        else:
            song = self.search_yt(query)
            if type(song) == type(True):
                print("connection 3 ")
                await ctx.send("Could not download the song. Incorrect format, try a different keyword")
            else:
                print("connection 4 ")
                await ctx.send("Song added to the queue")
                self.music_queue.append([song, voice_channel])

                if self.is_playing == False:
                    print("5")
                    await self.play_music(ctx)
    
    @commands.command(name = "pause")
    async def pause(self, ctx, *args):
        if self.is_playing:
            self.is_playing = False
            self.is_paused = True
            self.vc.pause()
        elif self.is_paused:
            self.is_playing = True
            self.is_paused = False
            self.vc.resume()
    
    @commands.command(name = "resume", aliases=["res"])
    async def resume(self, ctx, *args):
        if self.is_paused:
            self.is_paused = False
            self.is_playing = True
            self.vc.resume()

    @commands.command(name="skip", aliases=["s"], help="Skips the current song being played")
    async def skip(self, ctx):
        if self.vc != None and self.vc:
            self.vc.stop()
            #try to play next in the queue if it exists
            await self.play_music(ctx)
    
    @commands.command(name = "queue song", aliases=["q"])
    async def queue(self, ctx):
        retval = ""

        for i in range(0, len(self, self.music_queue)):
            if i > 10: break
            retval += self.music_queue[i][0]['title'] + '\n'
        
        if retval != "":
            await ctx.send(retval)
        else: 
            await ctx.send("No music in the queue.")

    @commands.command(name = "ClearMusic", aliases = ["c", "bin"])
    async def clear(self, ctx, *args):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Music queue cleared")
    
    @commands.command(name = "leave", aliases = ["disconnect", "l", "d"])
    async def leave(self, ctx):
        self.is_playing = False
        self.is_paused = False
        await self.vc.disconnect()

