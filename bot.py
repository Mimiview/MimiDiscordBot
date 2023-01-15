import discord 
import asyncio
from music_cog import music_cog as music
from discord.ext import commands
from dotenv import load_dotenv
import os

intents = discord.Intents.all()


load_dotenv('.env')

async def main():
    bot = commands.Bot(command_prefix='-', intents = intents)
    bot.remove_command('help')
    async with bot:
        await bot.load_extension('music_cog')
        await bot.start(os.getenv('BOT_TOKEN'))
    @bot.event
    async def on_ready():
        print("Bot is Running...")



asyncio.run(main());