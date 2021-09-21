import discord
from discord.channel import VoiceChannel
from discord.ext import commands

from youtube_dl import YoutubeDL


class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False

        self.music_queue = []
        self.vc = ""
        self.YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        self.FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    def search_yt(self, item):
        with YoutubeDL(self.YDL_OPTIONS) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" %
                                        item, download=False)['entries'][0]
            except Exception:
                return False

        return {'source': info['formats'][0]['url'], 'title': info['title']}

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #get the first url
            m_url = self.music_queue[0][0]['source']

            #remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next())
        else:
            self.is_playing = False


    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            #prendi l'url del primo
            m_url = self.music_queue[0][0]['source']


            #  questo mi connette il bot al voicechannel corrente
            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.music_queue[0][1].connect()
            else : 
                await self.vc.move_to(self.music_queue[0][1])


            
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(
                m_url, **self.FFMPEG_OPTIONS), after=lambda e: self.play_next()) #osservare il metodo play
        else:
            self.is_playing = False


    @commands.command(name="play", help="Plays a selected song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)

        voiceChannel = ctx.author.voice.channel

        if voiceChannel is None: 
            await ctx.send("Entra in un cazzo di canale fra!")
        else: 
            song = self.search_yt(query)
            if type(song) == True: 
                await ctx.send("Chicco mettime un link valido o ti pisto")
            else : 
                await ctx.send("Provvederò a sburare un pochino di musica")
                self.music_queue.append([song, voiceChannel])

                if self.is_playing == False: 
                    print("CHICCOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
                    await self.play_music()

    @commands.command(name="skip", help="skippa la canzone bro")
    async def skip(self, ctx):
        if self.vc !="" and self.vc:
            self.vc.stop()
            await self.play_music()

