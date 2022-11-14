# Importing Dependencies
import pandas as pd
import numpy as np
import warnings
import yaml
import os

# Filtering potential warnings
warnings.filterwarnings(action = "ignore")

# Loading the yaml file
with open(file = "../Configuration/config.yml") as yaml_file:
    config = yaml.safe_load(stream = yaml_file)

# Extracting the path to datasets and assigning it to a global variable
TARGET_PATH = config.get("dataset_path")

# Extracting the current season and assigning it to a global variable
CURRENT_SEASON = config.get("current_season")

# Defining a function to load the dataset
def load_data(target_path = TARGET_PATH, 
              current_season = CURRENT_SEASON,
              non_na_ratio = 0.6):
    """
    This is a function that is used to load datasets from a specified path and create a cohesive dataset.
    
    Args:
        target_path: A path for the datasets.
        current_season: A current season.
        non_na_ratio: A non na ratio for variables.
        
    Returns:
        A pandas data frame.
    """
    # Creating a list of datasets based on the specified path
    datasets = [f"{target_path}/{file}" for file in os.listdir(path = target_path) if file.endswith(".brotli")]
    
    # Loading the datasets using list comprehension
    data_frames = [pd.read_parquet(path = dataset, engine = "fastparquet") for dataset in datasets]
    
    # Concatenating data frames to create a cohesive data frame
    data_frame = pd.concat(objs = data_frames, ignore_index = True)
    
    # Casting the data type of the match date variable from object to datetime
    data_frame.match_date = pd.to_datetime(arg = data_frame.match_date, yearfirst = True)
    
    # Sorting the observations based on match_date variable in ascending order
    data_frame.sort_values(by = "match_date", inplace = True)
    
    # Reseting the index to maintain index order
    data_frame.reset_index(drop = True, inplace = True)
    
    # Removing potential duplicate observations
    data_frame.drop_duplicates(inplace = True, ignore_index = True)
    
    # Dropping features that exceed non na ratio
    data_frame.dropna(axis = 1, thresh = int(data_frame.shape[0] * non_na_ratio), inplace = True)
    
    # Filtering out the matches of the current season and sorting matches by match date in ascending order
    data_frame = data_frame.loc[data_frame.season != current_season].sort_values(by = "match_date")
    
    # Returning the data frame
    return data_frame