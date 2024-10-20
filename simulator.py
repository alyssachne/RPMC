import datetime
from trader import Trader
import pandas as pd
import json
from loguru import logger
class Simulator:
    def __init__(self, ticker_path, price_path, cash_level: float, total_assets: int):
        self.cash_level = cash_level
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
        self.trader = Trader(options=first_options, cash_level=self.cash_level, total_assets=self.total_assets, stock_price=first_price)
        current_total_assets = self.trader.get_total_assets()
        current_distribution = self.trader.get_each_holding_value()
        logger.info(f"Current total assets: {current_total_assets}, \n Current distribution: {current_distribution}")

    def run(self):
        data = []
        for date in self.dates[1:]:
            options = self.tickers[date]
            self.today = date
            price = self.price_df[self.price_df['Date'] == date]
            self.trader.update_stock_prices(price)
            self.trader.update_options(options)
            current_total_assets = self.trader.get_total_assets()
            current_distribution = self.trader.get_each_holding_value()
            # Append data to the list
            data.append({
                "Date": date,
                "Total Assets": current_total_assets,
                "Distribution": current_distribution,
                "Weights": self.trader.get_holding_weights()
            })

        logger.info(f'Total transaction count is {self.trader.get_transaction_count()}')
    
        # Convert list of dictionaries to a DataFrame
        df = pd.DataFrame(data)

        # put the total transaction count in the last row
        df.loc[len(df.index)] = ['Total Transaction Count', self.trader.get_transaction_count(), '', '']
        
        # Write DataFrame to CSV file
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        df.to_csv(f'data/results/trader_results_{timestamp}_cash_level{str(self.cash_level)}.csv', index=False)

if __name__ == "__main__":
    simulator = Simulator('data/daily_tickers.json', 'data/price_df_all_tickers.csv', 0.1, 10000)
    simulator = Simulator('data/daily_tickers.json', 'data/price_df_all_tickers.csv', 0.05, 10000)
    simulator = Simulator('data/daily_tickers.json', 'data/price_df_all_tickers.csv', 0.001, 10000)