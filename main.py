import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from webserver import keep_alive

keep_alive()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

bot = commands.Bot(command_prefix='!')

@bot.command(name='cryptobot', help='Cryptobot introduction')
async def introduce(ctx):
    response = "Chuyên gia đọc lệnh, thần tỉa nến, thánh all in"
    await ctx.send(response)

@bot.event
async def on_ready():
  activity = discord.Game(name="Visual Studio Code", type=4)
  await bot.change_presence(status=discord.Status.idle, activity=activity)

  print(f'{bot.user.name} has connected to Discord!')
  print(f'CryptoBot is ready!')

keep_alive()
bot.run(TOKEN)