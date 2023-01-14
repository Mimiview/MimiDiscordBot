import discord 
from music_cog import music_cog as music
from discord.ext import commands
from dotenv import load_dotenv
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='-', intents = intents)
  
bot.remove_command('help')
bot.load_extension('music_cog')
 
load_dotenv('.env')

@bot.event
async def on_ready():
    print("Bot is Running...")

bot.run(os.getenv('BOT_TOKEN'));