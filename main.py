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

@bot.command(name='price', help="Get a coin price")
async def get_price(ctx, symbol: str):
  print(symbol)
  if symbol.startswith("<@"):
    response = symbol + " là vô giá!"
    await ctx.send(response)
  else:
    price = Price()
    usd = price.get_price(symbol)
    response = "1 " + symbol + " = " + usd + " USD"
    await ctx.send(response)

@bot.command(name="swap", help="Check cryptocurrencies exchange rate")
async def swap(ctx, src, dst, amount=1):
  if src.startswith("<@") or dst.startswith("<@"):
    response = src + " là vô giá!, không thể đổi" if src.startswith("<@") else dst + " là vô giá!, không thể đổi"
    await ctx.send(response)
  else:
    price = Price()
    src_price, dst_price = price.get_multiple_price(src, dst)
    if src_price is None:
      await ctx.send("Không có thông tin của đồng " + src)
    if dst_price is None:
      await ctx.send("Không có thông tin của đồng " + dst)
    src_price, dst_price = float(src_price), float(dst_price)
    amount = int(amount)
    diff = (src_price - dst_price) * amount
    response = str(amount) + " " + src + " = " + str(src_price/dst_price) + " " + dst + ". "
    if diff == 0:
      response += "Hòa vốn"
    elif diff > 0:
      response += "Lãi " + str(diff) + " USD"
    else:
      response += "Lỗ" + str(diff) + " USD"
    await ctx.send(response)

@bot.event
async def on_ready():
  activity = discord.Game(name="Visual Studio Code", type=4)
  await bot.change_presence(status=discord.Status.idle, activity=activity)

  print(f'{bot.user.name} has connected to Discord!')
  print(f'CryptoBot is ready!')

keep_alive()
bot.run(TOKEN)