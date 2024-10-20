import math
from loguru import logger
class Trader:
    def __init__(self, options: list, cash_level: float, total_assets: float, stock_price, num_holding: int =None):
        # for now assume options is sorted from highest to lowest
        # TODO: use dictionary to store options and their scores

        # stocks I can buy
        self.options = options
        self.cash_level = cash_level
        self.num_holding = num_holding if num_holding is not None else len(options)
        self.total_assets = total_assets
        self.cash = total_assets
        # TODO: for now assume stock price is 100, in the future need to update it
        self.stock_price = stock_price
        self.transaction_count = 1
        self.init_holding()

    def get_stock_price(self, stock):
        return self.stock_price[stock].values[0]
    
    def update_stock_prices(self, prices):
        self.stock_price = prices
        logger.info("INFO", f"Load all stock prices")
        self.total_assets = sum([self.holdings[option] * self.get_stock_price(option) for option in self.holdings.keys()]) + self.cash
        logger.info(f"Total assets: {self.total_assets}")

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
        shares = math.ceil(total_value / self.get_stock_price(stock))
        value = shares * self.get_stock_price(stock)
        if self.cash - value < 0:
            shares = math.floor(self.cash / self.get_stock_price(stock))
        return shares
        
    def init_holding(self):
        # 平均分配：计算平均分配金额
        each_holding_value = (1 - self.cash_level) * self.total_assets / self.num_holding
        self.holdings = {option: 0 for option in self.options[:self.num_holding]}
        for option in self.holdings.keys():
            self.buy_stock(option, self.get_stock_shares(option, each_holding_value))

    def buy_stock(self, stock, shares):
        self.holdings[stock] += shares
        self.cash -= shares * self.get_stock_price(stock)

    def sell_stock(self, stock, shares):
        self.holdings[stock] -= shares
        self.cash += shares * self.get_stock_price(stock)

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
        # 平均分配：计算平均分配金额
        each_holding_value = extra_cash / self.num_holding
        logger.info(f"Each holding value: {each_holding_value}")
        for option in self.holdings.keys():
            self.buy_stock(option, self.get_stock_shares(option, each_holding_value))

    def update_options(self, new_options):
        made_transaction = False
        old_holdings = self.holdings.copy()
        # stocks I should hold
        for ticker in new_options[:self.num_holding]:
            if ticker not in self.holdings.keys():
                self.holdings[ticker] = 0

        # remove stocks that are not in the new options
        for ticker in list(self.holdings.keys()):
            if ticker not in new_options:
                made_transaction = True
                self.transaction_count += 1
                self.sell_stock(ticker, self.holdings[ticker])
                self.holdings.pop(ticker)

        self.num_holding = len(self.holdings.keys())
        # check cash level
        if self.cash > self.total_assets * self.cash_level:
            self.update_holding()

        if not made_transaction:
            for holding, weight in self.holdings.items():
                if (holding not in old_holdings and weight != 0) or (holding in old_holdings and weight != old_holdings[holding]):
                    self.transaction_count += 1
                    logger.info(f"current count: {self.transaction_count}, old_holding: {old_holdings}, new_holding: {self.holdings}")
                    break

    def get_total_assets(self):
        return self.total_assets
    
    def get_each_holding_value(self):
        results = {}
        for option in self.holdings.keys():
            results[option] = self.holdings[option] * self.get_stock_price(option)
        results['cash'] = self.cash
        return results
    
    def get_holding_weights(self):
        results = {}
        for option in self.holdings.keys():
            results[option] = self.holdings[option]
        return results
    
    def get_transaction_count(self):
        return self.transaction_count

if __name__ == "__main__":
    options = ['AAPL', 'AMAZ', 'GOOGL', 'MSFT', 'TSLA', 'EBAY', 'FB', 'TWTR', 'NFLX']
    trader = Trader(options, 0.1, 3, 1000)
    print(trader.holdings)
    new_options = ['EBAY', 'FB', 'TWTR', 'NFLX', 'AAPL', 'AMAZ', 'GOOGL', 'MSFT', 'TSLA']
    print(trader.options)
    print(trader.holdings)
    trader.update_stock_prices('aapl', 10)
    print(trader.holdings)
    print(trader.cash)
    print(trader.total_assets)