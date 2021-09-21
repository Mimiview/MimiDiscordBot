import discord 
from music_cog import music_cog as music
from discord.ext import commands
import pafy 

bot = commands.Bot(command_prefix='-')

  
bot.remove_command('help')

bot.add_cog(music(bot))



bot.run('ODgyNzE0NTQ4MTgyODU5ODU4.YS_Z_A.X_HPPBVo9SFPA4OFhUzWMphHH5g')

