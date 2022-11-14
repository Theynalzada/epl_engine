# Importing Dependencies
from feature_engineering import apply_feature_engineering
from sklearn.metrics import *

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import warnings
import pickle
import yaml
import os

# Filtering potential warnings
warnings.filterwarnings(action = "ignore")

# Configuring the settings based on font scale, style and palette
sns.set(font_scale = 1.5, style = "darkgrid", palette = "bright")

# Configuring the settings based on figure size
plt.rcParams["figure.figsize"] = (30, 10)

# Loading the yaml file
with open(file = "/Users/kzeynalzade/Documents/EPL Redevelopment/epl_engine/Configuration/config.yml") as yaml_file:
    config = yaml.safe_load(stream = yaml_file)

# Extracting the evaluation metric that will be used for probability thresholding
THRESHOLDING_METRIC = config.get('metrics').get('thresholding_metric')

# Extracting the path for the Loss model 
LOSS_MODEL_PATH = config.get('models_paths').get('loss_model_path')

# Extracting the path for the Draw model 
DRAW_MODEL_PATH = config.get('models_paths').get('draw_model_path')

# Extracting the path for the Win model 
WIN_MODEL_PATH = config.get('models_paths').get('win_model_path')

# Loading the current season
CURRENT_SEASON = config.get('current_season').replace('/', '-')

# Loading the dependent variable for the Loss model
LOSS_TARGET = config.get('target').get('loss_model')

# Loading the dependent variable for the Draw model
DRAW_TARGET = config.get('target').get('draw_model')

# Loading the dependent variable for the Win model
WIN_TARGET = config.get('target').get('win_model')

# Loading the Loss model
with open(file = LOSS_MODEL_PATH, mode = 'rb') as pickled_model:
    loss_model = pickle.load(file = pickled_model)

# Loading the Draw model
with open(file = DRAW_MODEL_PATH, mode = 'rb') as pickled_model:
    draw_model = pickle.load(file = pickled_model)

# Loading the Win model
with open(file = WIN_MODEL_PATH, mode = 'rb') as pickled_model:
    win_model = pickle.load(file = pickled_model)

