# Importing Dependencies
from statsmodels.stats.outliers_influence import variance_inflation_factor as VIF
from feature_engineering import apply_feature_engineering
from sklearn.base import BaseEstimator, TransformerMixin
from datetime import timedelta
import streamlit as st
import pandas as pd
import numpy as np
import warnings
import pickle
import time
import yaml
import PIL

# Filtering warnings
warnings.filterwarnings(action = 'ignore')

# Definig a global seed to maintain reproducibility of outputs
np.random.seed(seed = 42)

# Defining a function to load a yaml file
def load_yaml(filepath = None):
    """
    This is a function that will load a yaml file.
    
    Args:
        filepath: A path to a yaml file.
        
    Returns:
        A dictionary object.
    """
    # Loading the yaml file
    with open(file = filepath) as yaml_file:
        config = yaml.safe_load(stream = yaml_file)
    
    # Returning the yaml file
    return config

## Loading model properties from a yaml file
CONFIG = load_yaml(filepath = 'config.yml')

# Loading features for a batch model from model properties
FEATURES = CONFIG.get('features').get('batch_model_features')

# Extracting the path for the Loss model 
LOSS_MODEL_PATH = CONFIG.get('models_paths').get('loss_model_path')

# Extracting the path for the Draw model 
DRAW_MODEL_PATH = CONFIG.get('models_paths').get('draw_model_path')

# Extracting the path for the Win model 
WIN_MODEL_PATH = CONFIG.get('models_paths').get('win_model_path')

# Extracting the path for the Loss model 
SHADOW_LOSS_MODEL_PATH = CONFIG.get('shadow_models_paths').get('shadow_loss_model_path')

# Extracting the path for the Draw model 
SHADOW_DRAW_MODEL_PATH = CONFIG.get('shadow_models_paths').get('shadow_draw_model_path')

# Extracting the path for the Win model 
SHADOW_WIN_MODEL_PATH = CONFIG.get('shadow_models_paths').get('shadow_win_model_path')

# Loading the dependent variable for Loss modeling
LOSS_TARGET = CONFIG.get('target').get('loss_model')

# Loading the dependent variable for Draw modeling
DRAW_TARGET = CONFIG.get('target').get('draw_model')

# Loading the dependent variable for Win modeling
WIN_TARGET = CONFIG.get('target').get('win_model')

# Defining a custom transformer to reallocate variables
class FeatureReallocator(BaseEstimator, TransformerMixin):
    # Defining a function for fitting data to custom transformer
    def fit(self, X, y = None):
        # Creating a list of binary features
        binary_features = [feature for feature in FEATURES if X[feature].nunique() == 2]

        # Creating a list of date features
        date_features = ['match_week', 'month', 'day', 'weekday']

        # Creating a list of ordinal features
        ordinal_features = ['h_position', 'a_position']

        # Creating a list of numeric features
        left_out_features = [feature for feature in X.columns.tolist() if feature not in binary_features + date_features + ordinal_features]

        # Creating a list of reallocated features
        reallocated_features = date_features + ordinal_features + left_out_features + binary_features
        
        # Defining the list for feature reallocation
        self.reallocated_features = reallocated_features
        
        # Defining the list for ordinal features
        self.ordinal_features = ordinal_features
        
        # Returning the fitted and transformed data
        return self
    
    # Defining a function for transforming data with custom transformer
    def transform(self, X, y = None):
        # Reallocating variables
        X = X[[feature for feature in self.reallocated_features if feature in FEATURES]]
        
        # Converting the values of ordinal variables into string
        X[self.ordinal_features] = X[self.ordinal_features].applymap(func = lambda x: str(x))
        
        # Returning the transformed data
        return X
    
