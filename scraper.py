import requests
import pandas as pd
from bs4 import BeautifulSoup


header = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
base_url = 'https://finviz.com/quote.ashx?t='

#Grab columns (all of them are uniform, simpler to grab first)
generic_req = requests.get('https://finviz.com/quote.ashx?t=DIS',headers=header)
generic_soup = BeautifulSoup(generic_req.text,'html.parser')
column_list = [column.text for column in generic_soup.findAll('td',class_='snapshot-td2-cp')]

#Input validation
ticker = input('Enter your ticker symbol: ').upper()
while not ticker.isalpha() or len(ticker) > 4:
    ticker = input('Only strings less than five characters allowed. Try again! \nEnter your ticker symbol: ').upper()

url = base_url + ticker
request = requests.get(url,headers=header)

try:
    request.raise_for_status()
except:
    print('That ticker does not exist.')

soup = BeautifulSoup(request.text,'html.parser')
data_row = [data.text for data in soup.findAll('td',class_='snapshot-td2') ]

# Test prints
print(data_row)
print(column_list)