# Defining a function to find the best probability threshold
def find_optimal_threshold(model = None, 
                           metric = THRESHOLDING_METRIC, 
                           train_features = None, 
                           train_labels = None, 
                           test_features = None, 
                           test_labels = None, 
                           beta = None):
    """
    This function is used to find out the best probability thresholds for train & test set.
    
    Args:
        model: A classifier instance.
        metric: A classification metric based on which to optimize a model.
        train_features: Train features.
        train_labels: Train labels.
        test_features: Test features.
        test_labels: Train labels.
        beta: Beta to calculate the F Beta score.
        
    Returns:
        Plots thresholding plots and identifies best probability thresholds for train & test sets.
    """
    # Creating an array of probabilities
    probabilities = np.arange(0.1, 0.91, 0.01)
    
    # Creating a dictionary of labels for evaluation metrics of a classification problem
    metrics_dict = {"accuracy": "Accuracy",
                    "positive_recall": "Positive Recall", 
                    "negative_recall": "Negative Recall",
                    "balanced_accuracy": "Balanced Accuracy", 
                    "positive_precision": "Positive Precision", 
                    "negative_precision": "Negative Precision",
                    "positive_fbeta": f"Positive F{beta}",
                    "negative_fbeta": f"Negative F{beta}"}
    
    # Creating a condition to apply thresholding to a chosen evaluation metric
    if metric == "accuracy":
        # Calculating the accuracy score based on given probability thresholds for train and test set
        train_metrics_per_proba = [accuracy_score(y_true = train_labels, y_pred = np.where(model.predict_proba(X = train_features)[:, 1] >= proba, 1, 0)) for proba in probabilities]
        test_metrics_per_proba = [accuracy_score(y_true = test_labels, y_pred = np.where(model.predict_proba(X = test_features)[:, 1] >= proba, 1, 0)) for proba in probabilities]
        
        # Calculating the accuracy score at default threshold for train and test set
        score_at_default_threshold_train = accuracy_score(y_true = train_labels, y_pred = model.predict(X = train_features))
        score_at_default_threshold_test = accuracy_score(y_true = test_labels, y_pred = model.predict(X = test_features))
    elif metric == "balanced_accuracy":
        # Calculating the balanced accuracy score based on given probability thresholds for train and test set
        train_metrics_per_proba = [balanced_accuracy_score(y_true = train_labels, y_pred = np.where(model.predict_proba(X = train_features)[:, 1] >= proba, 1, 0)) for proba in probabilities]
        test_metrics_per_proba = [balanced_accuracy_score(y_true = test_labels, y_pred = np.where(model.predict_proba(X = test_features)[:, 1] >= proba, 1, 0)) for proba in probabilities]
        
        # Calculating the balanced accuracy score at default threshold for train and test set
        score_at_default_threshold_train = balanced_accuracy_score(y_true = train_labels, y_pred = model.predict(X = train_features))
        score_at_default_threshold_test = balanced_accuracy_score(y_true = test_labels, y_pred = model.predict(X = test_features))
    elif metric == "positive_precision":
        # Calculating the positive precision score based on given probability thresholds for train and test set
        train_metrics_per_proba = [precision_score(y_true = train_labels, y_pred = np.where(model.predict_proba(X = train_features)[:, 1] >= proba, 1, 0)) for proba in probabilities]
        test_metrics_per_proba = [precision_score(y_true = test_labels, y_pred = np.where(model.predict_proba(X = test_features)[:, 1] >= proba, 1, 0)) for proba in probabilities]
        
        # Calculating the positive precision score at default threshold for train and test set
        score_at_default_threshold_train = precision_score(y_true = train_labels, y_pred = model.predict(X = train_features))
        score_at_default_threshold_test = precision_score(y_true = test_labels, y_pred = model.predict(X = test_features))
    elif metric == "negative_precision":
        # Calculating the negative precision score based on given probability thresholds for train and test set
        train_metrics_per_proba = [precision_score(y_true = train_labels, y_pred = np.where(model.predict_proba(X = train_features)[:, 1] >= proba, 1, 0), pos_label = 0) for proba in probabilities]
        test_metrics_per_proba = [precision_score(y_true = test_labels, y_pred = np.where(model.predict_proba(X = test_features)[:, 1] >= proba, 1, 0), pos_label = 0) for proba in probabilities]
    
        # Calculating the negative precision score at default threshold for train and test set
        score_at_default_threshold_train = precision_score(y_true = train_labels, y_pred = model.predict(X = train_features), pos_label = 0)
        score_at_default_threshold_test = precision_score(y_true = test_labels, y_pred = model.predict(X = test_features), pos_label = 0)
    elif metric == "positive_recall":
        # Calculating the positive recall score based on given probability thresholds for train and test set
        train_metrics_per_proba = [recall_score(y_true = train_labels, y_pred = np.where(model.predict_proba(X = train_features)[:, 1] >= proba, 1, 0)) for proba in probabilities]
        test_metrics_per_proba = [recall_score(y_true = test_labels, y_pred = np.where(model.predict_proba(X = test_features)[:, 1] >= proba, 1, 0)) for proba in probabilities]
        
        # Calculating the positive recall score at default threshold for train and test set
        score_at_default_threshold_train = recall_score(y_true = train_labels, y_pred = model.predict(X = train_features))
        score_at_default_threshold_test = recall_score(y_true = test_labels, y_pred = model.predict(X = test_features))
    elif metric == "negative_recall":
        # Calculating the negative recall score based on given probability thresholds for train and test set
        train_metrics_per_proba = [recall_score(y_true = train_labels, y_pred = np.where(model.predict_proba(X = train_features)[:, 1] >= proba, 1, 0), pos_label = 0) for proba in probabilities]
        test_metrics_per_proba = [recall_score(y_true = test_labels, y_pred = np.where(model.predict_proba(X = test_features)[:, 1] >= proba, 1, 0), pos_label = 0) for proba in probabilities]
        
        # Calculating the negative recall score at default threshold for train and test set
        score_at_default_threshold_train = recall_score(y_true = train_labels, y_pred = model.predict(X = train_features), pos_label = 0)
        score_at_default_threshold_test = recall_score(y_true = test_labels, y_pred = model.predict(X = test_features), pos_label = 0)
    elif metric == "positive_fbeta":
        # Calculating the positive fbeta score based on given probability thresholds for train and test set
        train_metrics_per_proba = [fbeta_score(y_true = train_labels, y_pred = np.where(model.predict_proba(X = train_features)[:, 1] >= proba, 1, 0), beta = beta) for proba in probabilities]
        test_metrics_per_proba = [fbeta_score(y_true = test_labels, y_pred = np.where(model.predict_proba(X = test_features)[:, 1] >= proba, 1, 0), beta = beta) for proba in probabilities]
        
        # Calculating the positive fbeta score at default threshold for train and test set
        score_at_default_threshold_train = fbeta_score(y_true = train_labels, y_pred = model.predict(X = train_features), beta = beta)
        score_at_default_threshold_test = fbeta_score(y_true = test_labels, y_pred = model.predict(X = test_features), beta = beta)
    elif metric == "negative_fbeta":
        # Calculating the negative fbeta score based on given probability thresholds for train and test set
        train_metrics_per_proba = [fbeta_score(y_true = train_labels, y_pred = np.where(model.predict_proba(X = train_features)[:, 1] >= proba, 1, 0), beta = beta, pos_label = 0) for proba in probabilities]
        test_metrics_per_proba = [fbeta_score(y_true = test_labels, y_pred = np.where(model.predict_proba(X = test_features)[:, 1] >= proba, 1, 0), beta = beta, pos_label = 0) for proba in probabilities]
        
        # Calculating the negative fbeta score at default threshold for train and test set
        score_at_default_threshold_train = fbeta_score(y_true = train_labels, y_pred = model.predict(X = train_features), beta = beta, pos_label = 0)
        score_at_default_threshold_test = fbeta_score(y_true = test_labels, y_pred = model.predict(X = test_features), beta = beta, pos_label = 0)
    
    # Identifying the best probability threshold for train & test set
    best_threshold_train = probabilities[np.array(object = train_metrics_per_proba).argmax()]
    best_threshold_test = probabilities[np.array(object = test_metrics_per_proba).argmax()]
    
    # Filtering the best score based on chosen probability thresholds for train and test set
    score_at_best_threshold_train = train_metrics_per_proba[np.array(object = train_metrics_per_proba).argmax()]
    score_at_best_threshold_test = test_metrics_per_proba[np.array(object = test_metrics_per_proba).argmax()]
    
    # Plotting probability thresholding plot for train set
    plt.subplot(1, 2, 1)
    plt.plot(probabilities, train_metrics_per_proba, label = f"{metrics_dict.get(metric)} Score")
    plt.title(label = f"Train Set {metrics_dict.get(metric)} Thresholding", fontsize = 20)
    
    # Creating a condition based on thresholding for train set
    if score_at_best_threshold_train == score_at_default_threshold_train:
        # Drawing a vertical line at default (50%) probability threshold for train set
        plt.axvline(x = 0.5, color = "teal", label = "Best Threshold is Default Threshold (50%)")
        
        # Readdjusting the probability threshold for train set back to the default
        best_threshold_train = 0.5
    else:
        # Drawing vertical lines at both default and best probability thresholds for train set
        plt.axvline(x = 0.5, color = "teal", label = "Default Threshold (50%)")
        plt.axvline(x = best_threshold_train, color = "red", label = f"Best Train Threshold ({best_threshold_train:.0%})")
    
    plt.ylabel(ylabel = f"{metrics_dict.get(metric)} Score", fontsize = 20)
    plt.xlabel(xlabel = "Probability", fontsize = 20)
    plt.legend(loc = "best")
    
    # Plotting probability thresholding plot for test set
    plt.subplot(1, 2, 2)
    plt.plot(probabilities, test_metrics_per_proba, label = f"{metrics_dict.get(metric)} Score")
    plt.title(label = f"Test Set {metrics_dict.get(metric)} Thresholding", fontsize = 20)
    
    # Creating a condition based on thresholding for test set
    if score_at_best_threshold_test == score_at_default_threshold_test:
        # Drawing a vertical line at default (50%) probability threshold for test set
        plt.axvline(x = 0.5, color = "teal", label = "Best Threshold is Default Threshold (50%)")
        
        # Readdjusting the probability threshold for test set back to the default
        best_threshold_test = 0.5
    else:
        # Drawing vertical lines at both default and best probability thresholds for train set
        plt.axvline(x = 0.5, color = "teal", label = "Default Threshold (50%)")
        plt.axvline(x = best_threshold_test, color = "red", label = f"Best Test Threshold ({best_threshold_test:.0%})")
    
    plt.ylabel(ylabel = f"{metrics_dict.get(metric)} Score", fontsize = 20)
    plt.xlabel(xlabel = "Probability", fontsize = 20)
    plt.legend(loc = "best")
    plt.show()
    
    # Returning best probabiltiy threshold for train and test set
    return best_threshold_train, best_threshold_test