# Defining a custom transformer to remove multicollinearity
class VifDropper(BaseEstimator, TransformerMixin):
    # Initializing the default threshold for variance inflation factor (VIF)
    def __init__(self, threshold = 2.5):
        # Default VIF threshold
        self.threshold = threshold

    # Defining a function for fitting data to custom transformer
    def fit(self, X, y = None):
        # Creating a copy of a Numpy array as Pandas dataframe
        data = pd.DataFrame(data = X).copy()
        
        # Creating a Pandas dataframe
        vif_df = pd.DataFrame()
        
        # Assigning the names of columns to a feature variable
        vif_df['feature'] = data.columns
        
        # Calculating VIF values
        vif_df['VIF'] = [VIF(exog = data.values, exog_idx = i) for i in range(len(data.columns))]
        
        # Creating an empty list
        features_with_max_vif = []
        
        # Calculating VIF values of variables based on default threshold
        while vif_df.VIF.max() > self.threshold:
            feature_with_max_vif = vif_df.loc[vif_df.VIF == vif_df.VIF.max()].feature.values[0]
            data.drop(columns = feature_with_max_vif, inplace = True)
            features_with_max_vif.append(feature_with_max_vif)
 
            vif_df = pd.DataFrame()
            vif_df['feature'] = data.columns
            vif_df['VIF'] = [VIF(exog = data.values, exog_idx = i) for i in range(len(data.columns))]
        
        # Defining the list of variables with maximum VIF values
        self.features_with_max_vif = features_with_max_vif
        
        # Returning the fitted and transformed data
        return self 
    
    # Defining a function for transforming data with custom transformer
    def transform(self, X, y = None):
        # Returning the transformed data
        return pd.DataFrame(data = X).drop(columns = self.features_with_max_vif).values
    
# Loading the Loss model
with open(file = LOSS_MODEL_PATH, mode = 'rb') as pickled_model:
    loss_model = pickle.load(file = pickled_model)

# Loading the Draw model
with open(file = DRAW_MODEL_PATH, mode = 'rb') as pickled_model:
    draw_model = pickle.load(file = pickled_model)

# Loading the Win model
with open(file = WIN_MODEL_PATH, mode = 'rb') as pickled_model:
    win_model = pickle.load(file = pickled_model)
    
# Loading the Shadow Loss model
with open(file = SHADOW_LOSS_MODEL_PATH, mode = 'rb') as pickled_model:
    shadow_loss_model = pickle.load(file = pickled_model)

# Loading the Shadow Draw model
with open(file = SHADOW_DRAW_MODEL_PATH, mode = 'rb') as pickled_model:
    shadow_draw_model = pickle.load(file = pickled_model)

# Loading the Shadow Win model
with open(file = SHADOW_WIN_MODEL_PATH, mode = 'rb') as pickled_model:
    shadow_win_model = pickle.load(file = pickled_model)
    
# Loading the unprocessed data of the current season
current_season_df = pd.read_csv(filepath_or_buffer = '2022-23_unprocessed.csv')

# Casting the data type of match_date variable from object to datetime
current_season_df.match_date = pd.to_datetime(arg = current_season_df.match_date, yearfirst = True)

# Assigning the minimum match date
min_match_date = current_season_df.match_date.max()# + pd.DateOffset(days = 1)

# Creating a list of teams
teams = current_season_df.home_team.unique().tolist()

image = PIL.Image.open(fp = 'epl_logo.jpeg')

# Defining a function to generate input data
def generate_input_data(match_week = None, 
                        match_date = None, 
                        home_teams = None, 
                        away_teams = None,
                        unprocessed_data = None):
    
    # Creating a list of week days based on match date 
    weekdays = match_date.weekday() + 1
    
    # Creating a list of months based on match date 
    months = match_date.month
    
    # Creating a list of days based on match date 
    days = match_date.day
    
    # Extracting the season
    season = unprocessed_data.season.unique()[0]
    
    # Creating a dictionary of preliminary variables
    data_dictionary = {'season':season,
                       'match_week':match_week,
                       'match_date':match_date, 
                       'month':months,
                       'day':days,
                       'weekday':weekdays,
                       'home_team':home_teams, 
                       'away_team':away_teams}
    
    # Converting dictionary into data frame
    input_df = pd.DataFrame(data = data_dictionary, index = [0])
    
    # Casting the data type of match_date variable from object to datetime
    input_df.match_date = pd.to_datetime(arg = input_df.match_date, yearfirst = True)
    
    # Extending the data frame with post-match variables
    input_df = input_df.merge(right = unprocessed_data, how = 'left')
    
    # Concatenating the input data frame with unprocessed data frame vertically
    input_df = pd.concat(objs = [input_df, unprocessed_data], ignore_index = True)
    
    # Sorting the input data frame by match date in descending order
    input_df.sort_values(by = 'match_date', ascending = False, inplace = True)
    
    # Calling the function to apply feature engineering to calculate features
    input_df = apply_feature_engineering(data_frame = input_df)
    
    # Sorting the matches by match date in ascending order 
    input_df = input_df.loc[input_df.match_week == match_week].sort_values(by = 'match_date').reset_index(drop = True)
    
    # Returning input data frame
    return input_df

