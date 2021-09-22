import discord 
from music_cog import music_cog as music
from discord.ext import commands
import pafy 
from dotenv import load_dotenv
import os

bot = commands.Bot(command_prefix='-')

  
bot.remove_command('help')

bot.add_cog(music(bot))
 
 
load_dotenv('.env')

bot.run(os.getenv('BOT_TOKEN'))

