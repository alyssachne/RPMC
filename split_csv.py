import pandas as pd

import pandas as pd
import numpy as np

def create_csv(indicator_name, df, tickers):
    # Step 1: Create the file name from the indicator_name
    file_name = f"{indicator_name}.csv"
    
    # Step 2: Create an empty DataFrame to hold the data
    combined_df = pd.DataFrame()

    # Step 3: Ensure the 'date' column is in the DataFrame and set it as index
    df['date'] = pd.to_datetime(df['Date'])  # Convert date to datetime if necessary
    df.set_index('date', inplace=True)

    # Step 4: Iterate through each ticker, merge the data into the combined_df
    for ticker in tickers:
        ticker_data = df[f'{ticker}_{indicator_name}'].copy()
        combined_df = pd.merge(combined_df, ticker_data, how='outer', left_index=True, right_index=True)

    # Step 5: Fill missing values with NaN
    combined_df.sort_index(inplace=True)

    # Step 6: Save the DataFrame to a CSV file
    combined_df.to_csv(file_name)

    print(f"CSV file created: {file_name}")


def get_tickers(df):
    """
    Get all the tickers from the csv

    Coming from first row: Date,LLY_sales,LLY_NI,LLY_ROA,LLY_PE_FY1,UNH_sales,UNH_NI,UNH_ROA,UNH_PE_FY1,JNJ_sales,JNJ_NI,JNJ_ROA,JNJ_PE_FY1
    Should return: [LLY, UNH, JNJ]
    """
    # Extract column names excluding 'Date'
    columns = df.columns[1:]  # Skip the 'Date' column
    tickers = set()  # Use a set to avoid duplicates

    # Loop through the column names to extract tickers
    for col in columns:
        ticker = col.split('_')[0]  # Get the part before the underscore
        tickers.add(ticker)  # Add to the set

    return list(tickers)

def get_indicators(df):
    """
    Get all the indicators from the csv

    Coming from first row: Date,LLY_sales,LLY_NI,LLY_ROA,LLY_PE_FY1,UNH_sales,UNH_NI,UNH_ROA,UNH_PE_FY1,JNJ_sales,JNJ_NI,JNJ_ROA,JNJ_PE_FY1
    Should return: [sales, NI, ROA, PE_FY1]

    Start after Date, for each header, split('_') to get ticker and indicator
    Append to result list until the ticker is different
    """
    # Extract column names excluding 'Date'
    columns = df.columns[1:]  # Skip the 'Date' column
    indicators = []  # List to store unique indicators
    last_ticker = None  # Variable to track the last ticker

    # Loop through the column names to extract indicators
    for col in columns:
        ticker, indicator = col.split('_', 1)  # Split only on the first underscore
        if last_ticker is not None and ticker != last_ticker: 
            break
        if indicator not in indicators:  # Avoid duplicates
            indicators.append(indicator)  # Add the indicator to the list
        last_ticker = ticker  # Update the last ticker

    return indicators  # Return the list of indicators

def main(csv_path):
    # Load the original CSV file
    df = pd.read_csv(csv_path)
    tickers = get_tickers(df)
    columns = get_indicators(df)
    for col in columns:
        create_csv(col, df, tickers)

if __name__ == "__main__":
    csv_path = 'data/all_tickers_data.csv'
    main(csv_path=csv_path)
