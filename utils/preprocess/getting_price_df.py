from utils.preprocess.get_yfinance import api_n_year_data
import pandas as pd

def load_tickers(file_location,sheet_name):
    df = pd.read_excel(file_location, sheet_name=sheet_name)
    columns = df.columns.drop('DATE').tolist()
    tickers = [item.split("-")[0] for item in columns]
    return tickers

file_path = '/Users/shuaijia/Desktop/找工/RPMC/RPMC/health_care_fundamental.xlsx'
sheet_name = 'PE_FY1'
tickers = load_tickers(file_path, sheet_name)

counter = 0
price_df_all_tickers = pd.DataFrame()

for ticker in tickers:
    price = api_n_year_data(ticker, 11).get_price()
    dates = api_n_year_data(ticker, 11).get_dates()
    if len(dates) == len(price):
        price_df = pd.concat([dates, price], axis=1)
        price_df = price_df.rename(columns = {'Close': ticker})
    else:
        raise ValueError("Dates and prices are not the same length")
    if counter !=0:
        price_df_all_tickers = pd.merge(price_df_all_tickers, price_df, on='Date', how='outer')
    else:
        price_df_all_tickers = price_df
    counter += 1
    print(f"{counter} out of {len(tickers)} tickers loaded")   
    price_df_all_tickers.to_csv('/Users/shuaijia/Desktop/找工/RPMC/RPMC/price_df_all_tickers.csv', index=False)