# Defining a function to print out the classification report
def print_classification_report(model = None, 
                                train_features = None, 
                                train_labels = None, 
                                test_features = None, 
                                test_labels = None, 
                                train_threshold = None,
                                test_threshold = None,
                                class_labels = ["Loss or Draw", "Win"],
                                algorithm_name = None):
    """
    This function is used to print out a classification report for train & test set.
    
    Args:
        model: A classifier instance.
        train_features: Train features.
        train_labels: Train labels.
        test_features: Test features.
        test_labels: Train labels.
        train_threshold: Probability threshold for train set.
        test_threshold: Probability threshold for test set.
        algorithm_name: A name of an algoritm used to build the model.
        
    Returns:
        Prints out a classification report for train & test set.
    """
    # Creating a condition based on probability thresholds
    if train_threshold is None and test_threshold is None:
        # Unpacking a list to redefine probability thresholds
        train_threshold, test_threshold = [0.5, 0.5]
    else:
        # Passing in case a condition is not satisfied
        pass
    
    # Making predictions on train and test set based on chosen probability thresholds
    train_predictions = np.where(model.predict_proba(X = train_features)[:, 1] >= train_threshold, 1, 0)
    test_predictions = np.where(model.predict_proba(X = test_features)[:, 1] >= test_threshold, 1, 0)
    
    # Creating a classification report for train & test set
    train_report = classification_report(y_true = train_labels, y_pred = train_predictions, target_names = class_labels)
    test_report = classification_report(y_true = test_labels, y_pred = test_predictions, target_names = class_labels)
    
    # Printing out the classification report for train & test sets
    print(f"Classification Report Summary for {algorithm_name} Model:\n")
    print(f"Train report:\n{train_report}\n\n")
    print(f"Test report:\n{test_report}")
    
