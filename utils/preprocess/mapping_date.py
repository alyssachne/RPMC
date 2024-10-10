# Map the release date to quarterly fundamental data  
import pandas as pd
from utils.preprocess.get_yfinance import api_n_year_data
import json

def read_fundamental_sheet(indicator):
    
    file_path = 'data/health_care_fundamental.xlsx'

    df = pd.read_excel(file_path, sheet_name=indicator)

    return df

def read_earnings_dates():
    file_path = 'data/Earnings_dates.json'
    
    with open(file_path, 'r') as f:
        earnings_dates = json.load(f)
    
    return earnings_dates

def load_tickers(file_location,sheet_name):
    df = pd.read_excel(file_location, sheet_name=sheet_name)
    columns = df.columns.drop('DATE').tolist()
    tickers = [item.split("-")[0] for item in columns]
    return tickers

class preprocess_indicator:
    def __init__(self, ticker):
        self.ticker = ticker 

    def calculate_ni_ratio(self):
        stock = api_n_year_data(self.ticker,11)
        y_finance_dates =  stock.get_dates()
        y_finance_dates['Date'] = pd.to_datetime(y_finance_dates['Date'])

        earnings_dates = read_earnings_dates()
        earnings_dates_ticker = earnings_dates[self.ticker]

        df_ni = read_fundamental_sheet('NI')
        df_ni_ticker = df_ni[[self.ticker + '-US']]
        df_ni_ticker = df_ni_ticker.rename(columns={self.ticker + '-US': 'NI'})
        ni_lst = df_ni_ticker['NI'].tolist()
        ni_lst_reversed = ni_lst[::-1]
        
        seen = set()
        unique_lst = []
        #ni value from the most recent to 40 quarters ago (10 years)
        for ni in ni_lst_reversed:
            if ni not in seen:
                unique_lst.append(ni)
                seen.add(ni)

        ni_ratio= []

        for i in range(len(unique_lst)-4):
            ratio = (unique_lst[i] - unique_lst[i+4])/unique_lst[i+4]
            ni_ratio.append(ratio)

        ni_dict = {}

        # Combine it with the earnings date 
        for i in range(len(earnings_dates_ticker)):
            try:
                ni_dict[earnings_dates_ticker[i]] = ni_ratio[i]
            except:
                pass

        #Map it to yfinance dates(every trading date)
        df_ni = pd.DataFrame(ni_dict.items(), columns=['Date', 'NI'])
        df_ni['Date'] = pd.to_datetime(df_ni['Date'])
        # Remove timezone information (if any) to make them tz-naive
        df_ni['Date'] = df_ni['Date'].dt.tz_localize(None)
        y_finance_dates['Date'] = y_finance_dates['Date'].dt.tz_localize(None)
        

        # Sort both DataFrames by Date
        df_ni = df_ni.sort_values(by='Date')
        # Save df_ni as CSV
        #df_ni.to_csv('/Users/shuaijia/Desktop/找工/RPMC/RPMC/df_ni.csv', index=False)
        y_finance_dates = y_finance_dates.sort_values(by='Date')

        # We need to define the next NI date for each NI period
        df_ni['next_NI_date'] = df_ni['Date'].shift(-1)

        # Find the last date in y_finance_dates
        last_date = y_finance_dates['Date'].iloc[-1]

        # Set the next_roa_date for the last row in df_roa as the last date
        df_ni.loc[df_ni.index[-1], 'next_NI_date'] = last_date

        # Now, map each date in y_finance_dates to its corresponding NI value
        def map_NI(row, df_ni):

            # Convert row['Date'] to a pandas Timestamp for comparison
            row_date = pd.Timestamp(row['Date'])
            # Filter to find the appropriate NI range (current <= Date < next)
            current_NI = df_ni[(df_ni['Date'] < row_date) & (row_date <= df_ni['next_NI_date'])]
            if not current_NI.empty:
                return current_NI['NI'].values[0]
            return None  # If no NI is found, return None

        # Apply the mapping function to each row in y_finance_dates
        y_finance_dates['NI'] = y_finance_dates.apply(map_NI, axis=1, df_ni=df_ni)

        y_finance_dates = y_finance_dates.dropna(subset = ['NI'])

        return y_finance_dates

    def calculate_sales_ratio(self):
        stock = api_n_year_data(self.ticker,11)
        y_finance_dates =  stock.get_dates()
        y_finance_dates['Date'] = pd.to_datetime(y_finance_dates['Date'])

        earnings_dates = read_earnings_dates()
        earnings_dates_ticker = earnings_dates[self.ticker]

        df_sales = read_fundamental_sheet('Sales')
        df_sales_ticker = df_sales[[self.ticker + '-US']]
        df_sales_ticker = df_sales_ticker.rename(columns={self.ticker + '-US': 'sales'})
        sales_lst = df_sales_ticker['sales'].tolist()
        sales_lst_reversed = sales_lst[::-1]
        
        seen = set()
        unique_lst = []
        #sales value from the most recent to 40 quarters ago (10 years)
        for sales in sales_lst_reversed:
            if sales not in seen:
                unique_lst.append(sales)
                seen.add(sales)

        sales_ratio= []

        for i in range(len(unique_lst)-4):
            ratio = (unique_lst[i] - unique_lst[i+4])/unique_lst[i+4]
            sales_ratio.append(ratio)

        sales_dict = {}

        # Combine it with the earnings date 
        for i in range(len(earnings_dates_ticker)):
            try:
                sales_dict[earnings_dates_ticker[i]] = sales_ratio[i]
            except:
                pass

        #Map it to yfinance dates(every trading date)
        df_sales = pd.DataFrame(sales_dict.items(), columns=['Date', 'sales'])
        df_sales['Date'] = pd.to_datetime(df_sales['Date'])
        # Remove timezone information (if any) to make them tz-naive
        df_sales['Date'] = df_sales['Date'].dt.tz_localize(None)
        y_finance_dates['Date'] = y_finance_dates['Date'].dt.tz_localize(None)
        

        # Sort both DataFrames by Date
        df_sales = df_sales.sort_values(by='Date')
        #df_sales.to_csv('/Users/shuaijia/Desktop/找工/RPMC/RPMC/df_sales.csv', index=False)
        y_finance_dates = y_finance_dates.sort_values(by='Date')

        # We need to define the next sales date for each sales period
        df_sales['next_sales_date'] = df_sales['Date'].shift(-1)

        # Find the last date in y_finance_dates
        last_date = y_finance_dates['Date'].iloc[-1]

        # Set the next_roa_date for the last row in df_roa as the last date
        df_sales.loc[df_sales.index[-1], 'next_sales_date'] = last_date

        # Now, map each date in y_finance_dates to its corresponding sales value
        def map_sales(row, df_sales):

            # Convert row['Date'] to a pandas Timestamp for comparison
            row_date = pd.Timestamp(row['Date'])
            # Filter to find the appropriate sales range (current <= Date < next)
            current_sales = df_sales[(df_sales['Date'] < row_date) & (row_date <= df_sales['next_sales_date'])]
            if not current_sales.empty:
                return current_sales['sales'].values[0]
            return None  # If no sales is found, return None

        # Apply the mapping function to each row in y_finance_dates
        y_finance_dates['sales'] = y_finance_dates.apply(map_sales, axis=1, df_sales=df_sales)

        y_finance_dates = y_finance_dates.dropna(subset = ['sales'])

        return y_finance_dates

    def map_ROA(self):
        stock = api_n_year_data(self.ticker,11)
        y_finance_dates =  stock.get_dates()
        y_finance_dates['Date'] = pd.to_datetime(y_finance_dates['Date'])

        earnings_dates = read_earnings_dates()
        earnings_dates_ticker = earnings_dates[self.ticker]

    #dict {date: roa}
        df_ROA = read_fundamental_sheet('ROA')
        df_ROA_ticker = df_ROA[[self.ticker + '-US']]
        df_ROA_ticker = df_ROA_ticker.rename(columns={self.ticker + '-US': 'ROA'})
        roa_lst = df_ROA_ticker['ROA'].tolist()

    
        roa_dict = {}

        # prev = None
        # counter = 0
        # for roa in reversed(roa_lst):
        #     try:
        #         if prev is None or prev != roa:
        #             roa_dict[earnings_dates_ticker[counter]] = roa
        #             counter += 1
        #             prev = roa
        #     except:
        #         pass
        roa_lst_reversed = roa_lst[::-1]
        counter = 0
        prev = None
        for i in range(len(earnings_dates_ticker)):
            
            curr = roa_lst_reversed[counter]
            if prev is not None:
                while curr == prev:
                    # Move one down if the same
                    counter += 1
                    prev = curr
                    curr = roa_lst_reversed[counter]
                roa_dict[earnings_dates_ticker[i]] = curr
            else:
                roa_dict[earnings_dates_ticker[i]] = curr
            # Move one down if different
            prev = curr
            counter += 1
        
        df_roa = pd.DataFrame(roa_dict.items(), columns=['Date', 'ROA'])
        df_roa['Date'] = pd.to_datetime(df_roa['Date'])
        # Remove timezone information (if any) to make them tz-naive
        df_roa['Date'] = df_roa['Date'].dt.tz_localize(None)
        y_finance_dates['Date'] = y_finance_dates['Date'].dt.tz_localize(None)
        

        # Sort both DataFrames by Date
        df_roa = df_roa.sort_values(by='Date')
        #df_roa.to_csv('/Users/shuaijia/Desktop/找工/RPMC/RPMC/df_roa.csv', index=False)
        y_finance_dates = y_finance_dates.sort_values(by='Date')

        # We need to define the next ROA date for each ROA period
        df_roa['next_roa_date'] = df_roa['Date'].shift(-1)
        # Find the last date in y_finance_dates
        last_date = y_finance_dates['Date'].iloc[-1]

        # Set the next_roa_date for the last row in df_roa as the last date
        df_roa.loc[df_roa.index[-1], 'next_roa_date'] = last_date

        # Now, map each date in y_finance_dates to its corresponding ROA value
        def map_roa(row, df_roa):

            # Convert row['Date'] to a pandas Timestamp for comparison
            row_date = pd.Timestamp(row['Date'])
            # Filter to find the appropriate ROA range (current < Date <= next)
            current_roa = df_roa[(df_roa['Date'] < row_date) & (row_date <= df_roa['next_roa_date'])]
            if not current_roa.empty:
                return current_roa['ROA'].values[0]
            return None  # If no ROA is found, return None

        # Apply the mapping function to each row in y_finance_dates
        y_finance_dates['ROA'] = y_finance_dates.apply(map_roa, axis=1, df_roa=df_roa)

        y_finance_dates = y_finance_dates.dropna(subset = ['ROA'])

        return y_finance_dates

    def map_PE_FY1(self):
        stock = api_n_year_data(self.ticker,11)
        y_finance_dates =  stock.get_dates()
        y_finance_dates['Date'] = pd.to_datetime(y_finance_dates['Date'])
        y_finance_dates['month'] = y_finance_dates['Date'].dt.to_period('M')
        y_finance_dates['Date'] = y_finance_dates['Date'].dt.tz_localize(None)
        
        df_PE = read_fundamental_sheet('PE_FY1')
        df_PE_ticker = df_PE[['DATE', self.ticker + '-US']]
        df_PE_ticker = df_PE_ticker.rename(columns={'DATE': 'month', self.ticker + '-US': 'PE_FY1'})
        df_PE_ticker['month'] = pd.to_datetime(df_PE_ticker['month'], format='%m/%y')
        df_PE_ticker['month'] = df_PE_ticker['month'].dt.to_period('M')
        
        df_merged = pd.merge(y_finance_dates, df_PE_ticker, on='month', how = 'left')
        df_merged = df_merged.dropna(subset=['PE_FY1'])
        df_merged = df_merged.drop(columns = 'month')

        return df_merged



