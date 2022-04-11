import discord
from discord.channel import VoiceChannel
from discord.ext import commands
import youtube_dl
import os
from dotenv import load_dotenv
from youtube_dl import YoutubeDL
# Ricorda di installare PyNaCl

load_dotenv('.env')

# TODO fixare il fatto che se disconnetto il bot di proposito, me lo da come connesso ancora studiare comportamento


class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False

        self.music_queue = []
        self.vc = ""  # voice channel

    def youtube_dl_search(self, query):
        ydl_opts = {'format': 'bestaudio',
                    # if they setn a playlist it would not consider it? #TODO study the behaviour
                    'noplaylist': True,
                    # location where ffmep is situated
                    'ffmpeg_location': os.getenv('FFMPEG_PATH'),
                    'default_search': 'ytsearch',  # TODO osservare come cercare senza url
                    'postprocessors': [{  # postprocess options
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]}

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            meta = ydl.extract_info(query, download=False)
            # ritornando una lista avreemo in posizione 0 l'url e in posizione 1 il titolo

            # dictionary con 3 layers
            return [meta['entries'][0]['url'], meta['entries'][0]['title']]

    def play_next(self):
        print('Canzoni in coda: ', len(self.music_queue))
        if len(self.music_queue) > 0:
            self.is_playing = True
            song = self.music_queue.pop(0)
            self.vc.play(discord.FFmpegOpusAudio(
                song[0], executable=os.getenv('FFMPEG_PATH')), after=lambda e: self.play_next())
            # da vedere che bug potrebbe portare
            print("Current Playing: " + song[1]+'\n')
        else:
            self.is_playing = False

    async def bot_voice_channel_connector(self, channel):
        if self.vc == "" or not self.vc.is_connected() or self.vc == None or not self:
            self.vc = await channel.connect()
            print('Entrato nel Canale', channel)
        else:
            print("Move to channel")
            await self.vc.move_to(channel)

    async def play_music(self, channel):
        print('Canzoni in coda: ', len(self.music_queue))
        if len(self.music_queue) > 0:
            self.is_playing = True

            await self.bot_voice_channel_connector(channel)
            # prendi l'url del primo
            song = self.music_queue.pop(0)
            print('Poppato dalla lista'+song[1]+'\n')

            print('Verificata la connessione'+'\n')

            self.vc.play(discord.FFmpegOpusAudio(
                song[0], executable=os.getenv('FFMPEG_PATH')), after=lambda e: self.play_next())  # TODO se vai troppo fast devi vedere in che modo sloware la richiesta

            print("Current Playing: " + song[1]+'\n')

        else:
            self.is_playing = False
            print("non ci sono canzoni in lista\n")

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
        print('Canzone scaricata: entrato in play')  # need to

        if self.is_playing == False:
            await ctx.send("Pompo un pochino di "+song[1]+'\n')
            await self.play_music(voiceChannel)
        else:
            print("Canzone accodata "+song[1]+'\n')
            await ctx.send("Canzone messa in coda " + song[1])
            # skippa la song a quella successiva, nel mentrew handla il boolean isplaying

    @commands.command(name="sqhipe", help="skippa la canzone bro")
    async def sqhipe(self, ctx):
        if self.vc != "" and self.vc:
            try:
                voiceChannel = ctx.author.voice.channel
            except:
                await ctx.send("Entra in un cazzo di canale fra!")
                return
            await self.bot_voice_channel_connector(voiceChannel)
            self.vc.stop()
            await ctx.send("Canzone Skippata")
            print("Stoppato e skippato")
            self.play_next()  # TODO vedere perchè da clientException, capire perchè skippa due volte

    @commands.command(name="stop", help="mettinpausa")
    async def stop(self, ctx):  # Lo stop mette semplicemente in pausa
        if self.is_playing == True:
            await ctx.send("Canzone messa in pausa")
            print("Stoppa ziooo")
            self.vc.pause()
    # printa su discord la coda di canzoni

    @commands.command(name="queue", help="la lista delle song")
    async def queue(self, ctx):
        print("Lista stampata"+'\n')
        r = ' Playlist: \n'
        for i in self.music_queue:
            r += '  - ' + i[1] + '\n'
        await ctx.send(r)

    @commands.command(name="resume", help="rimette in play una canzone")
    async def resume(self, ctx):
        try:
                voiceChannel = ctx.author.voice.channel
        except:
                await ctx.send("Entra in un cazzo di canale fra!")
                return
        await self.bot_voice_channel_connector(voiceChannel)
        if self.is_playing and self.vc.is_paused():  # TODO la seconda è inutile, vedere come far a vedere
            print("Resumo")
            self.vc.resume()