# Defining a function to plot Receiver Operating Characteristics (ROC) curve
def plot_roc_curve(model = None, 
                   train_features = None, 
                   train_labels = None, 
                   test_features = None, 
                   test_labels = None, 
                   algorithm_name = None):
    """
    This function is used to plot Receiver Operating Characteristics (ROC) curve for train & test set.
    
    Args:
        model: A classifier instance.
        train_features: Train features.
        train_labels: Train labels.
        test_features: Test features.
        test_labels: Train labels.
        algorithm_name: A name of an algoritm used to build the model.
        
    Returns:
        Plots Receiver Operating Characteristics (ROC) curve for train & test set.
    """
    # Calculating Area Under the Curve (AUC) score for train & test set
    auc_score_train = roc_auc_score(y_true = train_labels, y_score = model.predict_proba(X = train_features)[:, 1])
    auc_score_test = roc_auc_score(y_true = test_labels, y_score = model.predict_proba(X = test_features)[:, 1])
    
    # Calculating False Positive Rate (FPR) and True Positive Rate (TPR) for train set
    fpr, tpr, _ = roc_curve(y_true = train_labels, y_score = model.predict_proba(X = train_features)[:, 1])
    
    # Plotting Receiver Operating Characteristics (ROC) curve for train set
    plt.subplot(1, 2, 1)
    plt.plot(fpr, tpr, label = f"{algorithm_name} Model AUC Score: {auc_score_train:.2f}", color = "red")
    plt.plot([0, 1], [0, 1], label = "Random Model", linestyle = "--", color = "teal")
    plt.title(label = "Train Set ROC Curve", fontsize = 20)
    plt.xlabel(xlabel = "False Positive Rate", fontsize = 20)
    plt.ylabel(ylabel = "True Positive Rate", fontsize = 20)
    plt.legend(loc = "lower right", fontsize = 20)
    
    # Calculating False Positive Rate (FPR) and True Positive Rate (TPR) for test set
    fpr, tpr, _ = roc_curve(y_true = test_labels, y_score = model.predict_proba(X = test_features)[:, 1])
    
    # Plotting Receiver Operating Characteristics (ROC) curve for test set
    plt.subplot(1, 2, 2)
    plt.plot(fpr, tpr, label = f"{algorithm_name} Model AUC Score: {auc_score_test:.2f}", color = "red")
    plt.plot([0, 1], [0, 1], label = "Random Model", linestyle = "--", color = "teal")
    plt.title(label = "Test Set ROC Curve", fontsize = 20)
    plt.xlabel(xlabel = "False Positive Rate", fontsize = 20)
    plt.ylabel(ylabel = "True Positive Rate", fontsize = 20)
    plt.legend(loc = "lower right", fontsize = 20)
    plt.show()
    
