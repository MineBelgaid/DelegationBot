from discord.ext.commands.core import command
import youtube_dl,discord
from discord.ext import commands

class Voice(commands.Cog,name="Voice"):
    def __init__(self,bot:commands.Bot):
        self.bot=bot
    
    @commands.command()
    async def join(self,ctx):
        user = ctx.message.author
        vc = user.voice.channel
        voice = discord.utils.get(self.bot.voice_clients,guild =ctx.guild)
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel!")
        voice_channel = ctx.author.voice.channel
        if voice is None:
            await vc.connect()
            await ctx.send("Delegation has arrived to the channel!")
        else:
            await ctx.send("I'm already in an existing channel")


    @commands.command()
    async def disconnect(self, ctx):
        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)
        if voice_client is not None:
            await ctx.voice_client.disconnect()
            await ctx.send("Succesfully left the channel ! ")
        else :
            await ctx.send("I am not connected") 

    @commands.command()
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.send("Paused ! ")
        

    @commands.command()
    async def resume(self, ctx):
        await ctx.voice_client.resume()
        await ctx.send("Resumed ! ")

    @commands.command()
    async def play(self, ctx, url):
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format': "bestaudio"}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, ** FFMPEG_OPTIONS)
            vc.play(source)
            ctx.send("Now playing ")
        

def setup(bot:commands.Bot):
    bot.add_cog(Voice(bot))
