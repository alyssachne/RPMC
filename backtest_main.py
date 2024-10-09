import pandas as pd
import numpy as np
from datetime import datetime
import json
import matplotlib.pyplot as plt


def null_visualization(df, data_type):
    # Check for columns with null values and count how many nulls per column
    null_counts = df.isnull().sum()

    # Filter to only columns that contain null values
    columns_with_null = null_counts[null_counts > 0]
    # Return the names of the columns containing null values
    columns_with_null_names = columns_with_null.index.tolist()
    null_dict = {}
    for col, count in zip(columns_with_null_names, columns_with_null):
        null_dict[col] = count
    
    null_df = pd.DataFrame.from_dict(null_dict, orient='index', columns=[data_type])

    return null_df

def null_count_by_date(df,data_type):
    # Count the number of null values in each row
    null_counts = df.isnull().sum(axis=1)
    
    # Create a DataFrame with 'Date' and the corresponding null counts
    null_df = pd.DataFrame({'Date': df['Date'], f'{data_type}': null_counts}).reset_index(drop=True)
    
    return null_df

#Read the csv
price_df_all_tickers = pd.read_csv('/Users/shuaijia/Desktop/找工/RPMC/RPMC/price_df_all_tickers.csv')
ni_ratio_df = pd.read_csv('/Users/shuaijia/Desktop/找工/RPMC/RPMC/ni_ratio.csv')
roa_df = pd.read_csv('/Users/shuaijia/Desktop/找工/RPMC/RPMC/roa.csv')
sales_ratio_df = pd.read_csv('/Users/shuaijia/Desktop/找工/RPMC/RPMC/sales_ratio.csv')
PE_FY1_df = pd.read_csv('/Users/shuaijia/Desktop/找工/RPMC/RPMC/PE_FY1.csv')

#Count null value by ticker
ni_ratio_null = null_visualization(ni_ratio_df,"ni_ratio")
PE_FY1_null = null_visualization(PE_FY1_df,"PE_FY1")
roa_null = null_visualization(roa_df,"roa")
sales_ratio_null = null_visualization(sales_ratio_df,"sales_ratio")

merged_df = pd.merge(ni_ratio_null, PE_FY1_null, left_index=True, right_index=True, how='outer')
merged_df = pd.merge(merged_df, roa_null, left_index=True, right_index=True, how='outer')
merged_df = pd.merge(merged_df, sales_ratio_null, left_index=True, right_index=True, how='outer')
merged_df.to_csv('/Users/shuaijia/Desktop/找工/RPMC/RPMC/null_value_by_ticker.csv', index=True)

#Count null value by date
ni_ratio_null_by_date = null_count_by_date(ni_ratio_df,"ni_ratio")
PE_FY1_null_by_date = null_count_by_date(PE_FY1_df,"PE_FY1")
roa_null_by_date = null_count_by_date(roa_df,"roa")
sales_ratio_null_by_date = null_count_by_date(sales_ratio_df,"sales_ratio")

# Merge the DataFrames on the 'Date' column
merged_df_2 = pd.merge(ni_ratio_null_by_date, PE_FY1_null_by_date, on='Date', how='outer')
merged_df_2 = pd.merge(merged_df_2, roa_null_by_date, on='Date', how='outer')
merged_df_2 = pd.merge(merged_df_2, sales_ratio_null_by_date, on='Date', how='outer')
merged_df_2.to_csv('/Users/shuaijia/Desktop/找工/RPMC/RPMC/null_value_by_date.csv', index=False)


#Filter the indicator dataframe to eliminate the rows of which that majority of columns is null 
index_of_date = PE_FY1_df[PE_FY1_df['Date'] == '2015-12-01'].index[0]
# Step 2: Slice the DataFrame to get all rows after the found index
PE_FY1_spec = PE_FY1_df.iloc[index_of_date:]

index_of_date = ni_ratio_df[ni_ratio_df['Date'] == '2015-12-01'].index[0]
ni_ratio_spec = ni_ratio_df.iloc[index_of_date:]

index_of_date = roa_df[roa_df['Date'] == '2015-12-01'].index[0]
roa_spec = roa_df.iloc[index_of_date:]

index_of_date = sales_ratio_df[sales_ratio_df['Date'] == '2015-12-01'].index[0]
sales_ratio_spec = sales_ratio_df.iloc[index_of_date:]


price_df_all_tickers['Date'] = price_df_all_tickers['Date'].str.slice(0, 10)
index_of_date = price_df_all_tickers[price_df_all_tickers['Date'] == '2015-12-01'].index[0]
price_df_all_tickers = price_df_all_tickers.iloc[index_of_date:]
price_df_all_tickers.reset_index(drop=True, inplace=True)

def screen_df(ni_ratio_spec, PE_FY1_df, roa_spec, sales_ratio_spec, price_df_all_tickers):
    daily_tickers = {}
    less_than_2_counter = 0
    for num in range(len(price_df_all_tickers)):
        
        date = price_df_all_tickers['Date'][num]
        #Find the date in price df corresponding to the starting date in PE_FY1
        PE_FY1_value = PE_FY1_df[PE_FY1_df['Date'] == date]
        PE_FY1_value = PE_FY1_value.drop('Date',axis = 1)

        sales_ratio_value = sales_ratio_spec[sales_ratio_spec['Date'] == date]
        sales_ratio_value = sales_ratio_value.drop('Date',axis = 1)

        roa_value = roa_spec[roa_spec['Date'] == date]
        roa_value = roa_value.drop('Date',axis = 1)

        ni_ratio_value = ni_ratio_spec[ni_ratio_spec['Date'] == date]
        ni_ratio_value = ni_ratio_value.drop('Date',axis = 1)


        
        # Filter out all ticker that PE is less than 25 
        PE_FY1_value = PE_FY1_value[PE_FY1_value < 25].dropna(axis=1)
        columns_1 = PE_FY1_value.columns.tolist()
        
        # Filter out all tickers that sales ratio > 10%
        sales_ratio_value = sales_ratio_value[sales_ratio_value > 0.1].dropna(axis=1)
        columns_2 = sales_ratio_value.columns.tolist()

        # Filter out all tickers that ni ratio > 15%
        ni_ratio_value = ni_ratio_value[ni_ratio_value > 0.15].dropna(axis=1)
        columns_3 = ni_ratio_value.columns.tolist()
        
        # Find the intersection of the three lists
        qualified_stock = list(set(columns_1).intersection(columns_2, columns_3))


        # Filter the roa_value DataFrame to include only the qualified stocks
        filtered_roa = roa_value[qualified_stock].squeeze()
        try: 
            # Drop rows (tickers) with NaN values
            filtered_roa = filtered_roa.dropna()
            sorted_roa = filtered_roa.sort_values(ascending=False)
            top_five_roa = sorted_roa.head(5)
            top_five_names = top_five_roa.index.tolist()
            daily_tickers[date] = top_five_names
        except:
            print("less than two values, no action needed")
            daily_tickers[date] = qualified_stock
            print(qualified_stock)
            less_than_2_counter +=1
            print(less_than_2_counter)

        # Convert daily_tickers dictionary to JSON
    daily_tickers_json = json.dumps(daily_tickers)

        # Save daily_tickers JSON to a file
    with open('/Users/shuaijia/Desktop/找工/RPMC/RPMC/daily_tickers.json', 'w') as file:
        file.write(daily_tickers_json)



if __name__ == "__main__":
    screen_df(ni_ratio_spec, PE_FY1_spec, roa_spec, sales_ratio_spec, price_df_all_tickers)


