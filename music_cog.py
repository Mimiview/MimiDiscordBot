import discord
import pafy
from discord.channel import VoiceChannel
from discord.ext import commands
import time
import youtube_dl

from youtube_dl import YoutubeDL


class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False

        self.music_queue = []
        self.vc = ""

    def search_yt(self, item):
        video = pafy.new(item)
        print(video.rating)
        best = video.getbest()
        filename = best.download("./assets/songs")
        return video.title

    def youtube_dl_search(self, item):
        ydl_opts = {'format': 'bestaudio/best',
                    'noplaylist': True,
                    'postprocessors': [{ #TODO look up for the option documentation and also fot "ffprobe/avprobe and ffmpeg/avconv not found. Please install one."'s issue 
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': './assets/songs/%(title)s.%(ext)s'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(
                'https://www.youtube.com/watch?v=ITc6xZJ60oY&ab_channel=LAW-Tutorials', download=True)

    async def play_music(self, channel):
        if len(self.music_queue) > 0:
            self.is_playing = True

            # prendi l'url del primo
            nomeSong = self.music_queue[0]

            #  questo mi connette il bot al voicechannel corrente
            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await channel.connect()
            else:
                await self.vc.move_to(channel)

            self.music_queue.pop(0)

            # todo aggiugnere ffmpeg
            self.vc.play(discord.FFmpegPCMAudio(executable="C:/Ffmpeg/ffmpeg/bin/ffmpeg.exe",
                         source='./assets/songs/'+nomeSong+'.mp4'))
            print("Current Playing: "+nomeSong)   # osservare il metodo play

            # mi contrtolla costantemente se una canzone è in playing
            while self.vc.is_playing():
                time.sleep(3)
            # TODO devi cercare di capire in che modo far waitare e farlo funzionare bro
            self.play_music(channel)

        else:
            self.is_playing = False
            if self.vc.is_connected():
                self.vc.disconnect()

    @commands.command(name="play", help="Plays a selected song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)

        voiceChannel = ctx.author.voice.channel

        if voiceChannel is None:
            await ctx.send("Entra in un cazzo di canale fra!")
        else:
            song = self.search_yt(query)
            if type(song) is None:
                await ctx.send("Chicco mettime un link valido o ti pisto")
            else:
                await ctx.send("Provvederò a sburare un pochino di musica")
                self.music_queue.append(song)
                if self.is_playing == False:
                    self.play_music(voiceChannel)

    @commands.command(name="skip", help="skippa la canzone bro")
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            print("Stoppato e skippato")
            await self.play_music(self.vc.channel)

    @commands.command(name="stop", help="skippa la canzone bro")
    async def stop(self):
        if self.is_playing == True:
            print("Stoppa ziooo")
            self.vc.stop()
