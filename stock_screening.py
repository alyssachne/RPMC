import pandas as pd
import numpy as np

from bs4 import BeautifulSoup
from datetime import datetime
import requests


"""**医药消费低估高增长策略**

股票池：沪深300+中证500成分股，且行业为医药生物、食品饮料。

选股条件：动态PE在30倍以下，营收同比大于0、净利润同比大于20%以上。

排序逻辑：按照ROA和市值综合排序，ROA越大排在越前面，市值越大排在越前面，且ROA和市值对排序影响的权重是1:1。

调仓逻辑：策略用轮动的方式进行买卖，每10日触发一次选股条件，符合条件，且在前3名的股票会继续持有，不符合条件，且掉出前3名股票就会卖掉。"""


file_location = '/Users/shuaijia/Desktop/找工/RPMC/health_care_fundamental.xlsx'
df_PE_FY1 = pd.read_excel(file_location, sheet_name='PE_FY1')
df_Sales = pd.read_excel(file_location, sheet_name='Sales')
df_NI = pd.read_excel(file_location, sheet_name='NI')
df_ROA = pd.read_excel(file_location, sheet_name='ROA')


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
