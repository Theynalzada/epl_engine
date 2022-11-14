# Importing Dependencies
from statsmodels.stats.outliers_influence import variance_inflation_factor as VIF
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import numpy as np
import warnings
import yaml

# Filtering potential warnings
warnings.filterwarnings(action = "ignore")

# Loading the yaml file
with open(file = "/Users/kzeynalzade/Documents/EPL Redevelopment/epl_engine/Configuration/config.yml") as yaml_file:
    config = yaml.safe_load(stream = yaml_file)
    
# Extracting the outlier boundary and assigning it to a global variable
OUTLIER_BOUNDARY = config.get("thresholds").get("outlier_boundary")

# Extracting the VIF threshold and assigning it to a global variable
VIF_THRESHOLD = config.get("thresholds").get("vif_threshold")
    
# Defining a custom transformer to handle multicollinearity
class VifDropper(BaseEstimator, TransformerMixin):
    # Initializing the objects
    def __init__(self, threshold = VIF_THRESHOLD):
        # Default VIF threshold
        self.threshold = threshold

    # Defining a fit function
    def fit(self, X, y = None):
        # Creating a copy of converted data frame
        data_frame = pd.DataFrame(data = X).copy()
        
        # Creating a Pandas data_frameframe
        vif_df = pd.DataFrame()
        
        # Assigning the names of columns to a feature variable
        vif_df["feature"] = data_frame.columns
        
        # Calculating VIF values
        vif_df["VIF"] = [VIF(exog = data_frame.values, exog_idx = i) for i in range(len(data_frame.columns))]
        
        # Creating an empty list
        features_with_max_vif = []
        
        # Calculating VIF values of variables based on default threshold
        while vif_df.VIF.max() > self.threshold:
            feature_with_max_vif = vif_df.loc[vif_df.VIF == vif_df.VIF.max()].feature.values[0]
            data_frame.drop(columns = feature_with_max_vif, inplace = True)
            features_with_max_vif.append(feature_with_max_vif)
 
            vif_df = pd.DataFrame()
            vif_df["feature"] = data_frame.columns
            vif_df["VIF"] = [VIF(exog = data_frame.values, exog_idx = i) for i in range(len(data_frame.columns))]
        
        # Defining the list of variables with maximum VIF values
        self.features_with_max_vif = features_with_max_vif
        
        # Returning the objects
        return self 
    
    # Defining a transform function
    def transform(self, X, y = None):
        # Creating a copy of converted data frame
        data_frame = pd.DataFrame(data = X).copy()
        
        # Returning the transformed data frame as an array
        return data_frame.drop(columns = self.features_with_max_vif).values
    
# Defining a custom transformer to winsorize outliers
class IQRWinsorizor(BaseEstimator, TransformerMixin):
    # Initializing the objects
    def __init__(self, map_to_zero = False, outlier_boundary = OUTLIER_BOUNDARY):
        self.outlier_boundary = outlier_boundary
        self.map_to_zero = map_to_zero
        
    # Defining a fit function
    def fit(self, X, y = None):
        # Creating empty lists for upper and lower boundaries
        upper_boundaries = []
        lower_boundaries = []
        
        # Creating a copy of converted data frame
        data_frame = pd.DataFrame(data = X).copy()
        
        # Defining a list of columns
        columns = data_frame.columns.tolist()
        
        # Looping through each column
        for i in columns:
            # Calculating the third quantile
            Q3 = data_frame[i].quantile(q = 0.75)
            
            # Calculating the first quantile
            Q1 = data_frame[i].quantile(q = 0.25)
            
            # Calculating the inter quantile range (IQR)
            IQR = Q3 - Q1
            
            # Calculating the outlier range
            outlier_range = IQR * self.outlier_boundary
            
            # Calculating the upper boundary
            upper_boundary = Q3 + outlier_range
            
            # Calculating the lower boundary
            lower_boundary = Q1 - outlier_range
            
            # Appending the upper boundary to the list
            upper_boundaries.append(upper_boundary)
            
            # Creating a condition based on negative lower boundary
            if not self.map_to_zero:
                # Passing in case the condition is not satisfied
                pass
            else:
                # Checking whether or not a lower boundary is lower than zero
                if lower_boundary < 0:
                    # Setting lower boundary to zero in case it is a negative value
                    lower_boundary = 0
                else:
                    # Passing in case the condition is not satisfied
                    pass
                
            # Appending the lower boundary to the list
            lower_boundaries.append(lower_boundary)
            
            # Winsorizing the outliers
            data_frame[i] = np.where(data_frame[i] > upper_boundary, upper_boundary, data_frame[i])
            data_frame[i] = np.where(data_frame[i] < lower_boundary, lower_boundary, data_frame[i])
            
        # Redefining the objects
        self.upper_boundaries = upper_boundaries
        self.lower_boundaries = lower_boundaries
        
        # Returning the obsjets
        return self
    
    # Defining a transform function
    def transform(self, X, y = None):
        # Creating a copy of converted data frame
        data_frame = pd.DataFrame(data = X).copy()
        
        # Defining a list of columns
        columns = data_frame.columns.tolist()
        
        # Looping through each column
        for index, column in enumerate(iterable = columns):
            # Winsorizing the outliers
            data_frame[column] = np.where(data_frame[column] > self.upper_boundaries[index], self.upper_boundaries[index], data_frame[column])
            data_frame[column] = np.where(data_frame[column] < self.lower_boundaries[index], self.lower_boundaries[index], data_frame[column])
            
        # Returning the transformed data frame as an array
        return data_frame.values