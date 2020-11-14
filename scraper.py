import requests
import pandas as pd
from bs4 import BeautifulSoup

df = None

def finviz_row_fixer(broken_list):
    # Fixing data in rows
    fixed_data_row = []
    i = 0
    j = 0
    z = 0
    while j < int(len(broken_list)):
        if i == 0:
            fixed_data_row.append(broken_list[0])
            i += 6
            j += 1
        elif i < 72:
            fixed_data_row.append(broken_list[i])
            i += 6
            j += 1
        else:
            z+=1
            i = z
    return fixed_data_row

def finviz_scraper(request,index_list):

    # Scraping data
    soup = BeautifulSoup(request.text,'html.parser')
    data_row = [data.text for data in soup.findAll('td',class_='snapshot-td2')]

    fixed_data_row = finviz_row_fixer(data_row)

    # Building dict
    data_dict = dict(zip(index_list,fixed_data_row))

    # Temporary column (currently only taking one ticker at a time)
    temp_column = ['ticker']
    # Building DataFrame
    global df
    df = pd.DataFrame.from_dict(data_dict,orient = 'index',columns =temp_column)
    
    df.to_csv()
        
    return df

def main():
    header = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}
    base_url = 'https://finviz.com/quote.ashx?t='

    # Building generic rows
    generic_req = requests.get('https://finviz.com/quote.ashx?t=DIS',headers=header)
    generic_soup = BeautifulSoup(generic_req.text,'html.parser')
    index_list = [index.text for index in generic_soup.findAll('td',class_='snapshot-td2-cp')]

    # Hard code duplicate key fix
    index_list[20] = 'EPS growth this Y'
    index_list[26] = 'EPS growth next Y '

    # Fixing index list
    fixed_index_list = finviz_row_fixer(index_list)

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
    
    print(finviz_scraper(request,fixed_index_list))

if __name__ == '__main__':
    main()

