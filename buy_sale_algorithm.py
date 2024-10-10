import math
from loguru import logger
class Trader:
    def __init__(self, options, cash_level, num_holding, total_assets, stock_price):
        # for now assume options is sorted from highest to lowest
        # TODO: use dictionary to store options and their scores
        self.options = options
        self.cash_level = cash_level
        self.num_holding = num_holding
        self.total_assets = total_assets
        self.cash = total_assets
        # TODO: for now assume stock price is 100, in the future need to update it
        self.stock_price = stock_price
        self.init_holding()

    def get_stock_price(self, stock):
        return self.stock_price[stock].values[0]
    
    def update_stock_prices(self, prices):
        self.stock_price = prices
        logger.info("INFO", f"Load all stock prices")
        self.total_assets = sum([self.holdings[option] * self.get_stock_price(option) for option in self.holdings.keys()]) + self.cash
        logger.info(f"Total assets: {self.total_assets}")
        self.check_cash_level()

    def update_single_stock_price(self, stock, price):
        # update the df
        self.stock_price[stock] = price
        logger.info("INFO", f"Stock price of {stock} is updated to {price}")
        self.total_assets = sum([self.holdings[option] * self.get_stock_price(option) for option in self.holdings.keys()]) + self.cash
        logger.info(f"Total assets: {self.total_assets}")
        self.check_cash_level()
    
    def get_stock_shares(self, stock, total_value):
        # round up if share is not integer 
        # -> cash level is guaranteed to be less than self.cash_level
        return math.ceil(total_value / self.get_stock_price(stock))

    def _update_cash(self):
        self.cash = self.total_assets - sum([self.holdings[option] * self.get_stock_price(option) for option in self.holdings.keys()])
        
    def init_holding(self):
        each_holding_value = (1 - self.cash_level) * self.total_assets / self.num_holding
        self.holdings = {option: self.get_stock_shares(option, each_holding_value) for option in self.options[:self.num_holding]}
        self._update_cash()

    def buy_stock(self, stock, shares):
        self.holdings[stock] += shares
        self.cash -= shares * self.get_stock_price(stock)
        self.check_cash_level()

    def sell_stock(self, stock, shares):
        self.holdings[stock] -= shares
        self.cash += shares * self.get_stock_price(stock)
        self.check_cash_level()

    def check_cash_level(self):
        # this number needs to be less than self.cash_level
        # if greater, buy more stocks
        if self.cash > self.total_assets * self.cash_level:
            logger.info("INFO", "Cash level is greater than the threshold, buying more stocks")
            self.update_holding()
        else:
            logger.info("INFO", "Cash level is less than the threshold, don't need to do anything")

    def update_holding(self):
        # buy more stocks for what we have
        extra_cash = self.cash - self.total_assets * self.cash_level
        logger.info(f"Extra cash beyond cash level: {extra_cash}")
        each_holding_value = extra_cash / self.num_holding
        logger.info(f"Each holding value: {each_holding_value}")
        for option in self.holdings.keys():
            self.holdings[option] += self.get_stock_shares(option, each_holding_value)
        self._update_cash()

    def update_options(self, new_options):
        self.options = new_options
        self.init_holding()

    def get_total_assets(self):
        return self.total_assets
    
    def get_each_holding_value(self):
        results = {}
        for option in self.holdings.keys():
            results[option] = self.holdings[option] * self.get_stock_price(option)
        results['cash'] = self.cash
        return results

if __name__ == "__main__":
    options = ['AAPL', 'AMAZ', 'GOOGL', 'MSFT', 'TSLA', 'EBAY', 'FB', 'TWTR', 'NFLX']
    trader = Trader(options, 0.1, 3, 1000)
    print(trader.holdings)
    new_options = ['EBAY', 'FB', 'TWTR', 'NFLX', 'AAPL', 'AMAZ', 'GOOGL', 'MSFT', 'TSLA']
    print(trader.options)
    print(trader.holdings)
    trader.update_stock_price('aapl', 10)
    print(trader.holdings)
    print(trader.cash)
    print(trader.total_assets)