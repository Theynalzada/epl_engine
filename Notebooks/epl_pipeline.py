# Importing Dependencies
from sklearn.preprocessing import RobustScaler, MinMaxScaler, MaxAbsScaler, StandardScaler, OneHotEncoder, OrdinalEncoder, PowerTransformer, QuantileTransformer
from sklearn.feature_selection import RFECV, SelectFpr, SelectFromModel, SelectPercentile, SequentialFeatureSelector
from sklearn.base import BaseEstimator, TransformerMixin
from epl_preprocessing import VifDropper, IQRWinsorizor
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import KFold
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn import set_config
from boruta import BorutaPy

import pandas as pd
import numpy as np
import warnings
import skopt
import yaml

# Filtering potential warnings
warnings.filterwarnings(action = "ignore")

# Defining a setting to visualize a pipeline
set_config(display = "diagram")

# Loading the yaml file
with open(file = "/Users/kzeynalzade/Documents/EPL Redevelopment/epl_engine/Configuration/config.yml") as yaml_file:
    config = yaml.safe_load(stream = yaml_file)

# Loading nominal features for a batch model from engine configuration file
NOMINAL_FEATURES = config.get("features").get("nominal_features")

# Loading ordinal features for a batch model from engine configuration file
ORDINAL_FEATURES = config.get("features").get("ordinal_features")

# Loading binary features for a batch model from engine configuration file
BINARY_FEATURES = config.get("features").get("binary_features")

# Loading date features for a batch model from engine configuration file
DATE_FEATURES = config.get("features").get("date_features")

# Loading features for a batch model from engine configuration file
FEATURES = config.get("features").get("batch_model_features")

# Extracting the evaluation metric that will be used for to optimize a model
OPTIMIZER_METRIC = config.get("metrics").get("optimizer_metric")

# Extracting the teams that are considered as traditional top six
TRADITIONAL_TOP_6 = config.get("2022/23").get("traditional_top_6")
    
# Defining a custom transformer to preprocess features
class InitialPreprocessor(BaseEstimator, TransformerMixin):
    # Defining a fit function
    def fit(self, X, y = None):
        # Copying the data frame
        data_frame = X.copy()
        
        # Creating a list of derbies that do not take place frequently
        low_frequency_derbies = ["West Midlands", "Tyne-Wear", "Roses", "A23"]
        
        # Creating a list of traditional top six clubs
        traditional_top_six = TRADITIONAL_TOP_6
        
        # Creating a list of binary features
        binary_features = BINARY_FEATURES
        
        # Creating a list of nominal features
        nominal_features = NOMINAL_FEATURES
        
        # Creating a list of ordinal features
        ordinal_features = ORDINAL_FEATURES
        
        # Creating a list of date features
        date_features = DATE_FEATURES
        
        # Mapping the clubs that are not considered as traditional top six as "Other"
        data_frame.loc[~data_frame.home_team.isin(values = traditional_top_six), "home_team"] = "Other"
        data_frame.loc[~data_frame.away_team.isin(values = traditional_top_six), "away_team"] = "Other"
        
        # Mapping the low frequency derby names as "Other"
        data_frame.loc[data_frame.derby_name.isin(values = low_frequency_derbies), "derby_name"] = "Other"
        
        # Converting the values of ordinal features from integer to string
        data_frame[ordinal_features] = data_frame[ordinal_features].applymap(func = lambda x: str(x))
        
        # Creating a list of remaining features
        remaining_features = [feature for feature in FEATURES if feature not in date_features + nominal_features + ordinal_features + binary_features]
        
        # Creating a list of reallocated features
        reallocated_features = date_features + nominal_features + ordinal_features + binary_features + remaining_features
        
        # Reallocating the features
        data_frame = data_frame[reallocated_features]
        
        # Redefining the objects
        self.low_frequency_derbies = low_frequency_derbies
        self.reallocated_features = reallocated_features
        self.traditional_top_six = traditional_top_six
        self.ordinal_features = ordinal_features
        
        # Returning the objects
        return self
    
    # Defining a transform function
    def transform(self, X, y = None):
        # Copying the data frame
        data_frame = X.copy()
        
        # Mapping the clubs that are not considered as traditional top six as "Other"
        data_frame.loc[~data_frame.home_team.isin(values = self.traditional_top_six), "home_team"] = "Other"
        data_frame.loc[~data_frame.away_team.isin(values = self.traditional_top_six), "away_team"] = "Other"
        
        # Mapping the low frequency derby names as "Other"
        data_frame.loc[data_frame.derby_name.isin(values = self.low_frequency_derbies), "derby_name"] = "Other"
        
        # Converting the values of ordinal features from integer to string
        data_frame[self.ordinal_features] = data_frame[self.ordinal_features].applymap(func = lambda x: str(x))
        
        # Reallocating the features
        data_frame = data_frame[self.reallocated_features]
        
        # Returning the transformed data frame
        return data_frame
    