# Defining a function to plot confusion matrices, recall & precision ratio
def plot_confusion_matrix(model = None, 
                          train_features = None, 
                          test_features = None, 
                          train_labels = None, 
                          test_labels = None,
                          train_threshold = None,
                          test_threshold = None,
                          class_labels = ["Loss or Draw", "Win"]):
    """
    This function is used to plot confusion matrices, recall & precision ratio for train & test set.
    
    Args:
        model: A classifier instance.
        train_features: Train features.
        train_labels: Train labels.
        test_features: Test features.
        test_labels: Train labels.
        train_threshold: Probability threshold for train set.
        test_threshold: Probability threshold for test set.
    
    Returns:
        Plots confusion matrices, recall and precision ratio for train & test set.
    """
    # Creating a condition based on probability thresholds
    if train_threshold is None and test_threshold is None:
        # Unpacking a list to redefine probability thresholds
        train_threshold, test_threshold = [0.5, 0.5]
    else:
        # Passing in case a condition is not satisfied
        pass
    
    # Making predictions on train and test set based on chosen probability thresholds
    train_predictions = np.where(model.predict_proba(X = train_features)[:, 1] >= train_threshold, 1, 0)
    test_predictions = np.where(model.predict_proba(X = test_features)[:, 1] >= test_threshold, 1, 0)
    
    # Creating confusion matrices for train and test set
    cm_train = confusion_matrix(y_true = train_labels, y_pred = train_predictions)
    cm_test = confusion_matrix(y_true = test_labels, y_pred = test_predictions)
    
    # Plotting confusion matrix for train set
    plt.figure(figsize = (30, 18))
    plt.subplot(2, 3, 1)
    sns.heatmap(data = cm_train, cmap = plt.cm.Blues, annot = True, fmt = ".4g", cbar = False, xticklabels = class_labels, yticklabels = class_labels)
    plt.title(label = "Train Set Confusion Matrix", fontsize = 16)
    plt.ylabel(ylabel = "Ground Truth", fontsize = 16)
    plt.xlabel(xlabel = "Predictions", fontsize = 16)
    plt.yticks(fontsize = 16)
    plt.xticks(fontsize = 16)
    
    # Calculating recall ratio for train set
    upper_array = np.divide(cm_train[0], cm_train.sum(axis = 1)[0])
    lower_array = np.divide(cm_train[1], cm_train.sum(axis = 1)[1])
    final_array = np.vstack(tup = (upper_array, lower_array))
    
    # Plotting recall ratio for train set
    plt.subplot(2, 3, 2)
    sns.heatmap(data = final_array, cmap = plt.cm.Blues, annot = True, fmt = ".0%", cbar = False, xticklabels = class_labels, yticklabels = class_labels)
    plt.title(label = "Train Set Recall Ratio", fontsize = 16)
    plt.ylabel(ylabel = "Ground Truth", fontsize = 16)
    plt.xlabel(xlabel = "Predictions", fontsize = 16)
    plt.yticks(fontsize = 16)
    plt.xticks(fontsize = 16)
    
    # Calculating precision ratio for train set
    negative_predictions = np.expand_dims(a = np.divide(cm_train[:, 0], cm_train.sum(axis = 0)[0]), axis = 1)
    positive_predictions = np.expand_dims(a = np.divide(cm_train[:, 1], cm_train.sum(axis = 0)[1]), axis = 1)
    final_array = np.hstack(tup = (negative_predictions, positive_predictions))
    
    # Plotting precision ratio for train set
    plt.subplot(2, 3, 3)
    sns.heatmap(data = final_array, cmap = plt.cm.Blues, annot = True, fmt = ".0%", cbar = False, xticklabels = class_labels, yticklabels = class_labels)
    plt.title(label = "Train Set Precision Ratio", fontsize = 16)
    plt.ylabel(ylabel = "Ground Truth", fontsize = 16)
    plt.xlabel(xlabel = "Predictions", fontsize = 16)
    plt.yticks(fontsize = 16)
    plt.xticks(fontsize = 16)
    
    # Plotting confusion matrix for test set
    plt.subplot(2, 3, 4)
    sns.heatmap(data = cm_test, cmap = plt.cm.Blues, annot = True, fmt = ".4g", cbar = False, xticklabels = class_labels, yticklabels = class_labels)
    plt.title(label = "Test Set Confusion Matrix", fontsize = 16)
    plt.ylabel(ylabel = "Ground Truth", fontsize = 16)
    plt.xlabel(xlabel = "Predictions", fontsize = 16)
    plt.yticks(fontsize = 16)
    plt.xticks(fontsize = 16)
    
    # Calculating recall ratio for test set
    upper_array = np.divide(cm_test[0], cm_test.sum(axis = 1)[0])
    lower_array = np.divide(cm_test[1], cm_test.sum(axis = 1)[1])
    final_array = np.vstack(tup = (upper_array, lower_array))
    
    # Plotting recall ratio for test set
    plt.subplot(2, 3, 5)
    sns.heatmap(data = final_array, cmap = plt.cm.Blues, annot = True, fmt = ".0%", cbar = False, xticklabels = class_labels, yticklabels = class_labels)
    plt.title(label = "Test Set Recall Ratio", fontsize = 16)
    plt.ylabel(ylabel = "Ground Truth", fontsize = 16)
    plt.xlabel(xlabel = "Predictions", fontsize = 16)
    plt.yticks(fontsize = 16)
    plt.xticks(fontsize = 16)
    
    # Calculating precision ratio for test set
    negative_predictions = np.expand_dims(a = np.divide(cm_test[:, 0], cm_test.sum(axis = 0)[0]), axis = 1)
    positive_predictions = np.expand_dims(a = np.divide(cm_test[:, 1], cm_test.sum(axis = 0)[1]), axis = 1)
    final_array = np.hstack(tup = (negative_predictions, positive_predictions))
    
    # Plotting precision ratio for test set
    plt.subplot(2, 3, 6)
    sns.heatmap(data = final_array, cmap = plt.cm.Blues, annot = True, fmt = ".0%", cbar = False, xticklabels = class_labels, yticklabels = class_labels)
    plt.title(label = "Test Set Precision Ratio", fontsize = 16)
    plt.ylabel(ylabel = "Ground Truth", fontsize = 16)
    plt.xlabel(xlabel = "Predictions", fontsize = 16)
    plt.yticks(fontsize = 16)
    plt.xticks(fontsize = 16)
    plt.show()
    
