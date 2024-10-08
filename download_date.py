import pandas as pd
from bs4 import BeautifulSoup
import requests
import time
import json
# Using beautifulsoup to scrape the EPS data from the website

def get_a_release_date(url,ticker):
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
                date_obj = cells[0].text

                Release_date.append(date_obj)
            
            except Exception as error:
                print(error)
                continue

    return Release_date


def get_all_release_dates():
    
    file_path = 'data/health_care_fundamental.xlsx'
    sheet_name = 'PE_FY1'
    tickers = load_tickers(file_path, sheet_name)
    count = 0
    dates = {}

    for ticker in tickers:
        try:
            url = "https://www.alphaquery.com/stock/"
            release_date = get_a_release_date(url,ticker)
            count += 1
            print(f"{ticker} has been processed, {count} out of {len(tickers)}")
            dates[ticker] = release_date
            time.sleep(1)
        except:
            pass
    
    output_path = "data/Earnings_dates.json"
    with open(output_path, "w") as f:
        json.dump(dates, f)


def load_tickers(file_location,sheet_name):
    df = pd.read_excel(file_location, sheet_name=sheet_name)
    columns = df.columns.drop('DATE').tolist()
    tickers = [item.split("-")[0] for item in columns]
    return tickers

if __name__ == "__main__":
    
    get_all_release_dates()


