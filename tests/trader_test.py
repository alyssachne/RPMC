import unittest
import pandas as pd
# trader_test.py

import sys
import os

# Add the root directory (one level up) to the system path to import trader.py
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from trader import Trader


class TestTrader(unittest.TestCase):

    def setUp(self):
        # Initial data setup for each test
        self.options = ['AAPL', 'AMAZ', 'GOOGL', 'MSFT', 'TSLA', 'EBAY', 'FB', 'TWTR', 'NFLX']
        self.stock_prices = {
            'AAPL': pd.DataFrame([150]),
            'AMAZ': pd.DataFrame([3200]),
            'GOOGL': pd.DataFrame([2800]),
            'MSFT': pd.DataFrame([300]),
            'TSLA': pd.DataFrame([800]),
            'EBAY': pd.DataFrame([65]),
            'FB': pd.DataFrame([340]),
            'TWTR': pd.DataFrame([45]),
            'NFLX': pd.DataFrame([600])
        }
        self.cash_level = 0.1
        self.total_assets = 100000  # Initial total assets
        self.trader = Trader(self.options, self.cash_level, self.total_assets, self.stock_prices)

    def test_initial_holding(self):
        # Test if holdings are initialized correctly
        self.assertEqual(len(self.trader.holdings), len(self.options))
        self.assertAlmostEqual(sum(self.trader.get_each_holding_value().values()), self.total_assets)
        # hold: AAPL: 67, AMAZ: 4, GOOGL: 4, MSFT: 34, TSLA: 13, EBAY: 154, FB: 30, TWTR: 223, NFLX: 17, cash: 4905
        self.assertEqual(self.trader.holdings['AAPL'], 67)
        self.assertEqual(self.trader.holdings['AMAZ'], 4)
        self.assertEqual(self.trader.holdings['GOOGL'], 4)
        self.assertEqual(self.trader.holdings['MSFT'], 34)
        self.assertEqual(self.trader.holdings['TSLA'], 13)
        self.assertEqual(self.trader.holdings['EBAY'], 154)
        self.assertEqual(self.trader.holdings['FB'], 30)
        self.assertEqual(self.trader.holdings['TWTR'], 223)
        self.assertEqual(self.trader.holdings['NFLX'], 17)
        self.assertEqual(self.trader.cash, 4905)

        # total value: AAPL: 10050, AMAZ: 12800, GOOGL: 11200, MSFT: 10200, TSLA: 10400, EBAY: 10010, FB: 10200, TWTR: 10035, NFLX: 10200, cash: 4905
        each_holding_value = self.trader.get_each_holding_value()
        self.assertEqual(each_holding_value['AAPL'], 10050)
        self.assertEqual(each_holding_value['AMAZ'], 12800)
        self.assertEqual(each_holding_value['GOOGL'], 11200)
        self.assertEqual(each_holding_value['MSFT'], 10200)
        self.assertEqual(each_holding_value['TSLA'], 10400)
        self.assertEqual(each_holding_value['EBAY'], 10010)
        self.assertEqual(each_holding_value['FB'], 10200)
        self.assertEqual(each_holding_value['TWTR'], 10035)
        self.assertEqual(each_holding_value['NFLX'], 10200)
        self.assertEqual(each_holding_value['cash'], 4905)


    def test_get_stock_price(self):
        # Test if stock price is correctly fetched
        self.assertEqual(self.trader.get_stock_price('AAPL'), 150)
        self.assertEqual(self.trader.get_stock_price('GOOGL'), 2800)

    def test_buy_stock(self):
        # Test stock buying behavior
        initial_cash = self.trader.cash.copy()
        self.trader.buy_stock('AAPL', 5)
        self.assertEqual(self.trader.holdings['AAPL'], 67 + 5)
        self.assertEqual(self.trader.cash, initial_cash - 5 * self.trader.get_stock_price('AAPL'))

    def test_sell_stock(self):
        # Test stock selling behavior
        initial_cash = self.trader.cash.copy()
        self.trader.sell_stock('AAPL', 5)
        self.assertEqual(self.trader.holdings['AAPL'], 62)
        self.assertEqual(self.trader.cash, initial_cash + 5 * self.trader.get_stock_price('AAPL'))


    def test_update_options(self):
        # Test updating stock options and removing non-existing ones
        new_options = ['FB', 'TWTR', 'NFLX', 'GOOGL']
        initial_transaction_count = self.trader.get_transaction_count()
        self.trader.update_options(new_options)
        self.assertEqual(set(self.trader.holdings.keys()), set(new_options))
        self.assertEqual(self.trader.get_transaction_count(), initial_transaction_count + 1)
        # shares: FB: 66, TWTR: 492, NFLX: 38, GOOGL: 9, cash: 7420
        self.assertEqual(self.trader.holdings['FB'], 66)
        self.assertEqual(self.trader.holdings['TWTR'], 492)
        self.assertEqual(self.trader.holdings['NFLX'], 38)
        self.assertEqual(self.trader.holdings['GOOGL'], 9)

        # total value: FB: 22440, TWTR: 22140, NFLX: 22800, GOOGL: 25200, cash: 7420
        each_holding_value = self.trader.get_each_holding_value()
        self.assertEqual(each_holding_value['FB'], 22440)
        self.assertEqual(each_holding_value['TWTR'], 22140)
        self.assertEqual(each_holding_value['NFLX'], 22800)
        self.assertEqual(each_holding_value['GOOGL'], 25200)
        self.assertEqual(each_holding_value['cash'], 7420)

    def test_update_options_with_price_change(self):
        new_prices = {
            'AAPL': pd.DataFrame([200]),
            'AMAZ': pd.DataFrame([3400]),
            'GOOGL': pd.DataFrame([3000]),
            'MSFT': pd.DataFrame([400]),
            'TSLA': pd.DataFrame([900]),
            'EBAY': pd.DataFrame([70]),
            'FB': pd.DataFrame([400]),
            'TWTR': pd.DataFrame([50]),
            'NFLX': pd.DataFrame([700])
        }
        self.trader.update_stock_prices(new_prices)
        options = ['AAPL', 'AMAZ', 'GOOGL', 'MSFT', 'TSLA', 'EBAY', 'FB', 'TWTR', 'NFLX']
        self.trader.update_options(options)
        


    def test_get_transaction_count(self):
        # Test transaction count increment on holdings update
        self.trader.update_options(self.options[:5])
        self.assertEqual(self.trader.get_transaction_count(), 2)  # 1 for init, 1 for update

if __name__ == '__main__':
    unittest.main()