# Defining a function to evaluate the performance of a classifier
def evaluate_model_performance(model = None, 
                               train_features = None, 
                               train_labels = None, 
                               test_features = None, 
                               test_labels = None, 
                               algorithm_name = None, 
                               beta = 1,
                               train_threshold = None,
                               test_threshold = None):
    """
    Args:
        model: A classifier instance.
        train_features: Train features.
        train_labels: Train labels.
        test_features: Test features.
        test_labels: Train labels.
        algorithm_name: A name of an algoritm used to build the model.
        beta: Beta to calculate F Beta score.
        train_threshold: Probability threshold for train set.
        test_threshold: Probability threshold for test set.
        
    Returns:
        A pandas data frame.
    """
    # Creating a condition based on probability thresholds
    if train_threshold is None and test_threshold is None:
        # Unpacking a list to redefine probability thresholds
        train_threshold, test_threshold = [0.5, 0.5]
    else:
        # Passing in case a condition is not satisfied
        pass
    
    # Making predictions on train and test set based on chosen probability thresholds
    train_predictions = np.where(model.predict_proba(X = train_features)[:, 1] >= train_threshold, 1, 0)
    test_predictions = np.where(model.predict_proba(X = test_features)[:, 1] >= test_threshold, 1, 0)
    
    # Calculating confusion matrix for train and test set
    cm_train = confusion_matrix(y_true = train_labels, y_pred = train_predictions)
    cm_test = confusion_matrix(y_true = test_labels, y_pred = test_predictions)
    
    # Calculating TPs, FPs, TNs, and FNs for train set
    TP_train = cm_train[1][1]
    TN_train = cm_train[0][0]
    FP_train = cm_train[0][1]
    FN_train = cm_train[1][0]
    
    # Calculating TPs, FPs, TNs, and FNs for test set
    TP_test = cm_test[1][1]
    TN_test = cm_test[0][0]
    FP_test = cm_test[0][1]
    FN_test = cm_test[1][0]
    
    # Calculating the sensitivity and specificity for train set
    sensitivity_train = TP_train / (TP_train + FN_train)
    specificity_train = TN_train / (TN_train + FP_train)
    
    # Calculating the sensitivity and specificity for test set
    sensitivity_test = TP_test / (TP_test + FN_test)
    specificity_test = TN_test / (TN_test + FP_test)
    
    # Evaluating the performance of the model based on evaluation metrics for a classification problem
    mcc = round(number = ((TP_test * TN_test) - (FP_test * FN_test)) / 
                np.sqrt((TP_test + FP_test) * (TP_test + FN_test) * (TN_test + FP_test) * (TN_test + FN_test)), ndigits = 2)
    brier_loss = round(number = sum(pow(base = test_labels - model.predict_proba(X = test_features)[:, 1], exp = 2)) / test_labels.shape[0], ndigits = 2)
    auc_train = round(number = roc_auc_score(y_true = train_labels, y_score = model.predict_proba(X = train_features)[:, 1]), ndigits = 2)
    auc_test = round(number = roc_auc_score(y_true = test_labels, y_score = model.predict_proba(X = test_features)[:, 1]), ndigits = 2)
    accuracy = round(number = (TP_test + TN_test) / (TP_test + TN_test + FP_test + FN_test), ndigits = 2)
    balanced_accuracy_train = round(number = (sensitivity_train + specificity_train) / 2, ndigits = 2)
    balanced_accuracy_test = round(number = (sensitivity_test + specificity_test) / 2, ndigits = 2)
    precision = round(number = TP_test / (TP_test + FP_test), ndigits = 2)
    recall = round(number = TP_test / (TP_test + FN_test), ndigits = 2)
    f_beta = round(number = ((1 + (beta ** 2)) * precision * recall) / (((beta ** 2) * precision) + recall), ndigits = 2)
    
    # In case a classifier instance contains multiple estimators
    try:
        # Extracting the number of features
        n_features = model[:-1].transform(X = test_features).shape[1]
    except:
        # Extracting the estimator names from the model
        estimator_names = list(model.named_estimators_.keys())
        
        # Extracting the number of features
        n_features = round(number = sum([model.named_estimators_.get(i)[:-1].transform(X = test_features).shape[1] for i in estimator_names]) / len(estimator_names))
    
    # Creating a dictionary of evaluation metrics for a classification problem
    data_dictionary = {"Train AUC": auc_train,
                       "Test AUC": auc_test,
                       "Train Balanced Accuracy": balanced_accuracy_train, 
                       "Test Balanced Accuracy": balanced_accuracy_test, 
                       "Accuracy": accuracy, 
                       "Precision": precision, 
                       "Recall": recall, 
                       f"F{beta}": f_beta, 
                       "MCC": mcc,
                       "Brier Loss": brier_loss, 
                       "N Features": n_features,
                       "Pipeline": model}
    
    # Creating a pandas data frame to store evaluation metrics for the model
    summary_df = pd.DataFrame(data = data_dictionary, index = [algorithm_name])
    
    # Returning the summary for evaluation metrics
    return summary_df

