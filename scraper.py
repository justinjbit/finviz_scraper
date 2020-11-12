import requests
from requests.exceptions import HTTPError
import pandas as pd
from bs4 import BeautifulSoup



header = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
base_url = 'https://finviz.com/quote.ashx?t='
ticker = input('Enter your ticker symbol: ').upper()

while not ticker.isalpha() or len(ticker) > 4:
    ticker = input('Only strings less than five characters allowed. Try again! \nEnter your ticker symbol: ').upper()

url = base_url + ticker
request = requests.get(url,headers=header)
try:
    request.raise_for_status()
except:
    print('That ticker does not exist. Try again!')