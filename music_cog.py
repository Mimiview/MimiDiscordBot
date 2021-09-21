import discord
import pafy
from discord.channel import VoiceChannel
from discord.ext import commands

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
        best = video.getbestaudio()
        filename = best.download("./assets/songs")
        return video.title

    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            # get the first url
            nomeSong = self.music_queue[0]

            # remove the first element as you are currently playing it
            self.music_queue.pop(0)

            self.vc.play(discord.FFmpegPCMAudio(
                executable="C:Ffmpeg/ffmpeg/bin/ffmpeg.exe", source='./assets/songs/'+nomeSong+'.webm'))
        else:
            self.is_playing = False

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
                         source='./assets/songs/'+nomeSong+'.webm'))  # osservare il metodo play
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
            if type(song) is None:
                await ctx.send("Chicco mettime un link valido o ti pisto")
            else:
                await ctx.send("Provvederò a sburare un pochino di musica")
                self.music_queue.append(song)
                if self.is_playing == False:
                    await self.play_music(voiceChannel)

    @commands.command(name="skip", help="skippa la canzone bro")
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            await self.play_music()

    @commands.command(name="stop", help="skippa la canzone bro")
    async def stop(self):
        if self.vc != "" and self.vc:
            self.vc.stop()
    
 
