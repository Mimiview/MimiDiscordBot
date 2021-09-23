import traceback
import youtube_dl
import time
import traceback
import sys

def youtube_dl_search():
    ydl_opts = {'format': 'bestaudio/best',
                'noplaylist': True,
                'ffmpeg_location' : 'C:/Ffmpeg/ffmpeg/bin/ffmpeg.exe',
                'postprocessors': [{  # TODO look up for the option documentation and also fot "ffprobe/avprobe and ffmpeg/avconv not found. Please install one."'s issue
                    'key': 'FFmpegExtractAudio',  
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': './assets/songs/%(title)s.%(ext)s'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(
            'https://www.youtube.com/watch?v=V2mnB2gYEMs&ab_channel=Rondodasosa', download=True)


try :
    youtube_dl_search()
except :
    traceback.print_exception(*sys.exc_info())
time.sleep(40)
