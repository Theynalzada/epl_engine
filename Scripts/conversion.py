# Importing Dependencies
import pandas as pd
import warnings
import logging
import os

# Filtering warnings
warnings.filterwarnings(action = 'ignore')

# Defining the settings for a logger file
logging.basicConfig(filename = '/Users/kzeynalzade/Documents/Project/Logs/conversion.log', filemode = 'w', format = '%(asctime)s - %(levelname)s - %(message)s', level = logging.INFO)

# Defining the paths for csv files
csv_files_path = '/Users/kzeynalzade/Documents/Project/Data/Processed data'

# Defining the paths for parquet files
target_path = '/Users/kzeynalzade/Documents/Project/Data/Converted data'

# Defining a function to convert csv files to parquet files
def convert_csv_to_parquet(filepath = None):
    # Creating a list of csv files
    csv_files = [f'{filepath}/{file}' for file in os.listdir(path = filepath) if file.endswith('.csv')]
    
    # Looping through each csv file
    for csv_file in csv_files:
        # Reading each csv file
        csv_df = pd.read_csv(filepath_or_buffer = csv_file)
        
        # Extracting the season
        season = csv_df.season.unique()[0].replace('/', '-')
        
        # Saving each csv file as a parquet file
        csv_df.to_parquet(path = f'{target_path}/{season}_season.parquet.brotli', engine = 'fastparquet', compression = 'brotli', index = False)
        
        # Logging information
        logging.info(msg = f'Data for {season} season has been converted and saved as a parquet file')

# Running the script
if __name__ == '__main__':
    # Calling the function to convert csv files to parquet files
    convert_csv_to_parquet(filepath = csv_files_path)