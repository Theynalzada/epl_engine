# Importing Dependencies
import pandas as pd
import epl_metrics
import warnings

# Filtering warnings
warnings.filterwarnings(action = "ignore")
    
# Loading the unprocessed data of the current season
current_season_df = pd.read_csv(filepath_or_buffer = "/Users/kzeynalzade/Documents/EPL Redevelopment/epl_engine/Data/Unprocessed data/2022-23_unprocessed.csv")

# Casting the data type of match_date variable from object to datetime
current_season_df.match_date = pd.to_datetime(arg = current_season_df.match_date, yearfirst = True)

# Creating a list of match dates
dates = pd.to_datetime(arg = ("2022-12-26 " * 6).strip().split() + ("2022-12-27 " * 2).strip().split() + ["2022-12-27", "2022-12-28"], yearfirst = True)

# Creating a list of home teams
home_teams = ["Brentford", "Crystal Palace", "Everton", "Leicester", "Southampton", "Aston Villa", "Arsenal", "Chelsea", "Man Utd", "Leeds"]

# Creating a list of away teams
away_teams = ["Spurs", "Fulham", "Wolves", "Newcastle", "Brighton", "Liverpool", "West Ham", "Bournemouth", "Nott'm Forest", "Man City"]

# Running the script
if __name__ == "__main__":
    # Calling the function to generate input data
    input_data = epl_metrics.generate_input_data(match_dates = dates,
                                                 home_teams = home_teams,
                                                 away_teams = away_teams,
                                                 unprocessed_data = current_season_df)
    
    # Calling the function to make predictions using the engine
    epl_metrics.evaluate_engine_performance(input_df = input_data, 
                                            predict_upcoming_matches = True)