# Defining a function to generate input data
def generate_input_data(match_dates = None, 
                        home_teams = None, 
                        away_teams = None,
                        unprocessed_data = None):
    
    # Creating a list of week days based on match date 
    weekdays = [match_date.weekday() + 1 for match_date in match_dates]
    
    # Creating a list of months based on match date 
    months = [match_date.month for match_date in match_dates]
    
    # Creating a list of days based on match date 
    days = [match_date.day for match_date in match_dates]
    
    # Extracting the season
    season = unprocessed_data.season.unique()[0]
    
    # Defining the match week
    match_week = unprocessed_data.match_week.max() + 1
    
    # Creating a dictionary of preliminary variables
    data_dictionary = {"season": season,
                       "home_team": home_teams, 
                       "away_team": away_teams,
                       "match_week": match_week,
                       "match_date": match_dates, 
                       "month": months,
                       "day": days,
                       "weekday": weekdays}
    
    # Converting dictionary into data frame
    input_df = pd.DataFrame(data = data_dictionary)
    
    # Extending the data frame with post-match variables
    input_df = input_df.merge(right = unprocessed_data, how = "left")
    
    # Reallocating the columns
    input_df = input_df[unprocessed_data.columns.tolist()]
    
    # Concatenating the input data frame with unprocessed data frame vertically
    input_df = pd.concat(objs = [input_df, unprocessed_data], ignore_index = True)
    
    # Sorting the input data frame by match date in descending order
    input_df = input_df.sort_values(by = "match_date", ascending = False).reset_index(drop = True)
    
    # Calling the function to apply feature engineering to calculate features
    input_df = apply_feature_engineering(data_frame = input_df)
    
    # Sorting the matches by match date in ascending order 
    input_df = input_df.loc[input_df.match_week == match_week].sort_values(by = "match_date").reset_index(drop = True)
    
    # Returning input data frame
    return input_df

