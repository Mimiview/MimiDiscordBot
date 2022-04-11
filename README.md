# MimiDiscordBot

This is a simple discord music bot that downloads the song using discrord messages.

## Requisites
* Python [3.6+](https://www.python.org/downloads/)
* ffmpeg [installed](https://ffmpeg.org/download.html)
* Discord [Bot](https://discord.com/developers/applications)

## Setup

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
venv\Scripts\activate
```
* Install with `pip` command all the libraries we need for 
```
(venv) pip install discord youtube_dl python-dotenv pynacl

```
* Now enjoy your bot
```
(venv) .\bot.py
```

## Usage 

After you get into your discord [application](https://discord.com/developers/applications), go on the OAuth2 section, scrool down and tick the bot *scope*, add the permission of voice texting and whatever you want, paste the link shown and get your bot into your server.

When you'll run the bot you can use all the commands down below: 
* `-play [url] : You must give a Youtube *url* to that`
* `-queue : It shows you the song queue`
* `-skip : Skip the song`
* `-stop : Pause the song`
* `-resume : It resumes the song`
