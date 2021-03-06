import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from webserver import keep_alive
from price import Price

keep_alive()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='cryptobot', help='Cryptobot introduction')
async def introduce(ctx):
    response = "Chuyên gia đọc lệnh, thần tỉa nến, thánh all in"
    await ctx.send(response)

@bot.command(name='price', help="Get a coin price. !price <symbol> <target currency-optional-default:VND>.\nEx: !price BTC, !price btc usd")
async def get_price(ctx, *args):
  if not args:
    response = "Vui lòng nhập ký hiệu đồng tiền và giá đích, !price <symbol> <target currency"
    await ctx.send(response)
  else:
    symbol = args[0].lower()
    if symbol.startswith("<@"):
      response = symbol + " là vô giá!"
      await ctx.send(response)
    else:
      target = args[1].lower() if len(args) >= 2 else "vnd"
      result = price.get_price(symbol, target)
      await ctx.send(result)
  
@bot.command(name="swap", help="Check cryptocurrencies exchange rate")
async def swap(ctx, src, dst, amount=1):
  if src.startswith("<@") or dst.startswith("<@"):
    response = src + " là vô giá!, không thể đổi" if src.startswith("<@") else dst + " là vô giá!, không thể đổi"
    await ctx.send(response)
  else:
    result = price.get_multiple_price(src.lower(), dst.lower())
    await ctx.send(result)

@bot.event
async def on_ready():
  activity = discord.Game(name="Visual Studio Code", type=4)
  await bot.change_presence(status=discord.Status.idle, activity=activity)

  print(f'{bot.user.name} has connected to Discord!')
  print(f'CryptoBot is ready!')

keep_alive()
price = Price()
bot.run(TOKEN)