# Defining a function to make predictions
def evaluate_engine_performance(input_df = None, 
                                upper_confidence_level = 0.65,
                                predict_upcoming_matches = False):
    """
    This is a function to evaluate the performance of the engine.
    
    Args:
        input_df: An input data frame
        upper_confidence_level: An upper confidence level for engine predictions
        predict_upcoming_matches: Whether or not to make predictions for the upcoming matches
        
    Returns:
        A pandas data frame.
    """
    # Copying the input data frame
    data_frame = input_df.copy()
    
    # Calculating the lower confidence level
    lower_confidence_level = upper_confidence_level - 0.15
    
    # Creating a list of class indices
    class_indices = [-1, 0, 1]
    
    # Creating inpute features for each of the model
    loss_features = data_frame.drop(columns = LOSS_TARGET)
    draw_features = data_frame.drop(columns = DRAW_TARGET)
    win_features = data_frame.drop(columns = WIN_TARGET)
    
    # Creating ground truth for each of the model
    loss_labels = data_frame[LOSS_TARGET]
    draw_labels = data_frame[DRAW_TARGET]
    win_labels = data_frame[WIN_TARGET]
    
    # Calculating the probabilities for the positive class
    loss_probas = loss_model.predict_proba(X = loss_features)[:, 1]
    draw_probas = draw_model.predict_proba(X = draw_features)[:, 1]
    win_probas = win_model.predict_proba(X = win_features)[:, 1]
    
    # Expanding the dimensions of the probability arrays
    loss_probas = np.expand_dims(a = loss_probas, axis = 1)
    draw_probas = np.expand_dims(a = draw_probas, axis = 1)
    win_probas = np.expand_dims(a = win_probas, axis = 1)
    
    # Horizontally stacking the probability arrays
    probabilities = np.hstack(tup = (loss_probas, draw_probas, win_probas))
    
    # Decoding probabilities into class indices
    engine_predictions = [class_indices[i] for i in probabilities.argmax(axis = 1)]
    
    # Extracting the probability for the most likely class
    engine_probabilities = [round(number = probas[probas.argmax()], ndigits = 2) for probas in probabilities]
    
    # Creating new columns to store predictions and probabilities
    data_frame["prediction"] = engine_predictions
    data_frame["probability"] = engine_probabilities
    
    # Creating a new column called bet to filter matches to which engine suggested making a bet
    data_frame["bet"] = np.where(data_frame.probability >= upper_confidence_level, True, False)
    
    # Creating a new column called confidence to display the confidence for each of engine prediction
    data_frame["confidence"] = np.select(condlist = [data_frame.probability >= upper_confidence_level, data_frame.probability < lower_confidence_level], 
                                         choicelist = ["High", "Low"], 
                                         default = "Medium")
    
    # Creating a new column called output to display the engine output based on a prediction
    data_frame["output"] = ''
    
    # Creating outputs based on engine prediction
    loss_outputs = data_frame.loc[data_frame.prediction == -1][["home_team", "away_team", "probability"]].\
    apply(lambda x: f"Probability of {x[1]} defeating {x[0]} away from home is {x[2]:.0%}.", axis = 1)
    draw_outputs = data_frame.loc[data_frame.prediction == 0][["home_team", "away_team", "probability"]].\
    apply(lambda x: f"Probability of {x[0]} and {x[1]} sharing points is {x[2]:.0%}.", axis = 1)
    win_outputs = data_frame.loc[data_frame.prediction == 1][["home_team", "away_team", "probability"]].\
    apply(lambda x: f"Probability of {x[0]} beating {x[1]} at home is {x[2]:.0%}.", axis = 1)
    
    # Assigning the values to the output column
    data_frame.loc[data_frame.prediction == -1, "output"] = loss_outputs
    data_frame.loc[data_frame.prediction == 0, "output"] = draw_outputs
    data_frame.loc[data_frame.prediction == 1, "output"] = win_outputs
    
    # Defining a path to store the engine predictions
    target_path = "/Users/kzeynalzade/Documents/EPL Redevelopment/epl_engine/Data/Predictions data"
    
    # Defining the name for the previous match week predictions
    filename = f"match_week_{data_frame.match_week.unique()[0] - 1}_predictions.csv"
    
    # Creating a condition in case the previous match week predictions exists in the specified folder
    if filename in os.listdir(path = target_path):
        # Creating the filepath
        filepath = os.path.join(target_path, filename)
        
        # Removing the file
        os.remove(path = filepath)
        
        # Creating an assertion to make sure that the file has been removed successfully
        assert filename not in os.listdir(path = target_path)
    else:
        # Passing in case the condition is not satisfied
        pass
    
    # Creating a condition based on the output columns
    if not predict_upcoming_matches:
        # Creating a list of columns
        output_columns = ["season", "match_week", "match_date", "home_team", "away_team", "goals_h", "goals_a", 
                          "prediction", "probability", "confidence", "output", "bet", "ground_truth"]
    else:
        # Removing ground truth, goals_h, goals_a, and ground_truth variables from the list in case the condition is not satisfied
        output_columns = ["season", "match_week", "match_date", "home_team", "away_team",
                          "prediction", "probability", "confidence", "output", "bet"]
        
        # Asserting the number of unique match weeks to be equal to one
        assert data_frame.match_week.nunique() == 1
        
        # Defining a filename for upcoming match week
        upcoming_match_predictions = f"match_week_{data_frame.match_week.unique()[0]}_predictions.csv"
        
        # Creating the filepath
        predictions_filepath = os.path.join(target_path, upcoming_match_predictions)
        
        # Writing the weekly engine predictions to a separate csv
        data_frame[output_columns].to_csv(path_or_buf = predictions_filepath, index = False)
        
    
    # Selecting only output columns
    data_frame = data_frame[output_columns]
    
    # Returning the data frame
    return data_frame