if __name__ == "__main__":
    
    file_path = 'data/health_care_fundamental.xlsx'
    sheet_name = 'PE_FY1'
    tickers = load_tickers(file_path, sheet_name)

    ticker_lst = tickers
    ticker_lst = [ticker for ticker in ticker_lst if ticker not in ['DXCM','GEHC','INCY','MRNA','PODD','SOLV']]

    
    #ticker_lst.append(tickers[57])

    count = 0
    #all_tickers_df = pd.DataFrame()
    ni_ratio_merged = pd.DataFrame()
    sales_ratio_merged = pd.DataFrame()
    ROA_merged = pd.DataFrame()
    PE_FY1_merged = pd.DataFrame()

    for ticker in ticker_lst:
        stock_indicator = preprocess_indicator(ticker)
        ni_ratio_ticker = stock_indicator.calculate_ni_ratio()
        sales_ratio_ticker = stock_indicator.calculate_sales_ratio()
        ROA_ticker = stock_indicator.map_ROA()
        PE_FY1_ticker = stock_indicator.map_PE_FY1()

        
        ni_ratio_ticker = ni_ratio_ticker.rename(columns={'NI': f'{ticker}'})
        sales_ratio_ticker = sales_ratio_ticker.rename(columns={'sales': f'{ticker}'})
        ROA_ticker = ROA_ticker.rename(columns={'ROA': f'{ticker}'})
        PE_FY1_ticker = PE_FY1_ticker.rename(columns={'PE_FY1': f'{ticker}'})
        #merged_df.to_csv(f'/Users/shuaijia/Desktop/找工/RPMC/RPMC/{ticker}_data.csv', index=False)
        
        if count != 0:
            ni_ratio_merged = pd.merge(ni_ratio_merged, ni_ratio_ticker , on = 'Date', how = 'outer')
            sales_ratio_merged = pd.merge(sales_ratio_merged, sales_ratio_ticker , on = 'Date', how = 'outer')
            ROA_merged = pd.merge(ROA_merged, ROA_ticker , on = 'Date', how = 'outer')
            PE_FY1_merged = pd.merge(PE_FY1_merged, PE_FY1_ticker , on = 'Date', how = 'outer')
        else:
            ni_ratio_merged = ni_ratio_ticker
            sales_ratio_merged = sales_ratio_ticker
            ROA_merged = ROA_ticker
            PE_FY1_merged = PE_FY1_ticker
        count += 1

        print(f'{count} out of {len(ticker_lst)} has been merged')

    # Save merged_df as CSV
    ni_ratio_merged.to_csv('/Users/shuaijia/Desktop/找工/RPMC/RPMC/ni_ratio.csv', index=False)
    sales_ratio_merged.to_csv('/Users/shuaijia/Desktop/找工/RPMC/RPMC/sales_ratio.csv', index=False)
    ROA_merged.to_csv('/Users/shuaijia/Desktop/找工/RPMC/RPMC/roa.csv', index=False)
    PE_FY1_merged.to_csv('/Users/shuaijia/Desktop/找工/RPMC/RPMC/PE_FY1.csv', index=False)
