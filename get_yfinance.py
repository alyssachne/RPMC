import pandas as pd
import yfinance as yf

class api_n_year_data:

    def __init__(self, ticker, nyears):
        self.stock = yf.Ticker(ticker)
        self.end_date = pd.Timestamp.now()
        self.start_date = self.end_date - pd.DateOffset(years=nyears)

    def get_dates(self):
        # Get the stock object
        stock = self.stock

        # Fetch historical price data for the past n years
        data = stock.history(start=self.start_date.strftime('%Y-%m-%d'), end=self.end_date.strftime('%Y-%m-%d'))

        #Reset the date as the new column
        data = data.reset_index()

        # Extract the 'Adj Close' column which contains the adjusted closing prices
        dates = data[['Date']]

        return dates
    
    def get_price(self):
        # Get the stock object
        stock = self.stock

        # Fetch historical price data for the past n years
        data = stock.history(start=self.start_date.strftime('%Y-%m-%d'), end=self.end_date.strftime('%Y-%m-%d'))

        #Reset the date as the new column
        data = data.reset_index()

        # Extract the 'Adj Close' column which contains the adjusted closing prices
        price = data[['Close']]

        return price
        



if __name__ == "__main__":
    AAPL = api_n_year_data('AAPL',10)
    price = AAPL.get_price()
    print(price)