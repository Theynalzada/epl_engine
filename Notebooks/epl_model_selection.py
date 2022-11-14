# Importing Dependencies
import pandas as pd
import numpy as np
import warnings
import yaml

# Filtering potential warnings
warnings.filterwarnings(action = "ignore")

# Loading the yaml file
with open(file = "../Configuration/config.yml") as yaml_file:
    config = yaml.safe_load(stream = yaml_file)

# Extracting the cutoff season that will be used to create train and test sets
CUTOFF_SEASON = config.get("train_test_split").get("cutoff_season")

# Defining a function to split data into train and test set based on time dimension
def train_test_split(data_frame = None, 
                     cutoff_season = CUTOFF_SEASON, 
                     target = None):
    """
    This function is used to split data into train & test sets.
    
    Args:
        data_frame: A pandas data frame.
        cutoff_season: A season which will be used to create train and test sets.
        target: A dependent variable.
        
    Returns:
        Features and labels for train & test set.
    """
    # Identifying the first match date in the test season
    split_date = str(data_frame.loc[data_frame.season == cutoff_season, "match_date"].min()).split()[0]
    
    # Creating train & test sets
    train_set = data_frame.loc[data_frame.match_date < split_date].reset_index(drop = True)
    test_set = data_frame.loc[data_frame.match_date >= split_date].reset_index(drop = True)
    
    # Creating features for train & test set
    X_train = train_set.drop(columns = target)
    X_test = test_set.drop(columns = target)
    
    # Creating labels for train & test set
    y_train = train_set[target]
    y_test = test_set[target]
    
    # Returning train & test features and labels
    return X_train, X_test, y_train, y_test