# Defining a function to make predictions
def make_predictions(data_frame = None, use_shadow_models = False):
    # Creating a list of class labels 
    class_labels = [-1, 0, 1]
    
    # Creating an input data for the Loss model
    loss_data = data_frame.drop(columns = LOSS_TARGET)

    # Creating an input data for the Draw model
    draw_data = data_frame.drop(columns = DRAW_TARGET)

    # Creating an input data for the Win model
    win_data = data_frame.drop(columns = WIN_TARGET)
    
    if not use_shadow_models:
        # Calculating the probabilities for the positive class of the Loss model
        loss_probabilities = np.expand_dims(a = loss_model.predict_proba(X = loss_data)[:, 1], axis = 1)

        # Calculating the probabilities for the positive class of the Draw model
        draw_probabilities = np.expand_dims(a = draw_model.predict_proba(X = draw_data)[:, 1], axis = 1)

        # Calculating the probabilities for the positive class of the Win model
        win_probabilities = np.expand_dims(a = win_model.predict_proba(X = win_data)[:, 1], axis = 1)
    else:
        # Calculating the probabilities for the positive class of the Shadow Loss model
        loss_probabilities = np.expand_dims(a = shadow_loss_model.predict_proba(X = loss_data)[:, 1], axis = 1)

        # Calculating the probabilities for the positive class of the Shadow Draw model
        draw_probabilities = np.expand_dims(a = shadow_draw_model.predict_proba(X = draw_data)[:, 1], axis = 1)

        # Calculating the probabilities for the positive class of the Shadow Win model
        win_probabilities = np.expand_dims(a = shadow_win_model.predict_proba(X = win_data)[:, 1], axis = 1)
        
    # Creating an array of probabilities of each model
    probabilities = np.hstack(tup = (loss_probabilities, draw_probabilities, win_probabilities))
    
    # Creating a list of predictions based on maximum probability index
    prediction = [class_labels[class_label] for class_label in probabilities.argmax(axis = 1)]
    
    # Extracting the probability for the prediction 
    probability = [probas[probas.argmax()] for probas in probabilities]
    
    # Assigning engine predictions to prediction column
    data_frame['prediction'] = prediction
    
    # Assigning engine probabilities to probability column
    data_frame['probability'] = probability

    # Creating an engine output variable
    data_frame['engine_output'] = ''
    
    # Creating a confidence interval variable
    data_frame['confidence'] = ''
    
    # Creating a bet making variable
    data_frame['bet'] = False
    
    # Creating confidence interval boundaries
    data_frame.loc[data_frame.probability < 0.35, 'confidence'] = 'Very Low'
    data_frame.loc[data_frame.probability.between(left = 0.35, right = 0.55, inclusive = 'left'), 'confidence'] = 'Low'
    data_frame.loc[data_frame.probability.between(left = 0.55, right = 0.65, inclusive = 'left'), 'confidence'] = 'Medium'
    data_frame.loc[data_frame.probability.between(left = 0.65, right = 0.85, inclusive = 'left'), 'confidence'] = 'High'
    data_frame.loc[data_frame.probability >= 0.85, 'confidence'] = 'Very High'
    
    # Assigning a positive boolean value to matches where engine suggests to make a bet
    data_frame.loc[data_frame.confidence.isin(values = ['High', 'Very High']), 'bet'] = True
    
    # Engine output message for victories
    win_output = data_frame.loc[data_frame.prediction == 1][['home_team', 'away_team', 'probability']].\
    apply(func = lambda x: f'Probability of {x[0]} beating {x[1]} at home is {x[-1]:.0%}.', axis = 1)
    
    # Engine output message for defeats
    loss_output = data_frame.loc[data_frame.prediction == -1][['home_team', 'away_team', 'probability']].\
    apply(func = lambda x: f'Probability of {x[1]} defeating {x[0]} away from home is {x[-1]:.0%}.', axis = 1)
    
    # Engine output message for draws
    draw_output = data_frame.loc[data_frame.prediction == 0][['home_team', 'away_team', 'probability']].\
    apply(func = lambda x: f'Probability of {x[0]} and {x[1]} sharing points is {x[-1]:.0%}.', axis = 1)
    
    # Assigning the engine output messages to engine_output column
    data_frame.loc[data_frame.prediction == 1, 'engine_output'] = win_output
    data_frame.loc[data_frame.prediction == -1, 'engine_output'] = loss_output
    data_frame.loc[data_frame.prediction == 0, 'engine_output'] = draw_output
    
    # Creating a list of output columns
    output_columns = ['season', 'match_week', 'match_date', 'home_team', 'away_team', 
                      'prediction', 'probability', 'confidence', 'bet', 'engine_output']
    
    # Selecting only the output columns
    data_frame = data_frame[output_columns]
    
    return data_frame.engine_output.values[0]

