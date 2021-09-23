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
        self.vc = ""  # voice channel

    def search_yt(self, item):
        video = pafy.new(item)
        print(video.rating)
        best = video.getbest()
        filename = best.download("./assets/songs")
        return video.title

    def youtube_dl_search():
        ydl_opts = {'format': 'bestaudio/best',
                    # if they setn a playlist it would not consider it? #TODO study the behaviour
                    'noplaylist': True,
                    # location where ffmep is situated
                    'ffmpeg_location': 'C:/Ffmpeg/ffmpeg/bin/ffmpeg.exe',
                    'postprocessors': [{  # postprocess options
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '128',
                    }],
                    'outtmpl': './assets/songs/%(title)s.%(ext)s'}  # output path

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(
                'https://www.youtube.com/watch?v=V2mnB2gYEMs&ab_channel=Rondodasosa', download=True)
        return [meta.get('title', None)] #TODO back-end handling

    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            # prendi l'url del primo
            nomeSong = self.music_queue[0]

            #  questo mi connette il bot al voicechannel corrente
            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await self.vc.connect()
            else:
                # TODO da vedere se si sposta o meno
                await self.vc.move_to(self.vc)

            self.music_queue.pop(0)

            #TODO vedere la lambda se funziona o meno e estudioia
            self.vc.play(discord.FFmpegPCMAudio(executable="C:/Ffmpeg/ffmpeg/bin/ffmpeg.exe",
                         source='./assets/songs/'+nomeSong+'.mp4'))
            print("Current Playing: "+nomeSong)   # osservare il metodo play

            # mi contrtolla costantemente se una canzone è in playing
            while self.vc.is_playing():
                time.sleep(3)
            # TODO devi cercare di capire in che modo far waitare e farlo funzionare bro
            self.play_music()

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
                    self.play_music()

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
