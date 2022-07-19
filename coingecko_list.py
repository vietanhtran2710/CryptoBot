from matplotlib.style import available
import requests

available_coin = []

response = requests.get('https://api.coingecko.com/api/v3/coins/list')
for item in response.json():
    available_coin.append(item["symbol"] + ";" + item["id"])

with open("coins_list.txt", "w") as f:
    f.write("\n".join(available_coin))