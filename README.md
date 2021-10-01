# MimiDiscordBot

This is a simple discord music bot that downloads the song thanks the yt-url of it.

# Requisites
* Python [3.6+](https://www.python.org/downloads/)
* ffmpeg [installed](https://ffmpeg.org/download.html) 

# Setup

* Install Python [3.6+](https://www.python.org/downloads/)

* Install [FFmpeg](https://ffmpeg.org/download.html)  

* Clone the repository: 

```
git clone https://github.com/Mimiview/MimiDiscordBot.git
```

* Define the following enviroment variable in file '.env':

  * BOT_TOKEN = insert here your *bot* toke
  * FFMPEG_PATH = you need to put here the ffmpeg download path 
  
* Make a virtualenv running this code and activate it
```
virtualenv venv
venv\Scripts|activate
```
* Install with `pip` command all the libraries we need for 
```
(venv) pip install discord
(venv) pip install youtube_dl
(venv) pip install python-dotenv
(venv) pip install pynacl
```
* Now enjoy your bot
```
(venv) .\bot.py
```
