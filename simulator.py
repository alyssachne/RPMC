from buy_sale_algorithm import Trader
import pandas as pd
import json
from loguru import logger
class Simulator:
    def __init__(self, ticker_path, price_path, cash_level, num_holding, total_assets):
        self.cash_level = cash_level
        self.num_holding = num_holding
        self.total_assets = total_assets
        self.load_tickers(ticker_path)
        self.load_price(price_path)
        self.load_dates()
        self.today = self.dates[0]
        self.load_trader()
        self.run()

    def load_price(self, file_location):
        self.price_df = pd.read_csv(file_location)
        # convert date to yyyy-mm-dd format
        self.price_df['Date'] = pd.to_datetime(self.price_df['Date'], utc=True).dt.strftime('%Y-%m-%d')

    def load_tickers(self, file_location):
        with open(file_location) as f:
            self.tickers = json.load(f)

    def load_dates(self):
        dates1 = self.price_df['Date']
        dates2 = self.tickers.keys()
        # find intersection of dates1 and dates2
        self.dates = list(set(dates1) & set(dates2))
        self.dates = sorted(self.dates)

    def load_trader(self):
        first_options = self.tickers[self.today]
        first_price = self.price_df[self.price_df['Date'] == self.today]
        self.trader = Trader(first_options, self.cash_level, self.num_holding, self.total_assets, first_price)
        current_total_assets = self.trader.get_total_assets()
        current_distribution = self.trader.get_each_holding_value()
        logger.info(f"Current total assets: {current_total_assets}, \n Current distribution: {current_distribution}")

    def run(self):
        for date in self.dates[1:]:
            # options = self.tickers[date]
            self.today = date
            price = self.price_df[self.price_df['Date'] == date]
            self.trader.update_stock_prices(price)
            current_total_assets = self.trader.get_total_assets()
            current_distribution = self.trader.get_each_holding_value()
            logger.info(f"At {date}, Current total assets: {current_total_assets}, \n Current distribution: {current_distribution}")
if __name__ == "__main__":
    simulator = Simulator('data/daily_tickers.json', 'data/price_df_all_tickers.csv', 0.1, 3, 10000)