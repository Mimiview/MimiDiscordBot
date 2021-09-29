import discord
import pafy
from discord.channel import VoiceChannel
from discord.ext import commands
import time
import youtube_dl
import os
from dotenv import load_dotenv

from youtube_dl import YoutubeDL
# Ricorda di installare PyNaCl

load_dotenv('.env')


class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False

        self.music_queue = []
        self.vc = ""  # voice channel

    def youtube_dl_search(self, query):
        ydl_opts = {'format': 'bestaudio/best',
                    # if they setn a playlist it would not consider it? #TODO study the behaviour
                    'noplaylist': True,
                    # location where ffmep is situated
                    'ffmpeg_location': os.getenv('FFMPEG_PATH'),
                    #'default_search' : 'auto', #TODO osservare come cercare senza url
                    'postprocessors': [{  # postprocess options
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': './assets/songs/%(title)s.%(ext)s'}  # output path deprecato da me, non esiste piu il download pappapero

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(query, download=False)
            return [meta.get('url', None), meta.get('title', None)] #ritornando una lista avreemo in posizione 0 l'url e in posizione 1 il titolo

    async def play_music(self, channel):
        print('Canzoni in coda: ', len(self.music_queue))
        if len(self.music_queue) > 0:
            self.is_playing = True

            # prendi l'url del primo
            song = self.music_queue[0]
            if self.vc == "" or not self.vc.is_connected() or self.vc == None:
                self.vc = await channel.connect()
                print('Entrato nel Canale', channel)
            else:
                # TODO da vedere se si sposta o meno
                await self.vc.move_to(channel)
            print('Verificata la connessione'+'\n')

            print('Poppato dalla lista'+self.music_queue.pop(0)[1]+'\n')
            self.vc.play(discord.FFmpegOpusAudio(
                song[0], executable=os.getenv('FFMPEG_PATH')))
            # da vedere che bug potrebbe portare
            print("Current Playing: " + song[1]+'\n')
            while self.vc.is_playing() is True:  # TODO trovare un modo come un event listener per quando smette di playare una canzone riparte con un'altra
                time.sleep(1)

            self.is_playing = False
            await self.play_music(channel)
        else:
            print("non ci sono canzoni in lista\n")

            # TODO devi cercare di capire in che modo far waitare e farlo funzionare bro

    @commands.command(name="play", help="Plays a selected song from youtube")
    async def play(self, ctx, *args):
        query = " ".join(args)

        try:
            voiceChannel = ctx.author.voice.channel
        except:
            await ctx.send("Entra in un cazzo di canale fra!")
            return

        try:
            song = self.youtube_dl_search(query)
        except:
            await ctx.send("Chicco mettime un link valido o ti pisto")
            return
        self.music_queue.append(song)
        print('Canzone scaricata: entrato in play')

        if self.is_playing == False:

            await ctx.send("Pompo un pochino di "+song[1])
            await self.play_music(voiceChannel)

        else:
            if self.vc.is_paused() is True:  # TODO problema del mettere in coda
                print("Resumo")
                self.vc.resume()
            else:  # TODO mettere in lista in caso positivo
                self.music_queue.append(song)
                await ctx.send("Canzone messa in cosa" + song[1])
                # skippa la song a quella successiva, nel mentrew handla il boolean isplaying

    @commands.command(name="skip", help="skippa la canzone bro")
    async def skip(self, ctx):
        if self.vc != "" and self.vc:
            self.vc.stop()
            self.is_playing = False
            await ctx.send("Canzone Skippata") #capire per quale motivo stampa due volte questo send
            print("Stoppato e skippato")
            await self.play_music(self.vc.channel)

    @commands.command(name="pause", help="mettinpausa")
    async def pause(self, ctx):
        if self.is_playing == True:
            await ctx.send("Canzone messa in pausa")
            print("Stoppa ziooo")
            self.vc.pause()
    # printa su discord la coda di canzoni

    @commands.command(name="queue", help="la lista delle song")
    async def queue(self, ctx):
        r = ' Coda in attesa: \n'
        for i in self.music_queue:
            r += i[1] + '\n'
        await ctx.send(r)
