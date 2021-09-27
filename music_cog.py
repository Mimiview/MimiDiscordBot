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
                        'preferredquality': '192',
                    }],
                    'outtmpl': './assets/songs/%(title)s.%(ext)s'}  # output path

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(
                'https://www.youtube.com/watch?v=V2mnB2gYEMs&ab_channel=Rondodasosa', download=True)
        return [meta.get('title', None)] #TODO back-end handling

    async def play_music(self,channel):
        print('Canzoni in coda: ',len(self.music_queue))
        if len(self.music_queue) > 0:
            self.is_playing = True

            # prendi l'url del primo
            nomeSong = self.music_queue[0]
            #TODO vedere se una canzone è in stop

            #  questo mi connette il bot al voicechannel corrente
            #TODO vedere se connetterlo al di fuori(ossia nella play) per poi provare a poter fare il resume
            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await channel.connect()
                print('Entrato nel Canale',channel)
            else:
                # TODO da vedere se si sposta o meno
                await self.vc.move_to(channel)
            print('Verificata la connessione')

            print('Poppato dalla lista'+self.music_queue.pop(0))
            #TODO vedere la lambda se funziona o meno e estudioia, vedere se è possibile non downloadare
            self.vc.play(discord.FFmpegPCMAudio(executable="C:/Ffmpeg/ffmpeg/bin/ffmpeg.exe",
                         source='./assets/songs/'+nomeSong+'.mp4'))
               # osservare il metodo play


            if self.vc.is_playing() is True: 
                print("Current Playing: "+nomeSong)
            else : 
                print("Non playa più la song: "+nomeSong)
            # mi contrtolla costantemente se una canzone è in playing
            
            # TODO devi cercare di capire in che modo far waitare e farlo funzionare bro
            

        

    @commands.command(name="play", help="Plays a selected song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)

        voiceChannel = ctx.author.voice.channel

        if voiceChannel is None:
            await ctx.send("Entra in un cazzo di canale fra!")
            return
        if self.vc.is_playing == False:
            song = self.search_yt(query)
            if type(song) is None:
                await ctx.send("Chicco mettime un link valido o ti pisto")
                return
            else:
                await ctx.send("Pompo un pochino di "+song)
                self.music_queue.append(song)

            if self.is_playing == False:
                    print('Canzone scaricata: entrato in play')
                    await self.play_music(voiceChannel)
        else :
            if self.vc.is_paused() is True :
                print("Resumo") 
                self.vc.resume()
            else : return
            
                
                    

    @commands.command(name="skip", help="skippa la canzone bro")
    async def skip(self):
        if self.vc != "" and self.vc:
            self.vc.stop()
            print("Stoppato e skippato")
            await self.play_music(self.vc.channel)

    @commands.command(name="stop", help="skippa la canzone bro")
    async def stop(self,ctx):
        if self.is_playing == True:
            print("Stoppa ziooo")
            self.vc.pause()

    

