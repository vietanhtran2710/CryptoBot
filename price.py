import requests
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os
from dotenv import load_dotenv

class Price(object):
  def __init__(self):
    load_dotenv()
    self.url = 'https://api.coingecko.com/api/v3/'
    self.symbol_to_id = {}
    self.currencies = [
      "btc","eth","ltc","bch","bnb","eos","xrp","xlm","link","dot",
      "yfi","usd","aed","ars","aud","bdt","bhd","bmd","brl","cad",
      "chf","clp","cny", "czk","dkk","eur","gbp","hkd","huf","idr",
      "ils","inr","jpy","krw","kwd","lkr","mmk","mxn","myr","ngn",
      "nok","nzd","php","pkr","pln","rub","sar","sek","sgd","thb",
      "try","twd","uah","vef","vnd","zar","xdr","xag","xau","bits","sats"
    ]
    with open("coins_list.txt", "r") as f:
      data = f.readlines()
      for item in data:
        symbol, id = item.strip().split(";")
        self.symbol_to_id[symbol] = id

  def get_price(self, symbol, target):
    if symbol.lower() not in self.symbol_to_id.keys():
      return "Đồng" + symbol + "không có trong dữ liệu"
    if target not in self.currencies:
      return "Đồng" + target + "không có trong dữ liệu"
    try:
      id = self.symbol_to_id[symbol]
      response = requests.get(self.url + 'simple/price?ids=' + id + '&vs_currencies=' + target)
      if response.status_code != 200:
        return "Đã có lỗi xảy ra, xin vui lòng thử lại sau, code: " + str(response.status_code)
      price = response.json()[id][target]
      return "1 " + symbol.upper() + " = " + f"{price:,}" + " " + target.upper()
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      return "Đã có lỗi xảy ra, xin vui lòng thử lại sau, " + e

  def get_multiple_price(self, src, dst):
    if src not in self.symbol_to_id.keys():
      return "Đồng" + src.upper() + "không có trong dữ liệu"
    if dst not in self.symbol_to_id.keys():
      return "Đồng" + dst.upper() + "không có trong dữ liệu"
    try:
      src_id = self.symbol_to_id[src]
      response = requests.get(self.url + 'simple/price?ids=' + src_id + '&vs_currencies=usd')
      if response.status_code != 200:
        return "Đã có lỗi xảy ra, xin vui lòng thử lại sau, code: " + str(response.status_code)
      src_price = response.json()[src_id]["usd"]
      dst_id = self.symbol_to_id[dst]
      response = requests.get(self.url + 'simple/price?ids=' + dst_id + '&vs_currencies=usd')
      if response.status_code != 200:
        return "Đã có lỗi xảy ra, xin vui lòng thử lại sau, code: " + str(response.status_code)
      dst_price = response.json()[dst_id]["usd"]
      ratio = src_price / dst_price
      return "1 " + src.upper() + " = " + str(ratio) + " " + dst.upper()
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      return "Đã có lỗi xảy ra, xin vui lòng thử lại sau, " + e