import requests
import pandas as pd
from bs4 import BeautifulSoup

header = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
base_url = 'https://finviz.com/quote.ashx?t='

# Building generic index
generic_req = requests.get('https://finviz.com/quote.ashx?t=DIS',headers=header)
generic_soup = BeautifulSoup(generic_req.text,'html.parser')
index_list = [index.text for index in generic_soup.findAll('td',class_='snapshot-td2-cp')]

# Hard code duplicate key fix
index_list[20] = 'EPS growth this Y'
index_list[26] = 'EPS growth next Y '

# Fixing index list
fixed_index_list = []
i = 0
j = 0
z = 0
while j < int(len(index_list)):
    if i == 0:
        fixed_index_list.append(index_list[0])
        print(index_list[0])
        i += 6
        j += 1
    elif i < 72:
        fixed_index_list.append(index_list[i])
        print(index_list[i])
        i += 6
        j += 1
    else:
        z += 1
        i = z
        
# Beginning of Function

# Input validation
ticker = input('Enter your ticker symbol: ').upper()
while not ticker.isalpha() or len(ticker) > 4:
    ticker = input('Only strings less than five characters allowed. Try again! \nEnter your ticker symbol: ').upper()

url = base_url + ticker
request = requests.get(url,headers=header)

try:
    request.raise_for_status()
except:
    print('That ticker does not exist.')

# Scraping data
soup = BeautifulSoup(request.text,'html.parser')
data_row = [data.text for data in soup.findAll('td',class_='snapshot-td2')]


# Fixing data rows
fixed_data_row = []
i = 0
j = 0
z = 0
while j < int(len(index_list)):
    if i == 0:
        fixed_data_row.append(data_row[0])
        i += 6
        j += 1
    elif i < 72:
        fixed_data_row.append(data_row[i])
        i += 6
        j += 1
    else:
        z+=1
        i = z

# Building dict
data_dict = dict(zip(fixed_index_list,fixed_data_row))

#Temporary index (currently only taking one ticker at a time)
temp_column = [ticker]
# Building DataFrame
df = pd.DataFrame.from_dict(data_dict,orient = 'index',columns =temp_column)

# Test prints
#print(data_row)
#print(index_list)
#print(data_dict)