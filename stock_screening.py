import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
from datetime import datetime
import requests

file_location = '/Users/shuaijia/Desktop/找工/RPMC/health_care_fundamental.xlsx'
df_PE_FY1 = pd.read_excel(file_location, sheet_name='PE_FY1')
df_Sales = pd.read_excel(file_location, sheet_name='Sales')
df_PS = pd.read_excel(file_location, sheet_name='PS')
df_EPS = pd.read_excel(file_location, sheet_name='EPS')
df_NI = pd.read_excel(file_location, sheet_name='NI')
df_ROA = pd.read_excel(file_location, sheet_name='ROA')
df_Assets = pd.read_excel(file_location, sheet_name='Assets')
df_PB = pd.read_excel(file_location, sheet_name='PB')
df_PE = pd.read_excel(file_location, sheet_name='PE')

# Using beautifulsoup to scrape the EPS data from the website

def get_EPS(url,ticker):
    EPS = []
    Release_date = []
    response = requests.get(url+ticker+"/earnings-history")
    #https://www.marketbeat.com/stocks/NYSE/LLY/earnings/
    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        Earn_tbl = soup.find_all('table')[-1]

        Earn_rows = Earn_tbl.find_all("tr")

        for row in Earn_rows:
            try:
                cells = row.find_all('td')

                # Convert to datetime object
                date_obj = datetime.strptime(cells[0].text, '%Y-%m-%d')

                Release_date.append(date_obj)
            
            except Exception as error:
                print(error)
                continue

    return Release_date

tickers = ['LLY']
count = 0

for ticker in tickers:
    count += 1
    print(f"{ticker} has been processed, {count} out of {len(tickers)}")
    try:
        url = "https://www.alphaquery.com/stock/"
        Release_date = get_EPS(url,ticker)
    except:
        pass

print(Release_date)
print(len(Release_date))

import yfinance as yf
import pandas as pd

# Define the ticker symbol (replace with the actual stock ticker)
ticker = 'LLY'  # Example: Apple

# Get the stock object
#stock = yf.Ticker(ticker)

# Fetch past earnings release dates
#earnings = stock.earnings_dates