def build_pipeline(classifier = None,
                   apply_feature_scaling = False,
                   feature_scaler_type = None,
                   drop_multicollinear_features = False,
                   winsorize_outliers = False,
                   apply_feature_selection = False,
                   feature_selection_type = None,
                   apply_bayesian_optimization = False,
                   hyperparameters = None,
                   n_iterations = 50,
                   train_features = None,
                   train_labels = None,
                   metric = OPTIMIZER_METRIC,
                   verbosity = 0):
    """
    This function is used to build a classifier pipeline.
    
    Args:
        classifier: A classifier instance.
        apply_feature_scaling: Whether or not to apply feature scaling.
        feature_scaler_type: A feature scaling method.
        drop_multicollinear_features: Whether or not to drop multicollinear features with high variance inflation factor (VIF) values.
        winsorize_outliers: Whether or not to winsorize outliers.
        apply_feature_selection: Whether or not to apply feature selection.
        feature_selection_type: A feature selection method.
        apply_bayesian_optimization: Whether or not to apply Bayesian Optimization to find the best hyperparameters.
        hyperparameters: A dictionary of search spaces.
        n_iterations: The number of search iterations for hyperparameter tuning.
        train_features: Train features as a data frame object.
        train_labels: Train labels as a series object.
        metric: A classification metric based on which to optimize a model.
        verbosity: A level of verbosity to display an output of Bayesian Optimization.
        
    Returns:
        Builds a classifier pipeline.
    """
    # Instantiating the cross validation technique
    kf = KFold()
    
    # Creating a dictionary of feature selector instances
    feature_selectors_dict = {"wrapper": SequentialFeatureSelector(estimator = classifier, scoring = metric, cv = kf, n_jobs = -1), 
                              "hybrid": RFECV(estimator = classifier, cv = kf, scoring = metric, n_jobs = -1),
                              "tree_based": BorutaPy(estimator = classifier, random_state = 42),
                              "meta": SelectFromModel(estimator = classifier),
                              "mutual_info": SelectPercentile(), 
                              "filter": SelectFpr()}
    
    # Creating a dictionary of feature scaler instances
    feature_scalers_dict = {"quantile": QuantileTransformer(random_state = 42),
                            "standard": StandardScaler(),
                            "power": PowerTransformer(),
                            "robust": RobustScaler(), 
                            "minmax": MinMaxScaler(), 
                            "maxabs": MaxAbsScaler()}
    
    # Creating a list of positions
    positions = [str(i) for i in list(range(1, 21))][::-1]
    
    # Creating a list of streak forms
    forms = ["Out of Interval", "Relegation Form", "Bad Form", "Mixed Form", "Good Form", "Hot Form"]
    
    # Creating a list of streak forms
    club_tiers = ["Small Club", "Considered as a Big Club", "Big Club", "Huge Club", "Elite Club"]
    
    # Creating a list of nominal features
    nominal_features = NOMINAL_FEATURES
    
    # Creating a list of ordinal features
    ordinal_features = ORDINAL_FEATURES
    
    # Creating a list of binary features
    binary_features = BINARY_FEATURES
    
    # Creating a list of date features
    date_features = DATE_FEATURES
    
    # Creating a list of numeric features
    numeric_features = [feature for feature in FEATURES if feature not in nominal_features + ordinal_features + date_features + binary_features]
    
    # Creating a pipeline for ordinal features
    nominal_pipeline = Pipeline(steps = [("imputer", SimpleImputer(strategy = "most_frequent")),
                                         ("ohe", OneHotEncoder(handle_unknown = "ignore"))])
    
    # Creating a pipeline for ordinal features
    ordinal_pipeline = Pipeline(steps = [("imputer", SimpleImputer(strategy = "constant")),
                                         ("ore", OrdinalEncoder(categories = [club_tiers, club_tiers,
                                                                              positions, positions, 
                                                                              forms, forms], 
                                                                handle_unknown = "use_encoded_value", 
                                                                unknown_value = -1))])
    
    # Creating a pipeline for binary features
    binary_pipeline = Pipeline(steps = [("imputer", SimpleImputer(strategy = "most_frequent"))])
    
    # Creating a condition based on preprocessing steps in a pipeline for numeric features
    if not apply_feature_scaling and not drop_multicollinear_features and not winsorize_outliers:
        # Creating a pipeline for numeric features
        numeric_pipeline = Pipeline(steps = [("imputer", SimpleImputer(strategy = "median"))])
    elif apply_feature_scaling and not drop_multicollinear_features and not winsorize_outliers:
        # Creating a pipeline for numeric features
        numeric_pipeline = Pipeline(steps = [("imputer", SimpleImputer(strategy = "median")),
                                             ("feature_scaler", feature_scalers_dict.get(feature_scaler_type))])
    elif not apply_feature_scaling and drop_multicollinear_features and not winsorize_outliers:
        # Creating a pipeline for numeric features
        numeric_pipeline = Pipeline(steps = [("imputer", SimpleImputer(strategy = "median")),
                                             ("vif_dropper", VifDropper())])
    elif not apply_feature_scaling and not drop_multicollinear_features and winsorize_outliers:
        # Creating a pipeline for numeric features
        numeric_pipeline = Pipeline(steps = [("imputer", SimpleImputer(strategy = "median")),
                                             ("winsorizor", IQRWinsorizor(map_to_zero = True))])
    elif apply_feature_scaling and drop_multicollinear_features and not winsorize_outliers:
        # Creating a pipeline for numeric features
        numeric_pipeline = Pipeline(steps = [("imputer", SimpleImputer(strategy = "median")),
                                             ("vif_dropper", VifDropper()),
                                             ("feature_scaler", feature_scalers_dict.get(feature_scaler_type))])
    elif apply_feature_scaling and not drop_multicollinear_features and winsorize_outliers:
        # Creating a pipeline for numeric features
        numeric_pipeline = Pipeline(steps = [("imputer", SimpleImputer(strategy = "median")),
                                             ("winsorizor", IQRWinsorizor(map_to_zero = True)),
                                             ("feature_scaler", feature_scalers_dict.get(feature_scaler_type))])
    elif not apply_feature_scaling and drop_multicollinear_features and winsorize_outliers:
        # Creating a pipeline for numeric features
        numeric_pipeline = Pipeline(steps = [("imputer", SimpleImputer(strategy = "median")),
                                             ("vif_dropper", VifDropper()),
                                             ("winsorizor", IQRWinsorizor(map_to_zero = True))])
    else:
        # Creating a pipeline for numeric features
        numeric_pipeline = Pipeline(steps = [("imputer", SimpleImputer(strategy = "median")),
                                             ("vif_dropper", VifDropper()),
                                             ("winsorizor", IQRWinsorizor(map_to_zero = True)),
                                             ("feature_scaler", feature_scalers_dict.get(feature_scaler_type))])
    
    # Creating a feature transformer
    feature_transformer = ColumnTransformer(transformers = [("nominal_pipeline", nominal_pipeline, nominal_features),
                                                            ("ordinal_pipeline", ordinal_pipeline, ordinal_features),
                                                            ("binary_pipeline", binary_pipeline, binary_features),
                                                            ("numeric_pipeline", numeric_pipeline, numeric_features)], 
                                            remainder = "passthrough",
                                            n_jobs = -1)
    
    # Creating a condition to apply feature selection
    if not apply_feature_selection:
        # Creating a classifier pipeline
        pipe = Pipeline(steps = [("initial_preprocessor", InitialPreprocessor()),
                                 ("feature_transformer", feature_transformer),
                                 ("classifier", classifier)])
    else:
        # Creating a classifier pipeline
        pipe = Pipeline(steps = [("initial_preprocessor", InitialPreprocessor()),
                                 ("feature_transformer", feature_transformer),
                                 ("feature_selector", feature_selectors_dict.get(feature_selection_type)),
                                 ("classifier", classifier)])
        
    # Creating a condition to apply Bayesian Optimization
    if not apply_bayesian_optimization:
        # Fitting the train features and labels
        pipe.fit(X = train_features, y = train_labels)
    else:
        # Defining an operating level seed
        np.random.seed(seed = 42)
        
        # Instantiating the BayesSearchCV algorithm
        bayes_search = skopt.BayesSearchCV(estimator = pipe, 
                                           search_spaces = hyperparameters, 
                                           n_iter = n_iterations, 
                                           scoring = metric, 
                                           n_jobs = -1, 
                                           cv = kf, 
                                           verbose = verbosity, 
                                           random_state = 42)
        
        # Fitting the train features and labels
        bayes_search.fit(X = train_features, y = train_labels)
        
        # Extracting the best classifier pipeline
        pipe = bayes_search.best_estimator_
        
    # Returning the classifier pipeline
    return pipe