# Instantiating the application
interface = st.container()

# Creating the main page
with interface:
    # Creating a title
    st.title(body = 'English Premier League Engine')
    
    st.image(image = image)
    
    # Creating a subheader
    st.subheader(body = 'Project Description')
    
    # Creating a markdown text
    st.markdown(body = """
    This is an end to end data science project in which the goal is to make accurate and precise predictions about the outcome of a football match beforehand.
    The engine is a combination of three separate machine learning models, one for each outcome. A prediction with the highest probability
    is taken as the final output of the engine. Models have been trained on the last six years of data containing **2280** matches. Engine's performance is evaluated
    based on predictions with probability greater equal than **65%**. In order understand how the entire pipeline works and what kind of features are calculated on the fly
    please read the **README.md** file in the Github repository.
    """)
    
    # Creating a subheader
    st.subheader(body = 'Input Features')
    
    # Creating a markdown text
    st.markdown(body = 'In order to create the input features you can view the latest [fixtures](https://www.premierleague.com/fixtures).')
    
    # Creating four columns containing home & away teams, match week and date
    home_team, away_team, match_week, match_date = st.columns(spec = [1, 1, 1, 1])
    
    with home_team:
        # Selecting a home team
        home_team = st.selectbox(label = 'Home Team', options = sorted(teams))
        
    with away_team:
        # Removing the home team from the list
        teams.remove(home_team)
        
        # Selecting an away team
        away_team = st.selectbox(label = 'Away Team', options = teams)
        
    with match_week:
        # Selecting a match week
        match_week = st.selectbox(label = 'Match Week', options = list(range(1, 39)))
        
    with match_date:
        # Specifying a match date
        match_date = st.date_input(label = 'Match Date', min_value = min_match_date)

    # Creating a straight line
    st.markdown(body = '***')
    
    # Creating a subheader
    st.subheader(body = 'Engine Prediction')
    
    # Creating a prediction button
    if st.button(label = 'Predict'):
        # Creating a spinner
        with st.spinner('Input features are being sent to the engine...'):
            # Making a little pause
            time.sleep(1.5)
        
        # Displaying the information about the engine features being calculating
        st.warning(body = 'Engine features are being calculated..')
        
        # Making a little pause
        time.sleep(1)
            
        # Calling the function to generate input data
        input_data = generate_input_data(match_week = match_week,
                                         match_date = match_date,
                                         home_teams = home_team,
                                         away_teams = away_team,
                                         unprocessed_data = current_season_df)
            
        # Making prediction with the engine
        prediction = make_predictions(data_frame = input_data)
        
        # Displaying the success message when the engine prediction is ready
        st.success('Engine prediction is ready!')
        
        # Making a little pause
        time.sleep(0.5)

        # Displaying output of the engine
        st.markdown(body = prediction)