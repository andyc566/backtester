import pandas as pd
import numpy as np
from sqlalchemy import create_engine

def load_sql_data(query, connection_string):
    """
    Load data from an SQL database.
    
    Parameters:
        query (str): SQL query to fetch data.
        connection_string (str): Connection string to the database.
        
    Returns:
        pd.DataFrame: Data loaded from the database.
    """
    engine = create_engine(connection_string)
    with engine.connect() as connection:
        data = pd.read_sql(query, connection)
    return data

def load_csv_data(file_path):
    """
    Load data from a CSV file.
    
    Parameters:
        file_path (str): Path to the CSV file.
        
    Returns:
        pd.DataFrame: Data loaded from the file.
    """
    return pd.read_csv(file_path, parse_dates=['date'])

def preprocess_data(data):
    """
    Preprocess and clean the data.
    
    Parameters:
        data (pd.DataFrame): Input data.
        
    Returns:
        pd.DataFrame: Preprocessed data with missing values handled.
    """
    # Handle missing data
    data = data.fillna(method='ffill').fillna(method='bfill')
    
    # Ensure the date column is in datetime format
    if 'date' in data.columns:
        data['date'] = pd.to_datetime(data['date'])
        
    return data

def merge_data(data_frames):
    """
    Merge multiple data sources on time (date) and align them.
    
    Parameters:
        data_frames (list of pd.DataFrame): List of dataframes to be merged.
        
    Returns:
        pd.DataFrame: Merged dataframe aligned on the 'date' column.
    """
    merged_data = data_frames[0]
    for df in data_frames[1:]:
        merged_data = pd.merge(merged_data, df, on='date', how='outer')
    
    # Sort by date to ensure data is time-aligned
    merged_data = merged_data.sort_values(by='date').reset_index(drop=True)
    return merged_data

def calculate_degree_days(temperature_data):
    """
    Calculate Heating and Cooling Degree Days.
    
    Parameters:
        temperature_data (pd.DataFrame): Temperature data with a 'temperature' column.
        
    Returns:
        pd.DataFrame: Data with Heating and Cooling Degree Days.
    """
    temperature_data['HDD'] = np.maximum(65 - temperature_data['temperature'], 0)
    temperature_data['CDD'] = np.maximum(temperature_data['temperature'] - 65, 0)
    return temperature_data

def normalize_data(data, columns_to_normalize):
    """
    Normalize or standardize specific columns in the dataset.
    
    Parameters:
        data (pd.DataFrame): Input data.
        columns_to_normalize (list of str): List of column names to normalize.
        
    Returns:
        pd.DataFrame: Data with normalized columns.
    """
    for col in columns_to_normalize:
        data[col] = (data[col] - data[col].mean()) / data[col].std()
    
    return data

# Example usage:
if __name__ == '__main__':
    # Load data from various sources
    futures_data = load_sql_data("SELECT * FROM futures_prices", "sqlite:///futures.db")
    weather_data = load_csv_data("weather_data.csv")
    storage_data = load_sql_data("SELECT * FROM storage_estimates", "sqlite:///storage.db")

    # Preprocess and align data
    futures_data = preprocess_data(futures_data)
    weather_data = preprocess_data(weather_data)
    storage_data = preprocess_data(storage_data)
    
    # Merge data on time (assuming all have a 'date' column)
    merged_data = merge_data([futures_data, weather_data, storage_data])

    # Calculate degree days for weather data
    merged_data = calculate_degree_days(merged_data)

    # Normalize relevant columns (e.g., futures price, storage levels)
    columns_to_normalize = ['futures_price', 'storage_level']
    normalized_data = normalize_data(merged_data, columns_to_normalize)

    print(normalized_data.head())
