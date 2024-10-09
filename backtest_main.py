import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt


def null_visualization(df):
    # Check for columns with null values and count how many nulls per column
    null_counts = df.isnull().sum()

    # Filter to only columns that contain null values
    columns_with_null = null_counts[null_counts > 0]

    # Visualize the result
    plt.figure(figsize=(8, 6))
    ax = columns_with_null.plot(kind='bar', color='skyblue')
    plt.title('Number of Null Values per Column')
    plt.ylabel('Number of Null Values')
    plt.xlabel('Columns')
    plt.xticks(rotation=45)
    
    # Annotate the bar chart with the number of null values at the top of each bar
    for p in ax.patches:
        ax.annotate(f'{int(p.get_height())}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 10), textcoords='offset points')
    
    plt.tight_layout()
    plt.show()

    # Return the names of the columns containing null values
    columns_with_null_names = columns_with_null.index.tolist()
    print("Columns with null values:", columns_with_null_names)

price_df_all_tickers = pd.read_csv('/Users/shuaijia/Desktop/找工/RPMC/RPMC/price_df_all_tickers.csv')
ni_ratio_df = pd.read_csv('/Users/shuaijia/Desktop/找工/RPMC/RPMC/ni_ratio.csv')
roa_df = pd.read_csv('/Users/shuaijia/Desktop/找工/RPMC/RPMC/roa.csv')
sales_ratio_df = pd.read_csv('/Users/shuaijia/Desktop/找工/RPMC/RPMC/sales_ratio.csv')
PE_FY1_df = pd.read_csv('/Users/shuaijia/Desktop/找工/RPMC/RPMC/PE_FY1.csv')


null_visualization(ni_ratio_df)
null_visualization(PE_FY1_df)
null_visualization(roa_df)
null_visualization(sales_ratio_df)


def screen_df(ni_df, PE_FY1_df, roa_df, sales_ratio_df, price_df_all_tickers):
    for num in range(len(price_df_all_tickers)):
        
        date = price_df_all_tickers['Date'][num][:10]
        PE_FY1_spec = PE_FY1_df[PE_FY1_df['Date'] == date]
        PE_FY1_spec = PE_FY1_spec.drop('Date',axis = 1)
        
        #Find the date in price df corresponding to the starting date in PE_FY1
        if not PE_FY1_spec.empty:
            PE_FY1_spec = PE_FY1_spec[PE_FY1_spec < 25].dropna(axis=1)
            columns = PE_FY1_spec.columns.tolist()
            

            #print(len(columns))
            print(date)
            break

        



    


    pass


screen_df(ni_df, PE_FY1_df, roa_df, sales_ratio_df, price_df_all_tickers)


