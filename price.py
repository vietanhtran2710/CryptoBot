from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import os
from dotenv import load_dotenv


class Price(object):
  def __init__(self):
    load_dotenv()
    self.url = 'https://api.nomics.com/v1/prices?key=' + os.getenv("API_KEY")
    self.session = Session()

  def get_price(self, symbol):
    try:
      response = self.session.get(self.url)
      data = json.loads(response.text)
      for item in data:
        if item['currency'] == symbol:
          return item['price']
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)

  def get_multiple_price(self, src, dst):
    try:
      response = self.session.get(self.url)
      data = json.loads(response.text)
      src_price, dst_price = None, None
      for item in data:
        if item['currency'] == src:
          src_price = item['price']
        if item['currency'] == dst:
          dst_price = item['price']
      return src_price, dst_price
    except (ConnectionError, Timeout, TooManyRedirects) as e:
      print(e)