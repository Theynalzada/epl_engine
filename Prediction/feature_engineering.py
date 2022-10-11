# Importing Dependencies
import pandas as pd
import numpy as np
import warnings
import yaml
import os

# Filtering the warnings
warnings.filterwarnings(action = 'ignore')

def load_credentials(filename = None):
    """
    This is a function that will load credentials from a yaml file.
    
    Args:
        filename: A yaml file that contains credentials.
        
    Returns:
        A dictionary object.
    """
    with open(file = filename) as yaml_file:
        config = yaml.safe_load(stream = yaml_file)
        
    return config

config = load_credentials(filename = '/Users/kzeynalzade/Documents/Project/Configuration/config.yml')

def create_preliminary_variables(data_frame = None, season = None):
    """
    This is a function that will create preliminary features which will
    then be used to create other features.
    
    Args:
        data_frame: Pandas data frame.
        
    Return:
        Pandas data frame.
    """
    FINISHED_IN_TOP_4_LAST_SEASON = config.get(season).get('finished_in_top_4_last_season')
    WON_CARABAO_CUP_LAST_SEASON = config.get(season).get('won_carabao_cup_last_season')
    WON_FA_CUP_LAST_SEASON = config.get(season).get('won_fa_cup_last_season')
    WAS_IN_UCL_LAST_SEASON = config.get(season).get('was_in_ucl_last_season')
    WAS_IN_UEL_LAST_SEASON = config.get(season).get('was_in_uel_last_season')
    IS_IN_UCL_THIS_SEASON = config.get(season).get('is_in_ucl_this_season')
    IS_IN_UEL_THIS_SEASON = config.get(season).get('is_in_uel_this_season')
    TRADITIONAL_TOP_6 = config.get(season).get('traditional_top_6')
    REIGNING_CHAMPION = config.get(season).get('reigning_champion')
    PROMOTED_TEAMS = config.get(season).get('promoted_teams')
    BOXING_DAY = config.get(season).get('boxing_day')
    
    data_frame.match_date = pd.to_datetime(arg = data_frame.match_date, yearfirst = True)
    
    data_frame['ground_truth'] = np.nan
    data_frame['result_h'] = ''
    data_frame['result_a'] = ''
    data_frame['points_h'] = 0
    data_frame['points_a'] = 0
    
    data_frame['is_boxing_day'] = np.where((data_frame.match_date.dt.month == 12) & (data_frame.match_date.dt.day == BOXING_DAY), 1, 0)
    data_frame['finished_top_4_last_season_h'] = np.where(data_frame.home_team.isin(values = FINISHED_IN_TOP_4_LAST_SEASON), 1, 0)
    data_frame['finished_top_4_last_season_a'] = np.where(data_frame.away_team.isin(values = FINISHED_IN_TOP_4_LAST_SEASON), 1, 0)
    data_frame['won_carabao_cup_last_season_h'] = np.where(data_frame.home_team == WON_CARABAO_CUP_LAST_SEASON, 1, 0)
    data_frame['won_carabao_cup_last_season_a'] = np.where(data_frame.away_team == WON_CARABAO_CUP_LAST_SEASON, 1, 0)
    data_frame['was_in_ucl_last_season_h'] = np.where(data_frame.home_team.isin(values = WAS_IN_UCL_LAST_SEASON), 1, 0)
    data_frame['was_in_ucl_last_season_a'] = np.where(data_frame.away_team.isin(values = WAS_IN_UCL_LAST_SEASON), 1, 0)
    data_frame['was_in_uel_last_season_h'] = np.where(data_frame.home_team.isin(values = WAS_IN_UEL_LAST_SEASON), 1, 0)
    data_frame['was_in_uel_last_season_a'] = np.where(data_frame.away_team.isin(values = WAS_IN_UEL_LAST_SEASON), 1, 0)
    data_frame['is_in_ucl_this_season_h'] = np.where(data_frame.home_team.isin(values = IS_IN_UCL_THIS_SEASON), 1, 0)
    data_frame['is_in_ucl_this_season_a'] = np.where(data_frame.away_team.isin(values = IS_IN_UCL_THIS_SEASON), 1, 0)
    data_frame['is_in_uel_this_season_h'] = np.where(data_frame.home_team.isin(values = IS_IN_UEL_THIS_SEASON), 1, 0)
    data_frame['is_in_uel_this_season_a'] = np.where(data_frame.away_team.isin(values = IS_IN_UEL_THIS_SEASON), 1, 0)
    data_frame['won_fa_cup_last_season_h'] = np.where(data_frame.home_team == WON_FA_CUP_LAST_SEASON, 1, 0)
    data_frame['won_fa_cup_last_season_a'] = np.where(data_frame.away_team == WON_FA_CUP_LAST_SEASON, 1, 0)
    data_frame['traditional_top_6_h'] = np.where(data_frame.home_team.isin(values = TRADITIONAL_TOP_6), 1, 0)
    data_frame['traditional_top_6_a'] = np.where(data_frame.away_team.isin(values = TRADITIONAL_TOP_6), 1, 0)
    data_frame['won_epl_last_season_h'] = np.where(data_frame.home_team == REIGNING_CHAMPION, 1, 0)
    data_frame['won_epl_last_season_a'] = np.where(data_frame.away_team == REIGNING_CHAMPION, 1, 0)
    data_frame['newly_promoted_h'] = np.where(data_frame.home_team.isin(values = PROMOTED_TEAMS), 1, 0)
    data_frame['newly_promoted_a'] = np.where(data_frame.away_team.isin(values = PROMOTED_TEAMS), 1, 0)
    
    data_frame['home_win'] = np.where(data_frame.goals_h > data_frame.goals_a, 1, 0)
    data_frame['away_win'] = np.where(data_frame.goals_a > data_frame.goals_h, 1, 0)
    data_frame['draw'] = np.where(data_frame.goals_h == data_frame.goals_a, 1, 0)

    data_frame.loc[data_frame.goals_h < data_frame.goals_a, 'result_h'] = 'defeat'
    data_frame.loc[data_frame.goals_h == data_frame.goals_a, 'result_h'] = 'draw'
    data_frame.loc[data_frame.goals_h > data_frame.goals_a, 'result_h'] = 'win'

    data_frame.loc[data_frame.result_h == 'win', 'result_a'] = 'defeat'
    data_frame.loc[data_frame.result_h == 'defeat', 'result_a'] = 'win'
    data_frame.loc[data_frame.result_h == 'draw', 'result_a'] = 'draw'
    
    data_frame.loc[data_frame.result_h == 'defeat', 'ground_truth'] = -1
    data_frame.loc[data_frame.result_h == 'draw', 'ground_truth'] = 0
    data_frame.loc[data_frame.result_h == 'win', 'ground_truth'] = 1

    data_frame.loc[data_frame.result_h == 'draw', 'points_h'] = 1
    data_frame.loc[data_frame.result_h == 'win', 'points_h'] = 3

    data_frame.loc[data_frame.result_a == 'draw', 'points_a'] = 1
    data_frame.loc[data_frame.result_a == 'win', 'points_a'] = 3
    
    return data_frame

def create_cumulative_goals_scored_h(data_frame = None):
    """
    This is a function that will create a variable based on the 
    cumulative sum of goals scored by home team in home mathces.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame with the new variable.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['goals_scored_h_cum'] = np.nan
    goals_scored = {}
    
    for team in teams:
        goals = data_frame.loc[data_frame.home_team == team, 'goals_h'].tolist() + [0]
        goals = np.cumsum(goals[::-1][:-1])[::-1].tolist()
        goals_scored.update({team:goals})
        cumulative_sum_of_goals_scored = goals_scored.get(team)
        data_frame.loc[data_frame.home_team == team, 'goals_scored_h_cum'] = cumulative_sum_of_goals_scored
        
    data_frame.goals_scored_h_cum = data_frame.goals_scored_h_cum.apply(func = lambda x: int(x))
    
    return data_frame

def create_cumulative_goals_scored_a(data_frame = None):
    """
    This is a function that will create a variable based on the 
    cumulative sum of goals scored by away team in away matches.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame with the new variable.
    """
    teams = data_frame.away_team.unique().tolist()
    data_frame['goals_scored_a_cum'] = np.nan
    goals_scored = {}
    
    for team in teams:
        goals = data_frame.loc[data_frame.away_team == team, 'goals_a'].tolist() + [0]
        goals = np.cumsum(goals[::-1][:-1])[::-1].tolist()
        goals_scored.update({team:goals})
        cumulative_sum_of_goals_scored = goals_scored.get(team)
        data_frame.loc[data_frame.away_team == team, 'goals_scored_a_cum'] = cumulative_sum_of_goals_scored
        
    data_frame.goals_scored_a_cum = data_frame.goals_scored_a_cum.apply(func = lambda x: int(x))
    
    return data_frame

def create_cumulative_points_h(data_frame = None):
    """
    This is a function that will create a variable based on the 
    cumulative sum of points accumulated by home team in home matches.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame with the new variable.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['points_h_cum'] = np.nan
    points_accumulated = {}
    
    for team in teams:
        points = data_frame.loc[data_frame.home_team == team, 'points_h'].tolist() + [0]
        points = np.cumsum(points[::-1][:-1])[::-1].tolist()
        points_accumulated.update({team:points})
        cumulative_sum_of_points = points_accumulated.get(team)
        data_frame.loc[data_frame.home_team == team, 'points_h_cum'] = cumulative_sum_of_points
        
    data_frame.points_h_cum = data_frame.points_h_cum.apply(func = lambda x: int(x))
    
    return data_frame

def create_cumulative_points_a(data_frame = None):
    """
    This is a function that will create a variable based on the 
    cumulative sum of points accumulated by away team in away matches.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame with the new variable.
    """
    teams = data_frame.away_team.unique().tolist()
    data_frame['points_a_cum'] = np.nan
    points_accumulated = {}
    
    for team in teams:
        points = data_frame.loc[data_frame.away_team == team, 'points_a'].tolist() + [0]
        points = np.cumsum(points[::-1][:-1])[::-1].tolist()
        points_accumulated.update({team:points})
        cumulative_sum_of_points = points_accumulated.get(team)
        data_frame.loc[data_frame.away_team == team, 'points_a_cum'] = cumulative_sum_of_points
        
    data_frame.points_a_cum = data_frame.points_a_cum.apply(func = lambda x: int(x))
    
    return data_frame

def create_cumulative_goals_conceded_h(data_frame = None):
    """
    This is a function that will create a variable based on the 
    cumulative sum of goals conceded by home team in home matches.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame with the new variable.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['goals_conceded_h_cum'] = np.nan
    goals_conceded = {}
    
    for team in teams:
        goals = data_frame.loc[data_frame.home_team == team, 'goals_a'].tolist() + [0]
        goals = np.cumsum(goals[::-1][:-1])[::-1].tolist()
        goals_conceded.update({team:goals})
        cumulative_sum_of_goals = goals_conceded.get(team)
        data_frame.loc[data_frame.home_team == team, 'goals_conceded_h_cum'] = cumulative_sum_of_goals
        
    data_frame.goals_conceded_h_cum = data_frame.goals_conceded_h_cum.apply(func = lambda x: int(x))
    
    return data_frame

def create_cumulative_goals_conceded_a(data_frame = None):
    """
    This is a function that will create a variable based on the 
    cumulative sum of goals conceded by away team in away matches.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame with the new variable.
    """
    teams = data_frame.away_team.unique().tolist()
    data_frame['goals_conceded_a_cum'] = np.nan
    goals_conceded = {}
    
    for team in teams:
        goals = data_frame.loc[data_frame.away_team == team, 'goals_h'].tolist() + [0]
        goals = np.cumsum(goals[::-1][:-1])[::-1].tolist()
        goals_conceded.update({team:goals})
        cumulative_sum_of_goals = goals_conceded.get(team)
        data_frame.loc[data_frame.away_team == team, 'goals_conceded_a_cum'] = cumulative_sum_of_goals
        
    data_frame.goals_conceded_a_cum = data_frame.goals_conceded_a_cum.apply(func = lambda x: int(x))
    
    return data_frame

def create_cumulative_possession_h(data_frame = None):
    """
    This is a function that will calculate the cumulative average possesion for a home team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['avg_possession_h'] = np.nan
    
    for team in teams:
        possession = data_frame.loc[data_frame.home_team == team, 'possession_h'].to_numpy()[::-1][:-1]
        possession = [50.0] + [round(number = np.mean(possession[:x]), ndigits = 1) for x in range(1, len(possession) + 1)]
        possession = possession[::-1]
        
        data_frame.loc[data_frame.home_team == team, 'avg_possession_h'] = possession
        
    return data_frame

def create_cumulative_possession_a(data_frame = None):
    """
    This is a function that will calculate the cumulative average possesion for an away team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.away_team.unique().tolist()
    data_frame['avg_possession_a'] = np.nan

    for team in teams:
        possession = data_frame.loc[data_frame.away_team == team, 'possession_a'].to_numpy()[::-1][:-1]
        possession = [50.0] + [round(number = np.mean(possession[:x]), ndigits = 1) for x in range(1, len(possession) + 1)]
        possession = possession[::-1]
        
        data_frame.loc[data_frame.away_team == team, 'avg_possession_a'] = possession
        
    return data_frame

def create_goal_difference(data_frame = None):
    """
    This is a function that will create two new variables based on home and away goal difference.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    data_frame['positive_total_goal_difference_h'] = np.where(data_frame.total_goals_scored_h > data_frame.total_goals_conceded_h, 1, 0)
    data_frame['positive_total_goal_difference_a'] = np.where(data_frame.total_goals_scored_a > data_frame.total_goals_conceded_a, 1, 0)
    data_frame['positive_goal_difference_h'] = np.where(data_frame.goals_scored_h_cum > data_frame.goals_conceded_h_cum, 1, 0)
    data_frame['positive_goal_difference_a'] = np.where(data_frame.goals_scored_a_cum > data_frame.goals_conceded_a_cum, 1, 0)
    data_frame['total_goal_difference_h'] = np.subtract(data_frame.total_goals_scored_h, data_frame.total_goals_conceded_h)
    data_frame['total_goal_difference_a'] = np.subtract(data_frame.total_goals_scored_a, data_frame.total_goals_conceded_a)
    data_frame['goal_difference_h'] = np.subtract(data_frame.goals_scored_h_cum, data_frame.goals_conceded_h_cum)
    data_frame['goal_difference_a'] = np.subtract(data_frame.goals_scored_a_cum, data_frame.goals_conceded_a_cum)
    
    return data_frame

def create_derbies(data_frame = None):
    """
    This is a function that will create two new variables, one indicating whether or not a match is a derby (derbies between major clubs)
    and the other one indicating which derby it is. 
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    data_frame['is_derby'] = 0
    data_frame['derby_name'] = 'No Derby'
    data_frame.loc[(data_frame.home_team == 'Arsenal') & (data_frame.away_team == 'Chelsea'), ['is_derby', 'derby_name']] = [1, 'North West London']
    data_frame.loc[(data_frame.home_team == 'Chelsea') & (data_frame.away_team == 'Arsenal'), ['is_derby', 'derby_name']] = [1, 'North West London']
    data_frame.loc[(data_frame.home_team == 'Chelsea') & (data_frame.away_team == 'Spurs'), ['is_derby', 'derby_name']] = [1, 'North West London']
    data_frame.loc[(data_frame.home_team == 'Spurs') & (data_frame.away_team == 'Chelsea'), ['is_derby', 'derby_name']] = [1, 'North West London']
    data_frame.loc[(data_frame.home_team == 'Liverpool') & (data_frame.away_team == 'Everton'), ['is_derby', 'derby_name']] = [1, 'Merseyside']
    data_frame.loc[(data_frame.home_team == 'Everton') & (data_frame.away_team == 'Liverpool'), ['is_derby', 'derby_name']] = [1, 'Merseyside']
    data_frame.loc[(data_frame.home_team == 'Man Utd') & (data_frame.away_team == 'Liverpool'), ['is_derby', 'derby_name']] = [1, 'North West']
    data_frame.loc[(data_frame.home_team == 'Liverpool') & (data_frame.away_team == 'Man Utd'), ['is_derby', 'derby_name']] = [1, 'North West']
    data_frame.loc[(data_frame.home_team == 'Man Utd') & (data_frame.away_team == 'Man City'), ['is_derby', 'derby_name']] = [1, 'Manchester']
    data_frame.loc[(data_frame.home_team == 'Man City') & (data_frame.away_team == 'Man Utd'), ['is_derby', 'derby_name']] = [1, 'Manchester']
    data_frame.loc[(data_frame.home_team == 'Arsenal') & (data_frame.away_team == 'Spurs'), ['is_derby', 'derby_name']] = [1, 'North London']
    data_frame.loc[(data_frame.home_team == 'Spurs') & (data_frame.away_team == 'Arsenal'), ['is_derby', 'derby_name']] = [1, 'North London']
    data_frame.loc[(data_frame.home_team == 'Man Utd') & (data_frame.away_team == 'Leeds'), ['is_derby', 'derby_name']] = [1, 'Roses']
    data_frame.loc[(data_frame.home_team == 'Leeds') & (data_frame.away_team == 'Man Utd'), ['is_derby', 'derby_name']] = [1, 'Roses']
    
    return data_frame

def create_cumulative_shots_on_target_h(data_frame = None):
    """
    This is a function that will calculate the cumulative shots on target for a home team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['avg_shots_on_target_h'] = np.nan
    
    for team in teams:
        shots_on_target = data_frame.loc[data_frame.home_team == team, 'shots_on_target_h'].to_numpy()[::-1][:-1]
        shots_on_target = [0.0] + [round(number = np.mean(shots_on_target[:x]), ndigits = 1) for x in range(1, len(shots_on_target) + 1)]
        shots_on_target = shots_on_target[::-1]
        
        data_frame.loc[data_frame.home_team == team, 'avg_shots_on_target_h'] = shots_on_target
        
    return data_frame

def create_cumulative_shots_on_target_a(data_frame = None):
    """
    This is a function that will calculate the cumulative shots on target for an away team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.away_team.unique().tolist()
    data_frame['avg_shots_on_target_a'] = np.nan
    
    for team in teams:
        shots_on_target = data_frame.loc[data_frame.away_team == team, 'shots_on_target_a'].to_numpy()[::-1][:-1]
        shots_on_target = [0.0] + [round(number = np.mean(shots_on_target[:x]), ndigits = 1) for x in range(1, len(shots_on_target) + 1)]
        shots_on_target = shots_on_target[::-1]
        
        data_frame.loc[data_frame.away_team == team, 'avg_shots_on_target_a'] = shots_on_target
        
    return data_frame

def create_cumulative_shots_h(data_frame = None):
    """
    This is a function that will calculate the cumulative shots for a home team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['avg_shots_h'] = np.nan
    
    for team in teams:
        shots = data_frame.loc[data_frame.home_team == team, 'shots_h'].to_numpy()[::-1][:-1]
        shots = [0.0] + [round(number = np.mean(shots[:x]), ndigits = 1) for x in range(1, len(shots) + 1)]
        shots = shots[::-1]
        
        data_frame.loc[data_frame.home_team == team, 'avg_shots_h'] = shots
        
    return data_frame

def create_cumulative_shots_a(data_frame = None):
    """
    This is a function that will calculate the cumulative shots for an away team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.away_team.unique().tolist()
    data_frame['avg_shots_a'] = np.nan
    
    for team in teams:
        shots = data_frame.loc[data_frame.away_team == team, 'shots_a'].to_numpy()[::-1][:-1]
        shots = [0.0] + [round(number = np.mean(shots[:x]), ndigits = 1) for x in range(1, len(shots) + 1)]
        shots = shots[::-1]
        
        data_frame.loc[data_frame.away_team == team, 'avg_shots_a'] = shots
        
    return data_frame

def create_cumulative_touches_h(data_frame = None):
    """
    This is a function that will calculate the cumulative touches for a home team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['avg_touches_h'] = np.nan
    
    for team in teams:
        touches = data_frame.loc[data_frame.home_team == team, 'touches_h'].to_numpy()[::-1][:-1]
        touches = [0.0] + [round(number = np.mean(touches[:x]), ndigits = 1) for x in range(1, len(touches) + 1)]
        touches = touches[::-1]
        
        data_frame.loc[data_frame.home_team == team, 'avg_touches_h'] = touches
        
    return data_frame

def create_cumulative_touches_a(data_frame = None):
    """
    This is a function that will calculate the cumulative touches for an away team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.away_team.unique().tolist()
    data_frame['avg_touches_a'] = np.nan
    
    for team in teams:
        touches = data_frame.loc[data_frame.away_team == team, 'touches_a'].to_numpy()[::-1][:-1]
        touches = [0.0] + [round(number = np.mean(touches[:x]), ndigits = 1) for x in range(1, len(touches) + 1)]
        touches = touches[::-1]
        
        data_frame.loc[data_frame.away_team == team, 'avg_touches_a'] = touches
        
    return data_frame

def create_cumulative_passes_h(data_frame = None):
    """
    This is a function that will calculate the cumulative passes for a home team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['avg_passes_h'] = np.nan
    
    for team in teams:
        passes = data_frame.loc[data_frame.home_team == team, 'passes_h'].to_numpy()[::-1][:-1]
        passes = [0.0] + [round(number = np.mean(passes[:x]), ndigits = 1) for x in range(1, len(passes) + 1)]
        passes = passes[::-1]
        
        data_frame.loc[data_frame.home_team == team, 'avg_passes_h'] = passes
        
    return data_frame

def create_cumulative_passes_a(data_frame = None):
    """
    This is a function that will calculate the cumulative passes for an away team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.away_team.unique().tolist()
    data_frame['avg_passes_a'] = np.nan
    
    for team in teams:
        passes = data_frame.loc[data_frame.away_team == team, 'passes_a'].to_numpy()[::-1][:-1]
        passes = [0.0] + [round(number = np.mean(passes[:x]), ndigits = 1) for x in range(1, len(passes) + 1)]
        passes = passes[::-1]
        
        data_frame.loc[data_frame.away_team == team, 'avg_passes_a'] = passes
        
    return data_frame

def create_cumulative_tackles_h(data_frame = None):
    """
    This is a function that will calculate the cumulative tackles for a home team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['avg_tackles_h'] = np.nan
    
    for team in teams:
        tackles = data_frame.loc[data_frame.home_team == team, 'tackles_h'].to_numpy()[::-1][:-1]
        tackles = [0.0] + [round(number = np.mean(tackles[:x]), ndigits = 1) for x in range(1, len(tackles) + 1)]
        tackles = tackles[::-1]
        
        data_frame.loc[data_frame.home_team == team, 'avg_tackles_h'] = tackles
        
    return data_frame

def create_cumulative_tackles_a(data_frame = None):
    """
    This is a function that will calculate the cumulative tackles for an away team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.away_team.unique().tolist()
    data_frame['avg_tackles_a'] = np.nan
    
    for team in teams:
        tackles = data_frame.loc[data_frame.away_team == team, 'tackles_a'].to_numpy()[::-1][:-1]
        tackles = [0.0] + [round(number = np.mean(tackles[:x]), ndigits = 1) for x in range(1, len(tackles) + 1)]
        tackles = tackles[::-1]
        
        data_frame.loc[data_frame.away_team == team, 'avg_tackles_a'] = tackles
        
    return data_frame

def create_cumulative_clearances_h(data_frame = None):
    """
    This is a function that will calculate the cumulative clearances for a home team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['avg_clearances_h'] = np.nan
    
    for team in teams:
        clearances = data_frame.loc[data_frame.home_team == team, 'clearances_h'].to_numpy()[::-1][:-1]
        clearances = [0.0] + [round(number = np.mean(clearances[:x]), ndigits = 1) for x in range(1, len(clearances) + 1)]
        clearances = clearances[::-1]
        
        data_frame.loc[data_frame.home_team == team, 'avg_clearances_h'] = clearances
        
    return data_frame

def create_cumulative_clearances_a(data_frame = None):
    """
    This is a function that will calculate the cumulative clearances for an away team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.away_team.unique().tolist()
    data_frame['avg_clearances_a'] = np.nan
    
    for team in teams:
        clearances = data_frame.loc[data_frame.away_team == team, 'clearances_a'].to_numpy()[::-1][:-1]
        clearances = [0.0] + [round(number = np.mean(clearances[:x]), ndigits = 1) for x in range(1, len(clearances) + 1)]
        clearances = clearances[::-1]
        
        data_frame.loc[data_frame.away_team == team, 'avg_clearances_a'] = clearances
        
    return data_frame

def create_cumulative_corners_h(data_frame = None):
    """
    This is a function that will calculate the cumulative corners for a home team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['avg_corners_h'] = np.nan
    
    for team in teams:
        corners = data_frame.loc[data_frame.home_team == team, 'corners_h'].to_numpy()[::-1][:-1]
        corners = [0.0] + [round(number = np.mean(corners[:x]), ndigits = 1) for x in range(1, len(corners) + 1)]
        corners = corners[::-1]
        
        data_frame.loc[data_frame.home_team == team, 'avg_corners_h'] = corners
        
    return data_frame

def create_cumulative_corners_a(data_frame = None):
    """
    This is a function that will calculate the cumulative corners for an away team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.away_team.unique().tolist()
    data_frame['avg_corners_a'] = np.nan
    
    for team in teams:
        corners = data_frame.loc[data_frame.away_team == team, 'corners_a'].to_numpy()[::-1][:-1]
        corners = [0.0] + [round(number = np.mean(corners[:x]), ndigits = 1) for x in range(1, len(corners) + 1)]
        corners = corners[::-1]
        
        data_frame.loc[data_frame.away_team == team, 'avg_corners_a'] = corners
        
    return data_frame

def create_cumulative_offsides_h(data_frame = None):
    """
    This is a function that will calculate the cumulative offsides for a home team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['avg_offsides_h'] = np.nan
    
    for team in teams:
        offsides = data_frame.loc[data_frame.home_team == team, 'offsides_h'].to_numpy()[::-1][:-1]
        offsides = [0.0] + [round(number = np.mean(offsides[:x]), ndigits = 1) for x in range(1, len(offsides) + 1)]
        offsides = offsides[::-1]
        
        data_frame.loc[data_frame.home_team == team, 'avg_offsides_h'] = offsides
        
    return data_frame

def create_cumulative_offsides_a(data_frame = None):
    """
    This is a function that will calculate the cumulative offsides for an away team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.away_team.unique().tolist()
    data_frame['avg_offsides_a'] = np.nan
    
    for team in teams:
        offsides = data_frame.loc[data_frame.away_team == team, 'offsides_a'].to_numpy()[::-1][:-1]
        offsides = [0.0] + [round(number = np.mean(offsides[:x]), ndigits = 1) for x in range(1, len(offsides) + 1)]
        offsides = offsides[::-1]
        
        data_frame.loc[data_frame.away_team == team, 'avg_offsides_a'] = offsides
        
    return data_frame

def create_cumulative_yellow_cards_h(data_frame = None):
    """
    This is a function that will calculate the cumulative yellow cards for a home team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['avg_yellow_cards_h'] = np.nan
    
    for team in teams:
        yellow_cards = data_frame.loc[data_frame.home_team == team, 'yellow_cards_h'].to_numpy()[::-1][:-1]
        yellow_cards = [0.0] + [round(number = np.mean(yellow_cards[:x]), ndigits = 1) for x in range(1, len(yellow_cards) + 1)]
        yellow_cards = yellow_cards[::-1]
        
        data_frame.loc[data_frame.home_team == team, 'avg_yellow_cards_h'] = yellow_cards
        
    return data_frame

def create_cumulative_yellow_cards_a(data_frame = None):
    """
    This is a function that will calculate the cumulative yellow cards for an away team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.away_team.unique().tolist()
    data_frame['avg_yellow_cards_a'] = np.nan
    
    for team in teams:
        yellow_cards = data_frame.loc[data_frame.away_team == team, 'yellow_cards_a'].to_numpy()[::-1][:-1]
        yellow_cards = [0.0] + [round(number = np.mean(yellow_cards[:x]), ndigits = 1) for x in range(1, len(yellow_cards) + 1)]
        yellow_cards = yellow_cards[::-1]
        
        data_frame.loc[data_frame.away_team == team, 'avg_yellow_cards_a'] = yellow_cards
        
    return data_frame

def create_cumulative_fouls_conceded_h(data_frame = None):
    """
    This is a function that will calculate the cumulative fouls conceded for a home team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['avg_fouls_conceded_h'] = np.nan
    
    for team in teams:
        fouls_conceded = data_frame.loc[data_frame.home_team == team, 'fouls_conceded_h'].to_numpy()[::-1][:-1]
        fouls_conceded = [0.0] + [round(number = np.mean(fouls_conceded[:x]), ndigits = 1) for x in range(1, len(fouls_conceded) + 1)]
        fouls_conceded = fouls_conceded[::-1]
        
        data_frame.loc[data_frame.home_team == team, 'avg_fouls_conceded_h'] = fouls_conceded
        
    return data_frame

def create_cumulative_fouls_conceded_a(data_frame = None):
    """
    This is a function that will calculate the cumulative fouls conceded for an away team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.away_team.unique().tolist()
    data_frame['avg_fouls_conceded_a'] = np.nan
    
    for team in teams:
        fouls_conceded = data_frame.loc[data_frame.away_team == team, 'fouls_conceded_a'].to_numpy()[::-1][:-1]
        fouls_conceded = [0.0] + [round(number = np.mean(fouls_conceded[:x]), ndigits = 1) for x in range(1, len(fouls_conceded) + 1)]
        fouls_conceded = fouls_conceded[::-1]
        
        data_frame.loc[data_frame.away_team == team, 'avg_fouls_conceded_a'] = fouls_conceded
        
    return data_frame

def create_n_matches_played(data_frame = None):
    """
    This is a function that identifies the number of matches played at home and away for home and away teams.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['n_matches_played_h'] = np.nan
    data_frame['n_matches_played_a'] = np.nan
    
    for team in teams:
        n_matches_played_h = list(range(data_frame.loc[data_frame.home_team == team].shape[0]))[::-1]
        n_matches_played_a = list(range(data_frame.loc[data_frame.away_team == team].shape[0]))[::-1]
        data_frame.loc[data_frame.home_team == team, 'n_matches_played_h'] = n_matches_played_h
        data_frame.loc[data_frame.away_team == team, 'n_matches_played_a'] = n_matches_played_a
        
    data_frame[['n_matches_played_h', 'n_matches_played_a']] = data_frame[['n_matches_played_h', 'n_matches_played_a']].applymap(lambda x: int(x))
    
    return data_frame

def create_max_and_dropped_points(data_frame = None):
    """
    This is a function that will calculate maximum points a team can get based on the
    number of matches played and dropped points.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['max_points_h'] = np.nan
    data_frame['max_points_a'] = np.nan
    
    for team in teams:
        max_points_h = data_frame.loc[data_frame.home_team == team, 'n_matches_played_h'].to_numpy() * 3
        max_points_a = data_frame.loc[data_frame.away_team == team, 'n_matches_played_a'].to_numpy() * 3
        data_frame.loc[data_frame.home_team == team, 'max_points_h'] = max_points_h
        data_frame.loc[data_frame.away_team == team, 'max_points_a'] = max_points_a
    
    data_frame[['max_points_h', 'max_points_a']] = data_frame[['max_points_h', 'max_points_a']].applymap(lambda x: int(x))
    
    data_frame['points_dropped_h'] = data_frame.max_points_h - data_frame.points_h_cum 
    data_frame['points_dropped_a'] = data_frame.max_points_a - data_frame.points_a_cum
    
    return data_frame

def create_avg_possession_last_3_and_5_h(data_frame = None):
    """
    This is a function that will calculate the average possession in last three and five home games for a home team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['avg_possession_last_3_h'] = np.nan
    data_frame['avg_possession_last_5_h'] = np.nan
    
    for team in teams:
        possession = data_frame.loc[data_frame.home_team == team, 'possession_h'].to_numpy()[1:]
        possession_3 = [round(number = np.mean(possession[x:x + 3]), ndigits = 1) if len(possession[x:x + 3]) == 3 else 50.0 \
                        for x in list(range(len(possession)))] + [50.0]
        possession_5 = [round(number = np.mean(possession[x:x + 5]), ndigits = 1) if len(possession[x:x + 5]) == 5 else 50.0 \
                        for x in list(range(len(possession)))] + [50.0]
        
        data_frame.loc[data_frame.home_team == team, 'avg_possession_last_3_h'] = possession_3
        data_frame.loc[data_frame.home_team == team, 'avg_possession_last_5_h'] = possession_5
        
    return data_frame

def create_avg_possession_last_3_and_5_a(data_frame = None):
    """
    This is a function that will calculate the average possession in last three and five away games for an away team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.away_team.unique().tolist()
    data_frame['avg_possession_last_3_a'] = np.nan
    data_frame['avg_possession_last_5_a'] = np.nan
    
    for team in teams:
        possession = data_frame.loc[data_frame.away_team == team, 'possession_a'].to_numpy()[1:]
        possession_3 = [round(number = np.mean(possession[x:x + 3]), ndigits = 1) if len(possession[x:x + 3]) == 3 else 50.0 \
                        for x in list(range(len(possession)))] + [50.0]
        possession_5 = [round(number = np.mean(possession[x:x + 5]), ndigits = 1) if len(possession[x:x + 5]) == 5 else 50.0 \
                        for x in list(range(len(possession)))] + [50.0]
        
        data_frame.loc[data_frame.away_team == team, 'avg_possession_last_3_a'] = possession_3
        data_frame.loc[data_frame.away_team == team, 'avg_possession_last_5_a'] = possession_5
        
    return data_frame

def create_avg_shots_on_target_last_3_and_5_h(data_frame = None):
    """
    This is a function that will calculate the average shots on target in last three and five home games for a home team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['avg_shots_on_target_last_3_h'] = np.nan
    data_frame['avg_shots_on_target_last_5_h'] = np.nan
    
    for team in teams:
        shots_on_target = data_frame.loc[data_frame.home_team == team, 'shots_on_target_h'].to_numpy()[1:]
        shots_on_target_3 = [round(number = np.mean(shots_on_target[x:x + 3]), ndigits = 1) if len(shots_on_target[x:x + 3]) == 3 else 0.0 \
                             for x in list(range(len(shots_on_target)))] + [0.0]
        shots_on_target_5 = [round(number = np.mean(shots_on_target[x:x + 5]), ndigits = 1) if len(shots_on_target[x:x + 5]) == 5 else 0.0 \
                             for x in list(range(len(shots_on_target)))] + [0.0]
        
        data_frame.loc[data_frame.home_team == team, 'avg_shots_on_target_last_3_h'] = shots_on_target_3
        data_frame.loc[data_frame.home_team == team, 'avg_shots_on_target_last_5_h'] = shots_on_target_5
        
    return data_frame

def create_avg_shots_on_target_last_3_and_5_a(data_frame = None):
    """
    This is a function that will calculate the average shots on target in last three and five away games for an away team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.away_team.unique().tolist()
    data_frame['avg_shots_on_target_last_3_a'] = np.nan
    data_frame['avg_shots_on_target_last_5_a'] = np.nan
    
    for team in teams:
        shots_on_target = data_frame.loc[data_frame.away_team == team, 'shots_on_target_a'].to_numpy()[1:]
        shots_on_target_3 = [round(number = np.mean(shots_on_target[x:x + 3]), ndigits = 1) if len(shots_on_target[x:x + 3]) == 3 else 0.0 \
                             for x in list(range(len(shots_on_target)))] + [0.0]
        shots_on_target_5 = [round(number = np.mean(shots_on_target[x:x + 5]), ndigits = 1) if len(shots_on_target[x:x + 5]) == 5 else 0.0 \
                             for x in list(range(len(shots_on_target)))] + [0.0]
        
        data_frame.loc[data_frame.away_team == team, 'avg_shots_on_target_last_3_a'] = shots_on_target_3
        data_frame.loc[data_frame.away_team == team, 'avg_shots_on_target_last_5_a'] = shots_on_target_5
        
    return data_frame

def create_avg_shots_last_3_and_5_h(data_frame = None):
    """
    This is a function that will calculate the average shots in last three and five home games for a home team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['avg_shots_last_3_h'] = np.nan
    data_frame['avg_shots_last_5_h'] = np.nan
    
    for team in teams:
        shots = data_frame.loc[data_frame.home_team == team, 'shots_h'].to_numpy()[1:]
        shots_3 = [round(number = np.mean(shots[x:x + 3]), ndigits = 1) if len(shots[x:x + 3]) == 3 else 0.0 for x in list(range(len(shots)))] + [0.0]
        shots_5 = [round(number = np.mean(shots[x:x + 5]), ndigits = 1) if len(shots[x:x + 5]) == 5 else 0.0 for x in list(range(len(shots)))] + [0.0]
        
        data_frame.loc[data_frame.home_team == team, 'avg_shots_last_3_h'] = shots_3
        data_frame.loc[data_frame.home_team == team, 'avg_shots_last_5_h'] = shots_5
        
    return data_frame

def create_avg_shots_last_3_and_5_a(data_frame = None):
    """
    This is a function that will calculate the average shots in last three and five away games for an away team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.away_team.unique().tolist()
    data_frame['avg_shots_last_3_a'] = np.nan
    data_frame['avg_shots_last_5_a'] = np.nan
    
    for team in teams:
        shots = data_frame.loc[data_frame.away_team == team, 'shots_a'].to_numpy()[1:]
        shots_3 = [round(number = np.mean(shots[x:x + 3]), ndigits = 1) if len(shots[x:x + 3]) == 3 else 0.0 for x in list(range(len(shots)))] + [0.0]
        shots_5 = [round(number = np.mean(shots[x:x + 5]), ndigits = 1) if len(shots[x:x + 5]) == 5 else 0.0 for x in list(range(len(shots)))] + [0.0]
        
        data_frame.loc[data_frame.away_team == team, 'avg_shots_last_3_a'] = shots_3
        data_frame.loc[data_frame.away_team == team, 'avg_shots_last_5_a'] = shots_5
        
    return data_frame

def create_avg_touches_last_3_and_5_h(data_frame = None):
    """
    This is a function that will calculate the average touches in last three and five home games for a home team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['avg_touches_last_3_h'] = np.nan
    data_frame['avg_touches_last_5_h'] = np.nan
    
    for team in teams:
        touches = data_frame.loc[data_frame.home_team == team, 'touches_h'].to_numpy()[1:]
        touches_3 = [round(number = np.mean(touches[x:x + 3]), ndigits = 1) if len(touches[x:x + 3]) == 3 else 0.0 \
                     for x in list(range(len(touches)))] + [0.0]
        touches_5 = [round(number = np.mean(touches[x:x + 5]), ndigits = 1) if len(touches[x:x + 5]) == 5 else 0.0 \
                     for x in list(range(len(touches)))] + [0.0]
        
        data_frame.loc[data_frame.home_team == team, 'avg_touches_last_3_h'] = touches_3
        data_frame.loc[data_frame.home_team == team, 'avg_touches_last_5_h'] = touches_5
        
    return data_frame

def create_avg_touches_last_3_and_5_a(data_frame = None):
    """
    This is a function that will calculate the average touches in last three and five away games for an away team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.away_team.unique().tolist()
    data_frame['avg_touches_last_3_a'] = np.nan
    data_frame['avg_touches_last_5_a'] = np.nan
    
    for team in teams:
        touches = data_frame.loc[data_frame.away_team == team, 'touches_a'].to_numpy()[1:]
        touches_3 = [round(number = np.mean(touches[x:x + 3]), ndigits = 1) if len(touches[x:x + 3]) == 3 else 0.0 \
                     for x in list(range(len(touches)))] + [0.0]
        touches_5 = [round(number = np.mean(touches[x:x + 5]), ndigits = 1) if len(touches[x:x + 5]) == 5 else 0.0 \
                     for x in list(range(len(touches)))] + [0.0]
        
        data_frame.loc[data_frame.away_team == team, 'avg_touches_last_3_a'] = touches_3
        data_frame.loc[data_frame.away_team == team, 'avg_touches_last_5_a'] = touches_5
        
    return data_frame

def create_avg_passes_last_3_and_5_h(data_frame = None):
    """
    This is a function that will calculate the average passes in last three and five home games for a home team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['avg_passes_last_3_h'] = np.nan
    data_frame['avg_passes_last_5_h'] = np.nan
    
    for team in teams:
        passes = data_frame.loc[data_frame.home_team == team, 'passes_h'].to_numpy()[1:]
        passes_3 = [round(number = np.mean(passes[x:x + 3]), ndigits = 1) if len(passes[x:x + 3]) == 3 else 0.0 for x in list(range(len(passes)))] + [0.0]
        passes_5 = [round(number = np.mean(passes[x:x + 5]), ndigits = 1) if len(passes[x:x + 5]) == 5 else 0.0 for x in list(range(len(passes)))] + [0.0]
        
        data_frame.loc[data_frame.home_team == team, 'avg_passes_last_3_h'] = passes_3
        data_frame.loc[data_frame.home_team == team, 'avg_passes_last_5_h'] = passes_5
        
    return data_frame

def create_avg_passes_last_3_and_5_a(data_frame = None):
    """
    This is a function that will calculate the average passes in last three and five away games for an away team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.away_team.unique().tolist()
    data_frame['avg_passes_last_3_a'] = np.nan
    data_frame['avg_passes_last_5_a'] = np.nan
    
    for team in teams:
        passes = data_frame.loc[data_frame.away_team == team, 'passes_a'].to_numpy()[1:]
        passes_3 = [round(number = np.mean(passes[x:x + 3]), ndigits = 1) if len(passes[x:x + 3]) == 3 else 0.0 for x in list(range(len(passes)))] + [0.0]
        passes_5 = [round(number = np.mean(passes[x:x + 5]), ndigits = 1) if len(passes[x:x + 5]) == 5 else 0.0 for x in list(range(len(passes)))] + [0.0]
        
        data_frame.loc[data_frame.away_team == team, 'avg_passes_last_3_a'] = passes_3
        data_frame.loc[data_frame.away_team == team, 'avg_passes_last_5_a'] = passes_5
        
    return data_frame

def create_avg_tackles_last_3_and_5_h(data_frame = None):
    """
    This is a function that will calculate the average tackles in last three and five home games for a home team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['avg_tackles_last_3_h'] = np.nan
    data_frame['avg_tackles_last_5_h'] = np.nan
    
    for team in teams:
        tackles = data_frame.loc[data_frame.home_team == team, 'tackles_h'].to_numpy()[1:]
        tackles_3 = [round(number = np.mean(tackles[x:x + 3]), ndigits = 1) if len(tackles[x:x + 3]) == 3 else 0.0 \
                     for x in list(range(len(tackles)))] + [0.0]
        tackles_5 = [round(number = np.mean(tackles[x:x + 5]), ndigits = 1) if len(tackles[x:x + 5]) == 5 else 0.0 \
                     for x in list(range(len(tackles)))] + [0.0]
        
        data_frame.loc[data_frame.home_team == team, 'avg_tackles_last_3_h'] = tackles_3
        data_frame.loc[data_frame.home_team == team, 'avg_tackles_last_5_h'] = tackles_5
        
    return data_frame

def create_avg_tackles_last_3_and_5_a(data_frame = None):
    """
    This is a function that will calculate the average tackles in last three and five away games for an away team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.away_team.unique().tolist()
    data_frame['avg_tackles_last_3_a'] = np.nan
    data_frame['avg_tackles_last_5_a'] = np.nan
    
    for team in teams:
        tackles = data_frame.loc[data_frame.away_team == team, 'tackles_a'].to_numpy()[1:]
        tackles_3 = [round(number = np.mean(tackles[x:x + 3]), ndigits = 1) if len(tackles[x:x + 3]) == 3 else 0.0 \
                     for x in list(range(len(tackles)))] + [0.0]
        tackles_5 = [round(number = np.mean(tackles[x:x + 5]), ndigits = 1) if len(tackles[x:x + 5]) == 5 else 0.0 \
                     for x in list(range(len(tackles)))] + [0.0]
        
        data_frame.loc[data_frame.away_team == team, 'avg_tackles_last_3_a'] = tackles_3
        data_frame.loc[data_frame.away_team == team, 'avg_tackles_last_5_a'] = tackles_5
        
    return data_frame

def create_avg_clearances_last_3_and_5_h(data_frame = None):
    """
    This is a function that will calculate the average clearances in last three and five home games for a home team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['avg_clearances_last_3_h'] = np.nan
    data_frame['avg_clearances_last_5_h'] = np.nan
    
    for team in teams:
        clearances = data_frame.loc[data_frame.home_team == team, 'clearances_h'].to_numpy()[1:]
        clearances_3 = [round(number = np.mean(clearances[x:x + 3]), ndigits = 1) if len(clearances[x:x + 3]) == 3 else 0.0 \
                        for x in list(range(len(clearances)))] + [0.0]
        clearances_5 = [round(number = np.mean(clearances[x:x + 5]), ndigits = 1) if len(clearances[x:x + 5]) == 5 else 0.0 \
                        for x in list(range(len(clearances)))] + [0.0]
        
        data_frame.loc[data_frame.home_team == team, 'avg_clearances_last_3_h'] = clearances_3
        data_frame.loc[data_frame.home_team == team, 'avg_clearances_last_5_h'] = clearances_5
        
    return data_frame

def create_avg_clearances_last_3_and_5_a(data_frame = None):
    """
    This is a function that will calculate the average clearances in last three and five away games for an away team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.away_team.unique().tolist()
    data_frame['avg_clearances_last_3_a'] = np.nan
    data_frame['avg_clearances_last_5_a'] = np.nan
    
    for team in teams:
        clearances = data_frame.loc[data_frame.away_team == team, 'clearances_a'].to_numpy()[1:]
        clearances_3 = [round(number = np.mean(clearances[x:x + 3]), ndigits = 1) if len(clearances[x:x + 3]) == 3 else 0.0 \
                        for x in list(range(len(clearances)))] + [0.0]
        clearances_5 = [round(number = np.mean(clearances[x:x + 5]), ndigits = 1) if len(clearances[x:x + 5]) == 5 else 0.0 \
                        for x in list(range(len(clearances)))] + [0.0]
        
        data_frame.loc[data_frame.away_team == team, 'avg_clearances_last_3_a'] = clearances_3
        data_frame.loc[data_frame.away_team == team, 'avg_clearances_last_5_a'] = clearances_5
        
    return data_frame

def create_avg_corners_last_3_and_5_h(data_frame = None):
    """
    This is a function that will calculate the average corners in last three and five home games for a home team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['avg_corners_last_3_h'] = np.nan
    data_frame['avg_corners_last_5_h'] = np.nan
    
    for team in teams:
        corners = data_frame.loc[data_frame.home_team == team, 'corners_h'].to_numpy()[1:]
        corners_3 = [round(number = np.mean(corners[x:x + 3]), ndigits = 1) if len(corners[x:x + 3]) == 3 else 0.0 \
                     for x in list(range(len(corners)))] + [0.0]
        corners_5 = [round(number = np.mean(corners[x:x + 5]), ndigits = 1) if len(corners[x:x + 5]) == 5 else 0.0 \
                     for x in list(range(len(corners)))] + [0.0]
        
        data_frame.loc[data_frame.home_team == team, 'avg_corners_last_3_h'] = corners_3
        data_frame.loc[data_frame.home_team == team, 'avg_corners_last_5_h'] = corners_5
        
    return data_frame

def create_avg_corners_last_3_and_5_a(data_frame = None):
    """
    This is a function that will calculate the average corners in last three and five away games for an away team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.away_team.unique().tolist()
    data_frame['avg_corners_last_3_a'] = np.nan
    data_frame['avg_corners_last_5_a'] = np.nan
    
    for team in teams:
        corners = data_frame.loc[data_frame.away_team == team, 'corners_a'].to_numpy()[1:]
        corners_3 = [round(number = np.mean(corners[x:x + 3]), ndigits = 1) if len(corners[x:x + 3]) == 3 else 0.0 \
                     for x in list(range(len(corners)))] + [0.0]
        corners_5 = [round(number = np.mean(corners[x:x + 5]), ndigits = 1) if len(corners[x:x + 5]) == 5 else 0.0 \
                     for x in list(range(len(corners)))] + [0.0]
        
        data_frame.loc[data_frame.away_team == team, 'avg_corners_last_3_a'] = corners_3
        data_frame.loc[data_frame.away_team == team, 'avg_corners_last_5_a'] = corners_5
        
    return data_frame

def create_avg_offsides_last_3_and_5_h(data_frame = None):
    """
    This is a function that will calculate the average offsides in last three and five home games for a home team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['avg_offsides_last_3_h'] = np.nan
    data_frame['avg_offsides_last_5_h'] = np.nan
    
    for team in teams:
        offsides = data_frame.loc[data_frame.home_team == team, 'offsides_h'].to_numpy()[1:]
        offsides_3 = [round(number = np.mean(offsides[x:x + 3]), ndigits = 1) if len(offsides[x:x + 3]) == 3 else 0.0 \
                      for x in list(range(len(offsides)))] + [0.0]
        offsides_5 = [round(number = np.mean(offsides[x:x + 5]), ndigits = 1) if len(offsides[x:x + 5]) == 5 else 0.0 \
                      for x in list(range(len(offsides)))] + [0.0]
        
        data_frame.loc[data_frame.home_team == team, 'avg_offsides_last_3_h'] = offsides_3
        data_frame.loc[data_frame.home_team == team, 'avg_offsides_last_5_h'] = offsides_5
        
    return data_frame

def create_avg_offsides_last_3_and_5_a(data_frame = None):
    """
    This is a function that will calculate the average offsides in last three and five away games for an away team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.away_team.unique().tolist()
    data_frame['avg_offsides_last_3_a'] = np.nan
    data_frame['avg_offsides_last_5_a'] = np.nan
    
    for team in teams:
        offsides = data_frame.loc[data_frame.away_team == team, 'offsides_a'].to_numpy()[1:]
        offsides_3 = [round(number = np.mean(offsides[x:x + 3]), ndigits = 1) if len(offsides[x:x + 3]) == 3 else 0.0 \
                      for x in list(range(len(offsides)))] + [0.0]
        offsides_5 = [round(number = np.mean(offsides[x:x + 5]), ndigits = 1) if len(offsides[x:x + 5]) == 5 else 0.0 \
                      for x in list(range(len(offsides)))] + [0.0]
        
        data_frame.loc[data_frame.away_team == team, 'avg_offsides_last_3_a'] = offsides_3
        data_frame.loc[data_frame.away_team == team, 'avg_offsides_last_5_a'] = offsides_5
        
    return data_frame

def create_avg_yellow_cards_last_3_and_5_h(data_frame = None):
    """
    This is a function that will calculate the average yellow cards in last three and five home games for a home team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['avg_yellow_cards_last_3_h'] = np.nan
    data_frame['avg_yellow_cards_last_5_h'] = np.nan
    
    for team in teams:
        yellow_cards = data_frame.loc[data_frame.home_team == team, 'yellow_cards_h'].to_numpy()[1:]
        yellow_cards_3 = [round(number = np.mean(yellow_cards[x:x + 3]), ndigits = 1) if len(yellow_cards[x:x + 3]) == 3 else 0.0 \
                          for x in list(range(len(yellow_cards)))] + [0.0]
        yellow_cards_5 = [round(number = np.mean(yellow_cards[x:x + 5]), ndigits = 1) if len(yellow_cards[x:x + 5]) == 5 else 0.0 \
                          for x in list(range(len(yellow_cards)))] + [0.0]
        
        data_frame.loc[data_frame.home_team == team, 'avg_yellow_cards_last_3_h'] = yellow_cards_3
        data_frame.loc[data_frame.home_team == team, 'avg_yellow_cards_last_5_h'] = yellow_cards_5
        
    return data_frame

def create_avg_yellow_cards_last_3_and_5_a(data_frame = None):
    """
    This is a function that will calculate the average yellow cards in last three and five away games for an away team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.away_team.unique().tolist()
    data_frame['avg_yellow_cards_last_3_a'] = np.nan
    data_frame['avg_yellow_cards_last_5_a'] = np.nan
    
    for team in teams:
        yellow_cards = data_frame.loc[data_frame.away_team == team, 'yellow_cards_a'].to_numpy()[1:]
        yellow_cards_3 = [round(number = np.mean(yellow_cards[x:x + 3]), ndigits = 1) if len(yellow_cards[x:x + 3]) == 3 else 0.0 \
                          for x in list(range(len(yellow_cards)))] + [0.0]
        yellow_cards_5 = [round(number = np.mean(yellow_cards[x:x + 5]), ndigits = 1) if len(yellow_cards[x:x + 5]) == 5 else 0.0 \
                          for x in list(range(len(yellow_cards)))] + [0.0]
        
        data_frame.loc[data_frame.away_team == team, 'avg_yellow_cards_last_3_a'] = yellow_cards_3
        data_frame.loc[data_frame.away_team == team, 'avg_yellow_cards_last_5_a'] = yellow_cards_5
        
    return data_frame

def create_avg_fouls_conceded_last_3_and_5_h(data_frame = None):
    """
    This is a function that will calculate the average fouls conceded in last three and five home games for a home team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['avg_fouls_conceded_last_3_h'] = np.nan
    data_frame['avg_fouls_conceded_last_5_h'] = np.nan
    
    for team in teams:
        fouls_conceded = data_frame.loc[data_frame.home_team == team, 'fouls_conceded_h'].to_numpy()[1:]
        fouls_conceded_3 = [round(number = np.mean(fouls_conceded[x:x + 3]), ndigits = 1) if len(fouls_conceded[x:x + 3]) == 3 else 0.0 \
                            for x in list(range(len(fouls_conceded)))] + [0.0]
        fouls_conceded_5 = [round(number = np.mean(fouls_conceded[x:x + 5]), ndigits = 1) if len(fouls_conceded[x:x + 5]) == 5 else 0.0 \
                            for x in list(range(len(fouls_conceded)))] + [0.0]
        
        data_frame.loc[data_frame.home_team == team, 'avg_fouls_conceded_last_3_h'] = fouls_conceded_3
        data_frame.loc[data_frame.home_team == team, 'avg_fouls_conceded_last_5_h'] = fouls_conceded_5
        
    return data_frame

def create_avg_fouls_conceded_last_3_and_5_a(data_frame = None):
    """
    This is a function that will calculate the average fouls conceded in last three and five away games for an away team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.away_team.unique().tolist()
    data_frame['avg_fouls_conceded_last_3_a'] = np.nan
    data_frame['avg_fouls_conceded_last_5_a'] = np.nan
    
    for team in teams:
        fouls_conceded = data_frame.loc[data_frame.away_team == team, 'fouls_conceded_a'].to_numpy()[1:]
        fouls_conceded_3 = [round(number = np.mean(fouls_conceded[x:x + 3]), ndigits = 1) if len(fouls_conceded[x:x + 3]) == 3 else 0.0 \
                            for x in list(range(len(fouls_conceded)))] + [0.0]
        fouls_conceded_5 = [round(number = np.mean(fouls_conceded[x:x + 5]), ndigits = 1) if len(fouls_conceded[x:x + 5]) == 5 else 0.0 \
                            for x in list(range(len(fouls_conceded)))] + [0.0]
        
        data_frame.loc[data_frame.away_team == team, 'avg_fouls_conceded_last_3_a'] = fouls_conceded_3
        data_frame.loc[data_frame.away_team == team, 'avg_fouls_conceded_last_5_a'] = fouls_conceded_5
        
    return data_frame

def create_total_goals_scored(data_frame = None):
    """
    This is a function that will calculate the total goals scored by a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_goals_scored_h'] = np.nan
    data_frame['total_goals_scored_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'goals_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'goals_a']]
        
        home.columns = ['match_date', 'goals']
        away.columns = ['match_date', 'goals']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.goals.to_list() + [0]
        total = np.cumsum(a = total[::-1][:-1])[::-1]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_goals_scored_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_goals_scored_a'] = away_data_frame
        
    data_frame[['total_goals_scored_h', 'total_goals_scored_a']] = data_frame[['total_goals_scored_h', 'total_goals_scored_a']].applymap(lambda x: int(x))
        
    return data_frame

def create_total_goals_conceded(data_frame = None):
    """
    This is a function that will calculate the total goals conceded by a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_goals_conceded_h'] = np.nan
    data_frame['total_goals_conceded_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'goals_a']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'goals_h']]
        
        home.columns = ['match_date', 'goals']
        away.columns = ['match_date', 'goals']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.goals.to_list() + [0]
        total = np.cumsum(a = total[::-1][:-1])[::-1]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_goals_conceded_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_goals_conceded_a'] = away_data_frame
        
    data_frame[['total_goals_conceded_h', 'total_goals_conceded_a']] = data_frame[['total_goals_conceded_h', 'total_goals_conceded_a']].applymap(lambda x: int(x))
        
    return data_frame

def create_total_avg_possesion(data_frame = None):
    """
    This is a function that will calculate the average possession for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_possession_h'] = np.nan
    data_frame['total_avg_possession_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'possession_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'possession_a']]
        
        home.columns = ['match_date', 'possession']
        away.columns = ['match_date', 'possession']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.possession.tolist()[::-1][:-1]
        total = [50.0] + [round(number = np.mean(total[:x]), ndigits = 1) for x in range(1, len(total) + 1)]
        total = total[::-1]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_possession_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_possession_a'] = away_data_frame
        
    return data_frame

def create_total_avg_shots_on_target(data_frame = None):
    """
    This is a function that will calculate the average shots on target for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_shots_on_target_h'] = np.nan
    data_frame['total_avg_shots_on_target_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'shots_on_target_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'shots_on_target_a']]
        
        home.columns = ['match_date', 'shots_on_target']
        away.columns = ['match_date', 'shots_on_target']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.shots_on_target.tolist()[::-1][:-1]
        total = [0.0] + [round(number = np.mean(total[:x]), ndigits = 1) for x in range(1, len(total) + 1)]
        total = total[::-1]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_shots_on_target_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_shots_on_target_a'] = away_data_frame
        
    return data_frame

def create_total_avg_shots(data_frame = None):
    """
    This is a function that will calculate the average shots for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_shots_h'] = np.nan
    data_frame['total_avg_shots_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'shots_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'shots_a']]
        
        home.columns = ['match_date', 'shots']
        away.columns = ['match_date', 'shots']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.shots.tolist()[::-1][:-1]
        total = [0.0] + [round(number = np.mean(total[:x]), ndigits = 1) for x in range(1, len(total) + 1)]
        total = total[::-1]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_shots_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_shots_a'] = away_data_frame
        
    return data_frame

def create_total_avg_touches(data_frame = None):
    """
    This is a function that will calculate the average touches for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_touches_h'] = np.nan
    data_frame['total_avg_touches_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'touches_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'touches_a']]
        
        home.columns = ['match_date', 'touches']
        away.columns = ['match_date', 'touches']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.touches.tolist()[::-1][:-1]
        total = [0.0] + [round(number = np.mean(total[:x]), ndigits = 1) for x in range(1, len(total) + 1)]
        total = total[::-1]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_touches_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_touches_a'] = away_data_frame
        
    return data_frame

def create_total_avg_passes(data_frame = None):
    """
    This is a function that will calculate the average passes for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_passes_h'] = np.nan
    data_frame['total_avg_passes_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'passes_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'passes_a']]
        
        home.columns = ['match_date', 'passes']
        away.columns = ['match_date', 'passes']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.passes.tolist()[::-1][:-1]
        total = [0.0] + [round(number = np.mean(total[:x]), ndigits = 1) for x in range(1, len(total) + 1)]
        total = total[::-1]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_passes_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_passes_a'] = away_data_frame
        
    return data_frame

def create_total_avg_tackles(data_frame = None):
    """
    This is a function that will calculate the average tackles for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_tackles_h'] = np.nan
    data_frame['total_avg_tackles_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'tackles_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'tackles_a']]
        
        home.columns = ['match_date', 'tackles']
        away.columns = ['match_date', 'tackles']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.tackles.tolist()[::-1][:-1]
        total = [0.0] + [round(number = np.mean(total[:x]), ndigits = 1) for x in range(1, len(total) + 1)]
        total = total[::-1]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_tackles_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_tackles_a'] = away_data_frame
        
    return data_frame

def create_total_avg_clearances(data_frame = None):
    """
    This is a function that will calculate the average clearances for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_clearances_h'] = np.nan
    data_frame['total_avg_clearances_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'clearances_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'clearances_a']]
        
        home.columns = ['match_date', 'clearances']
        away.columns = ['match_date', 'clearances']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.clearances.tolist()[::-1][:-1]
        total = [0.0] + [round(number = np.mean(total[:x]), ndigits = 1) for x in range(1, len(total) + 1)]
        total = total[::-1]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_clearances_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_clearances_a'] = away_data_frame
        
    return data_frame

def create_total_avg_corners(data_frame = None):
    """
    This is a function that will calculate the average corners for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_corners_h'] = np.nan
    data_frame['total_avg_corners_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'corners_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'corners_a']]
        
        home.columns = ['match_date', 'corners']
        away.columns = ['match_date', 'corners']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.corners.tolist()[::-1][:-1]
        total = [0.0] + [round(number = np.mean(total[:x]), ndigits = 1) for x in range(1, len(total) + 1)]
        total = total[::-1]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_corners_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_corners_a'] = away_data_frame
        
    return data_frame

def create_total_avg_offsides(data_frame = None):
    """
    This is a function that will calculate the average offsides for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_offsides_h'] = np.nan
    data_frame['total_avg_offsides_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'offsides_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'offsides_a']]
        
        home.columns = ['match_date', 'offsides']
        away.columns = ['match_date', 'offsides']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.offsides.tolist()[::-1][:-1]
        total = [0.0] + [round(number = np.mean(total[:x]), ndigits = 1) for x in range(1, len(total) + 1)]
        total = total[::-1]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_offsides_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_offsides_a'] = away_data_frame
        
    return data_frame

def create_total_avg_yellow_cards(data_frame = None):
    """
    This is a function that will calculate the average yellow cards for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_yellow_cards_h'] = np.nan
    data_frame['total_avg_yellow_cards_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'yellow_cards_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'yellow_cards_a']]
        
        home.columns = ['match_date', 'yellow_cards']
        away.columns = ['match_date', 'yellow_cards']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.yellow_cards.tolist()[::-1][:-1]
        total = [0.0] + [round(number = np.mean(total[:x]), ndigits = 1) for x in range(1, len(total) + 1)]
        total = total[::-1]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_yellow_cards_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_yellow_cards_a'] = away_data_frame
        
    return data_frame

def create_total_avg_fouls_conceded(data_frame = None):
    """
    This is a function that will calculate the average fouls conceded for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_fouls_conceded_h'] = np.nan
    data_frame['total_avg_fouls_conceded_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'fouls_conceded_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'fouls_conceded_a']]
        
        home.columns = ['match_date', 'fouls_conceded']
        away.columns = ['match_date', 'fouls_conceded']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.fouls_conceded.tolist()[::-1][:-1]
        total = [0.0] + [round(number = np.mean(total[:x]), ndigits = 1) for x in range(1, len(total) + 1)]
        total = total[::-1]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_fouls_conceded_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_fouls_conceded_a'] = away_data_frame
        
    return data_frame

def create_total_avg_possession_last_3(data_frame = None):
    """
    This is a function that will calculate the average possession in the last three matches for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_possession_last_3_h'] = np.nan
    data_frame['total_avg_possession_last_3_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'possession_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'possession_a']]
        
        home.columns = ['match_date', 'possession']
        away.columns = ['match_date', 'possession']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.possession.to_numpy()[1:]
        total = [round(number = np.mean(total[x:x + 3]), ndigits = 1) if len(total[x:x + 3]) == 3 else 50.0 for x in list(range(len(total)))] + [50.0]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_possession_last_3_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_possession_last_3_a'] = away_data_frame
        
    return data_frame

def create_total_avg_possession_last_5(data_frame = None):
    """
    This is a function that will calculate the average possession in the last five matches for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_possession_last_5_h'] = np.nan
    data_frame['total_avg_possession_last_5_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'possession_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'possession_a']]
        
        home.columns = ['match_date', 'possession']
        away.columns = ['match_date', 'possession']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.possession.to_numpy()[1:]
        total = [round(number = np.mean(total[x:x + 5]), ndigits = 1) if len(total[x:x + 5]) == 5 else 50.0 for x in list(range(len(total)))] + [50.0]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_possession_last_5_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_possession_last_5_a'] = away_data_frame
        
    return data_frame

def create_total_avg_shots_on_target_last_3(data_frame = None):
    """
    This is a function that will calculate the average shots on target in the last three matches for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_shots_on_target_last_3_h'] = np.nan
    data_frame['total_avg_shots_on_target_last_3_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'shots_on_target_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'shots_on_target_a']]
        
        home.columns = ['match_date', 'shots_on_target']
        away.columns = ['match_date', 'shots_on_target']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.shots_on_target.to_numpy()[1:]
        total = [round(number = np.mean(total[x:x + 3]), ndigits = 1) if len(total[x:x + 3]) == 3 else 0.0 for x in list(range(len(total)))] + [0.0]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_shots_on_target_last_3_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_shots_on_target_last_3_a'] = away_data_frame
        
    return data_frame

def create_total_avg_shots_on_target_last_5(data_frame = None):
    """
    This is a function that will calculate the average shots on target in the last fivr matches for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_shots_on_target_last_5_h'] = np.nan
    data_frame['total_avg_shots_on_target_last_5_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'shots_on_target_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'shots_on_target_a']]
        
        home.columns = ['match_date', 'shots_on_target']
        away.columns = ['match_date', 'shots_on_target']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.shots_on_target.to_numpy()[1:]
        total = [round(number = np.mean(total[x:x + 5]), ndigits = 1) if len(total[x:x + 5]) == 5 else 0.0 for x in list(range(len(total)))] + [0.0]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_shots_on_target_last_5_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_shots_on_target_last_5_a'] = away_data_frame
        
    return data_frame

def create_total_avg_shots_last_3(data_frame = None):
    """
    This is a function that will calculate the average shots in the last three matches for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_shots_last_3_h'] = np.nan
    data_frame['total_avg_shots_last_3_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'shots_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'shots_a']]
        
        home.columns = ['match_date', 'shots']
        away.columns = ['match_date', 'shots']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.shots.to_numpy()[1:]
        total = [round(number = np.mean(total[x:x + 3]), ndigits = 1) if len(total[x:x + 3]) == 3 else 0.0 for x in list(range(len(total)))] + [0.0]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_shots_last_3_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_shots_last_3_a'] = away_data_frame
        
    return data_frame

def create_total_avg_shots_last_5(data_frame = None):
    """
    This is a function that will calculate the average shots in the last five matches for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_shots_last_5_h'] = np.nan
    data_frame['total_avg_shots_last_5_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'shots_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'shots_a']]
        
        home.columns = ['match_date', 'shots']
        away.columns = ['match_date', 'shots']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.shots.to_numpy()[1:]
        total = [round(number = np.mean(total[x:x + 5]), ndigits = 1) if len(total[x:x + 5]) == 5 else 0.0 for x in list(range(len(total)))] + [0.0]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_shots_last_5_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_shots_last_5_a'] = away_data_frame
        
    return data_frame

def create_total_avg_touches_last_3(data_frame = None):
    """
    This is a function that will calculate the average touches in the last three matches for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_touches_last_3_h'] = np.nan
    data_frame['total_avg_touches_last_3_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'touches_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'touches_a']]
        
        home.columns = ['match_date', 'touches']
        away.columns = ['match_date', 'touches']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.touches.to_numpy()[1:]
        total = [round(number = np.mean(total[x:x + 3]), ndigits = 1) if len(total[x:x + 3]) == 3 else 0.0 for x in list(range(len(total)))] + [0.0]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_touches_last_3_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_touches_last_3_a'] = away_data_frame
        
    return data_frame

def create_total_avg_touches_last_5(data_frame = None):
    """
    This is a function that will calculate the average touches in the last three matches for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_touches_last_5_h'] = np.nan
    data_frame['total_avg_touches_last_5_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'touches_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'touches_a']]
        
        home.columns = ['match_date', 'touches']
        away.columns = ['match_date', 'touches']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.touches.to_numpy()[1:]
        total = [round(number = np.mean(total[x:x + 5]), ndigits = 1) if len(total[x:x + 5]) == 5 else 0.0 for x in list(range(len(total)))] + [0.0]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_touches_last_5_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_touches_last_5_a'] = away_data_frame
        
    return data_frame

def create_total_avg_passes_last_3(data_frame = None):
    """
    This is a function that will calculate the average passes in the last three matches for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_passes_last_3_h'] = np.nan
    data_frame['total_avg_passes_last_3_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'passes_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'passes_a']]
        
        home.columns = ['match_date', 'passes']
        away.columns = ['match_date', 'passes']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.passes.to_numpy()[1:]
        total = [round(number = np.mean(total[x:x + 3]), ndigits = 1) if len(total[x:x + 3]) == 3 else 0.0 for x in list(range(len(total)))] + [0.0]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_passes_last_3_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_passes_last_3_a'] = away_data_frame
        
    return data_frame

def create_total_avg_passes_last_5(data_frame = None):
    """
    This is a function that will calculate the average passes in the last five matches for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_passes_last_5_h'] = np.nan
    data_frame['total_avg_passes_last_5_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'passes_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'passes_a']]
        
        home.columns = ['match_date', 'passes']
        away.columns = ['match_date', 'passes']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.passes.to_numpy()[1:]
        total = [round(number = np.mean(total[x:x + 5]), ndigits = 1) if len(total[x:x + 5]) == 5 else 0.0 for x in list(range(len(total)))] + [0.0]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_passes_last_5_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_passes_last_5_a'] = away_data_frame
        
    return data_frame

def create_total_avg_tackles_last_3(data_frame = None):
    """
    This is a function that will calculate the average tackles in the last three matches for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_tackles_last_3_h'] = np.nan
    data_frame['total_avg_tackles_last_3_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'tackles_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'tackles_a']]
        
        home.columns = ['match_date', 'tackles']
        away.columns = ['match_date', 'tackles']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.tackles.to_numpy()[1:]
        total = [round(number = np.mean(total[x:x + 3]), ndigits = 1) if len(total[x:x + 3]) == 3 else 0.0 for x in list(range(len(total)))] + [0.0]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_tackles_last_3_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_tackles_last_3_a'] = away_data_frame
        
    return data_frame

def create_total_avg_tackles_last_5(data_frame = None):
    """
    This is a function that will calculate the average tackles in the last five matches for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_tackles_last_5_h'] = np.nan
    data_frame['total_avg_tackles_last_5_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'tackles_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'tackles_a']]
        
        home.columns = ['match_date', 'tackles']
        away.columns = ['match_date', 'tackles']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.tackles.to_numpy()[1:]
        total = [round(number = np.mean(total[x:x + 5]), ndigits = 1) if len(total[x:x + 5]) == 5 else 0.0 for x in list(range(len(total)))] + [0.0]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_tackles_last_5_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_tackles_last_5_a'] = away_data_frame
        
    return data_frame

def create_total_avg_clearances_last_3(data_frame = None):
    """
    This is a function that will calculate the average clearances in the last three matches for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_clearances_last_3_h'] = np.nan
    data_frame['total_avg_clearances_last_3_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'clearances_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'clearances_a']]
        
        home.columns = ['match_date', 'clearances']
        away.columns = ['match_date', 'clearances']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.clearances.to_numpy()[1:]
        total = [round(number = np.mean(total[x:x + 3]), ndigits = 1) if len(total[x:x + 3]) == 3 else 0.0 for x in list(range(len(total)))] + [0.0]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_clearances_last_3_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_clearances_last_3_a'] = away_data_frame
        
    return data_frame

def create_total_avg_clearances_last_5(data_frame = None):
    """
    This is a function that will calculate the average clearances in the last five matches for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_clearances_last_5_h'] = np.nan
    data_frame['total_avg_clearances_last_5_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'clearances_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'clearances_a']]
        
        home.columns = ['match_date', 'clearances']
        away.columns = ['match_date', 'clearances']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.clearances.to_numpy()[1:]
        total = [round(number = np.mean(total[x:x + 5]), ndigits = 1) if len(total[x:x + 5]) == 5 else 0.0 for x in list(range(len(total)))] + [0.0]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_clearances_last_5_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_clearances_last_5_a'] = away_data_frame
        
    return data_frame

def create_total_avg_corners_last_3(data_frame = None):
    """
    This is a function that will calculate the average corners in the last three matches for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_corners_last_3_h'] = np.nan
    data_frame['total_avg_corners_last_3_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'corners_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'corners_a']]
        
        home.columns = ['match_date', 'corners']
        away.columns = ['match_date', 'corners']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.corners.to_numpy()[1:]
        total = [round(number = np.mean(total[x:x + 3]), ndigits = 1) if len(total[x:x + 3]) == 3 else 0.0 for x in list(range(len(total)))] + [0.0]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_corners_last_3_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_corners_last_3_a'] = away_data_frame
        
    return data_frame

def create_total_avg_corners_last_5(data_frame = None):
    """
    This is a function that will calculate the average corners in the last five matches for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_corners_last_5_h'] = np.nan
    data_frame['total_avg_corners_last_5_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'corners_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'corners_a']]
        
        home.columns = ['match_date', 'corners']
        away.columns = ['match_date', 'corners']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.corners.to_numpy()[1:]
        total = [round(number = np.mean(total[x:x + 5]), ndigits = 1) if len(total[x:x + 5]) == 5 else 0.0 for x in list(range(len(total)))] + [0.0]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_corners_last_5_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_corners_last_5_a'] = away_data_frame
        
    return data_frame

def create_total_avg_offsides_last_3(data_frame = None):
    """
    This is a function that will calculate the average offsides in the last three matches for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_offsides_last_3_h'] = np.nan
    data_frame['total_avg_offsides_last_3_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'offsides_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'offsides_a']]
        
        home.columns = ['match_date', 'offsides']
        away.columns = ['match_date', 'offsides']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.offsides.to_numpy()[1:]
        total = [round(number = np.mean(total[x:x + 3]), ndigits = 1) if len(total[x:x + 3]) == 3 else 0.0 for x in list(range(len(total)))] + [0.0]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_offsides_last_3_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_offsides_last_3_a'] = away_data_frame
        
    return data_frame

def create_total_avg_offsides_last_5(data_frame = None):
    """
    This is a function that will calculate the average offsides in the last five matches for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_offsides_last_5_h'] = np.nan
    data_frame['total_avg_offsides_last_5_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'offsides_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'offsides_a']]
        
        home.columns = ['match_date', 'offsides']
        away.columns = ['match_date', 'offsides']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.offsides.to_numpy()[1:]
        total = [round(number = np.mean(total[x:x + 5]), ndigits = 1) if len(total[x:x + 5]) == 5 else 0.0 for x in list(range(len(total)))] + [0.0]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_offsides_last_5_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_offsides_last_5_a'] = away_data_frame
        
    return data_frame

def create_total_avg_yellow_cards_last_3(data_frame = None):
    """
    This is a function that will calculate the average yellow cards in the last three matches for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_yellow_cards_last_3_h'] = np.nan
    data_frame['total_avg_yellow_cards_last_3_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'yellow_cards_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'yellow_cards_a']]
        
        home.columns = ['match_date', 'yellow_cards']
        away.columns = ['match_date', 'yellow_cards']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.yellow_cards.to_numpy()[1:]
        total = [round(number = np.mean(total[x:x + 3]), ndigits = 1) if len(total[x:x + 3]) == 3 else 0.0 for x in list(range(len(total)))] + [0.0]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_yellow_cards_last_3_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_yellow_cards_last_3_a'] = away_data_frame
        
    return data_frame

def create_total_avg_yellow_cards_last_5(data_frame = None):
    """
    This is a function that will calculate the average yellow cards in the last five matches for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_yellow_cards_last_5_h'] = np.nan
    data_frame['total_avg_yellow_cards_last_5_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'yellow_cards_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'yellow_cards_a']]
        
        home.columns = ['match_date', 'yellow_cards']
        away.columns = ['match_date', 'yellow_cards']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.yellow_cards.to_numpy()[1:]
        total = [round(number = np.mean(total[x:x + 5]), ndigits = 1) if len(total[x:x + 5]) == 5 else 0.0 for x in list(range(len(total)))] + [0.0]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_yellow_cards_last_5_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_yellow_cards_last_5_a'] = away_data_frame
        
    return data_frame

def create_total_avg_fouls_conceded_last_3(data_frame = None):
    """
    This is a function that will calculate the average fouls conceded in the last three matches for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_fouls_conceded_last_3_h'] = np.nan
    data_frame['total_avg_fouls_conceded_last_3_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'fouls_conceded_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'fouls_conceded_a']]
        
        home.columns = ['match_date', 'fouls_conceded']
        away.columns = ['match_date', 'fouls_conceded']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.fouls_conceded.to_numpy()[1:]
        total = [round(number = np.mean(total[x:x + 3]), ndigits = 1) if len(total[x:x + 3]) == 3 else 0.0 for x in list(range(len(total)))] + [0.0]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_fouls_conceded_last_3_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_fouls_conceded_last_3_a'] = away_data_frame
        
    return data_frame

def create_total_avg_fouls_conceded_last_5(data_frame = None):
    """
    This is a function that will calculate the average fouls conceded in the last five matches for a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_avg_fouls_conceded_last_5_h'] = np.nan
    data_frame['total_avg_fouls_conceded_last_5_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'fouls_conceded_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'fouls_conceded_a']]
        
        home.columns = ['match_date', 'fouls_conceded']
        away.columns = ['match_date', 'fouls_conceded']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.fouls_conceded.to_numpy()[1:]
        total = [round(number = np.mean(total[x:x + 5]), ndigits = 1) if len(total[x:x + 5]) == 5 else 0.0 for x in list(range(len(total)))] + [0.0]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_avg_fouls_conceded_last_5_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_avg_fouls_conceded_last_5_a'] = away_data_frame
        
    return data_frame

def create_total_n_matches_played(data_frame = None):
    """
    This is a function that will calculate the total number of matches played by a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_n_matches_played_h'] = np.nan
    data_frame['total_n_matches_played_a'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'home_team']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'away_team']]
        
        home.columns = ['match_date', 'team']
        away.columns = ['match_date', 'team']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = list(range(combined_df.shape[0]))[::-1]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_n_matches_played_h'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_n_matches_played_a'] = away_data_frame
        
    data_frame[['total_n_matches_played_h', 'total_n_matches_played_a']] = data_frame[['total_n_matches_played_h', 
                                                                           'total_n_matches_played_a']].applymap(lambda x: int(x))
        
    return data_frame

def create_total_points_cum(data_frame = None):
    """
    This is a function to calculate total number of points accumulated by a team.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_points_h_cum'] = np.nan
    data_frame['total_points_a_cum'] = np.nan
    
    for team in teams:
        home = data_frame.loc[data_frame.home_team == team][['match_date', 'points_h']]
        away = data_frame.loc[data_frame.away_team == team][['match_date', 'points_a']]
        
        home.columns = ['match_date', 'points']
        away.columns = ['match_date', 'points']
        
        home['status'] = 'home'
        away['status'] = 'away'
        
        combined_df = pd.concat(objs = [home, away]).sort_values(by = 'match_date', ascending = False).reset_index(drop = True)
        total = combined_df.points.tolist() + [0]
        total = np.cumsum(a = total[::-1][:-1])[::-1]
        combined_df['total'] = total
        
        home_data_frame = combined_df.loc[combined_df.status == 'home', 'total'].to_numpy()
        away_data_frame = combined_df.loc[combined_df.status == 'away', 'total'].to_numpy()
        
        data_frame.loc[data_frame.home_team == team, 'total_points_h_cum'] = home_data_frame
        data_frame.loc[data_frame.away_team == team, 'total_points_a_cum'] = away_data_frame
        
    data_frame[['total_points_h_cum', 'total_points_a_cum']] = data_frame[['total_points_h_cum', 'total_points_a_cum']].applymap(lambda x: int(x))
        
    return data_frame

def create_total_max_and_dropped_points(data_frame = None):
    """
    This is a function that will calculate the total number of points dropped.
    
    Args:
        data_frame: Pandas data frame.
        
    Returns:
        Pandas data frame.
    """
    teams = data_frame.home_team.unique().tolist()
    data_frame['total_max_points_h'] = np.nan
    data_frame['total_max_points_a'] = np.nan
    
    for team in teams:
        total_max_points_h = data_frame.loc[data_frame.home_team == team, 'total_n_matches_played_h'].to_numpy() * 3
        total_max_points_a = data_frame.loc[data_frame.away_team == team, 'total_n_matches_played_a'].to_numpy() * 3
        data_frame.loc[data_frame.home_team == team, 'total_max_points_h'] = total_max_points_h
        data_frame.loc[data_frame.away_team == team, 'total_max_points_a'] = total_max_points_a
        
    data_frame[['total_max_points_h', 'total_max_points_a']] = data_frame[['total_max_points_h', 'total_max_points_a']].applymap(lambda x: int(x))
    
    data_frame['total_points_dropped_h'] = data_frame.total_max_points_h - data_frame.total_points_h_cum
    data_frame['total_points_dropped_a'] = data_frame.total_max_points_a - data_frame.total_points_a_cum
    
    return data_frame

def create_league_positions(data_frame = None):
    data_frame['h_position'] = np.nan
    data_frame['a_position'] = np.nan
    
    teams = data_frame.home_team.unique().tolist()
    all_match_weeks = sorted(data_frame.match_week.unique().tolist())
    
    for match_week in all_match_weeks:
        home_df = data_frame.loc[data_frame.match_week == match_week][['match_date', 'home_team', 'total_points_h_cum', 'total_goal_difference_h']].reset_index(drop = True)
        away_df = data_frame.loc[data_frame.match_week == match_week][['match_date', 'away_team', 'total_points_a_cum', 'total_goal_difference_a']].reset_index(drop = True)

        home_df.columns = ['date', 'team', 'point', 'gd']
        away_df.columns = ['date', 'team', 'point', 'gd']

        home_df['status'] = 'home'
        away_df['status'] = 'away'

        standings_df = pd.concat(objs = [home_df, away_df], ignore_index = True)
        standings_df.sort_values(by = 'date', ascending = False, inplace = True) # new
        standings_df.drop_duplicates(subset = 'team', inplace = True, ignore_index = True)
        standings_df.sort_values(by = ['point', 'gd', 'team'], ascending = [False, False, True], inplace = True)
        standings_df.reset_index(drop = True, inplace = True)
        standings_df['position'] = list(range(1, standings_df.shape[0] + 1))

        assert standings_df.shape[0] == standings_df.team.nunique()

        home_team_positions = standings_df.loc[standings_df.status == 'home'][['team', 'position']].reset_index(drop = True)
        away_team_positions = standings_df.loc[standings_df.status == 'away'][['team', 'position']].reset_index(drop = True)
        lacking_teams = [lacking_team for lacking_team in teams if lacking_team not in standings_df.team.tolist()]
        
        if match_week == 1 and standings_df.shape[0] < 20:
            pass
        elif standings_df.shape[0] < 20:
            previous_match_week = all_match_weeks[all_match_weeks.index(match_week) - 1]
            
            home_df_v2 = data_frame.loc[data_frame.match_week == previous_match_week][['home_team', 'total_points_h_cum', 'total_goal_difference_h']].reset_index(drop = True)
            away_df_v2 = data_frame.loc[data_frame.match_week == previous_match_week][['away_team', 'total_points_a_cum', 'total_goal_difference_a']].reset_index(drop = True)

            home_df_v2.columns = ['team', 'point', 'gd']
            away_df_v2.columns = ['team', 'point', 'gd']

            home_df_v2['status'] = 'home'
            away_df_v2['status'] = 'away'

            standings_df_v2 = pd.concat(objs = [home_df_v2, away_df_v2], ignore_index = True)
            standings_df_v2.sort_values(by = ['point', 'gd', 'team'], ascending = [False, False, True], inplace = True)
            standings_df_v2.reset_index(drop = True, inplace = True)
            standings_df_v2['position'] = list(range(1, standings_df_v2.shape[0] + 1))
            standings_df_v2.drop_duplicates(subset = 'team', inplace = True, ignore_index = True)

            assert standings_df_v2.shape[0] == standings_df_v2.team.nunique()
            extension_df = standings_df_v2.loc[standings_df_v2.team.isin(values = lacking_teams)]

            previous_week = 1

            while extension_df.shape[0] != len(lacking_teams):
                lacking_team_v2 = [team for team in lacking_teams if team not in extension_df.team.tolist()]
                
                home_df_v3 = data_frame.loc[data_frame.match_week == previous_match_week - previous_week][['home_team', 'total_points_h_cum', 'total_goal_difference_h']].reset_index(drop = True)
                away_df_v3 = data_frame.loc[data_frame.match_week == previous_match_week - previous_week][['away_team', 'total_points_a_cum', 'total_goal_difference_a']].reset_index(drop = True)

                home_df_v3.columns = ['team', 'point', 'gd']
                away_df_v3.columns = ['team', 'point', 'gd']

                home_df_v3['status'] = 'home'
                away_df_v3['status'] = 'away'

                standings_df_v3 = pd.concat(objs = [home_df_v3, away_df_v3], ignore_index = True)
                standings_df_v3.sort_values(by = ['point', 'gd', 'team'], ascending = [False, False, True], inplace = True)
                standings_df_v3.reset_index(drop = True, inplace = True)
                standings_df_v3['position'] = list(range(1, standings_df_v3.shape[0] + 1))
                standings_df_v3.drop_duplicates(subset = 'team', inplace = True, ignore_index = True)

                assert standings_df_v3.shape[0] == standings_df_v3.team.nunique()
                extension_df_v2 = standings_df_v3.loc[standings_df_v3.team.isin(values = lacking_team_v2)]

                if extension_df_v2.shape[0] != 0:
                    extension_df = pd.concat(objs = [extension_df, extension_df_v2], ignore_index = True)
                else:
                    pass

                previous_week += 1

                if extension_df.shape[0] == len(lacking_teams):
                    break

            standings_df = pd.concat(objs = [standings_df, extension_df])
            standings_df.sort_values(by = ['point', 'gd', 'team'], ascending = [False, False, True], inplace = True)
            standings_df.reset_index(drop = True, inplace = True)
            standings_df.drop_duplicates(subset = 'team', inplace = True, ignore_index = True)
            standings_df['position'] = list(range(1, standings_df.shape[0] + 1))

            assert standings_df.shape[0] == standings_df.team.nunique()

            home_team_positions = standings_df.loc[standings_df.status == 'home'][['team', 'position']].reset_index(drop = True)
            away_team_positions = standings_df.loc[standings_df.status == 'away'][['team', 'position']].reset_index(drop = True)
            
        for team in data_frame.loc[data_frame.match_week == match_week, 'home_team'].tolist():
            position = standings_df.loc[(standings_df.status == 'home') & (standings_df.team == team), 'position'].values
            
            if len(position) == 0:
                position = away_team_positions.loc[away_team_positions.team == team, 'position'].values[0]
            else:
                position = position[0]
            
            data_frame.loc[(data_frame.home_team == team) & (data_frame.match_week == match_week), 'h_position'] = position
            
        for team in data_frame.loc[data_frame.match_week == match_week, 'away_team'].tolist():
            position = standings_df.loc[(standings_df.status == 'away') & (standings_df.team == team), 'position'].values
            
            if len(position) == 0:
                position = home_team_positions.loc[home_team_positions.team == team, 'position'].values[0]
            else:
                position = position[0]
            
            data_frame.loc[(data_frame.away_team == team) & (data_frame.match_week == match_week), 'a_position'] = position
            
    data_frame[['h_position', 'a_position']] = data_frame[['h_position', 'a_position']].applymap(func = lambda x: int(x))
    
    assert data_frame.loc[data_frame.h_position == data_frame.a_position].shape[0] == 0

    return data_frame

# Defining a function to apply feature engineering
def apply_feature_engineering(data_frame = None):
    # Replacing the dash with forward slash
    season = data_frame.season.unique()[0]

    # Loading the raw data
    df = data_frame.copy()

    # Applying the functions
    df = create_preliminary_variables(data_frame = df, season = season)
    df = create_avg_shots_on_target_last_3_and_5_h(data_frame = df)
    df = create_avg_shots_on_target_last_3_and_5_a(data_frame = df)
    df = create_avg_fouls_conceded_last_3_and_5_h(data_frame = df)
    df = create_avg_fouls_conceded_last_3_and_5_a(data_frame = df)
    df = create_avg_yellow_cards_last_3_and_5_h(data_frame = df)
    df = create_avg_yellow_cards_last_3_and_5_a(data_frame = df)
    df = create_avg_possession_last_3_and_5_h(data_frame = df)
    df = create_avg_possession_last_3_and_5_a(data_frame = df)
    df = create_avg_clearances_last_3_and_5_h(data_frame = df)
    df = create_avg_clearances_last_3_and_5_a(data_frame = df)
    df = create_cumulative_shots_on_target_h(data_frame = df)
    df = create_cumulative_shots_on_target_a(data_frame = df)
    df = create_total_avg_shots_on_target_last_3(data_frame = df)
    df = create_total_avg_shots_on_target_last_5(data_frame = df)
    df = create_total_avg_fouls_conceded_last_3(data_frame = df)
    df = create_total_avg_fouls_conceded_last_5(data_frame = df)
    df = create_total_avg_yellow_cards_last_3(data_frame = df)
    df = create_total_avg_yellow_cards_last_5(data_frame = df)
    df = create_total_avg_clearances_last_3(data_frame = df)
    df = create_total_avg_clearances_last_5(data_frame = df)
    df = create_avg_offsides_last_3_and_5_h(data_frame = df)
    df = create_avg_offsides_last_3_and_5_a(data_frame = df)
    df = create_cumulative_goals_conceded_h(data_frame = df)
    df = create_cumulative_goals_conceded_a(data_frame = df)
    df = create_cumulative_fouls_conceded_h(data_frame = df)
    df = create_cumulative_fouls_conceded_a(data_frame = df)
    df = create_avg_corners_last_3_and_5_h(data_frame = df)
    df = create_avg_corners_last_3_and_5_a(data_frame = df)
    df = create_avg_touches_last_3_and_5_h(data_frame = df)
    df = create_avg_touches_last_3_and_5_a(data_frame = df)
    df = create_avg_tackles_last_3_and_5_h(data_frame = df)
    df = create_avg_tackles_last_3_and_5_a(data_frame = df)
    df = create_total_avg_offsides_last_3(data_frame = df)
    df = create_total_avg_offsides_last_5(data_frame = df)
    df = create_cumulative_goals_scored_h(data_frame = df)
    df = create_cumulative_goals_scored_a(data_frame = df)
    df = create_cumulative_yellow_cards_h(data_frame = df)
    df = create_cumulative_yellow_cards_a(data_frame = df)
    df = create_avg_passes_last_3_and_5_h(data_frame = df)
    df = create_avg_passes_last_3_and_5_a(data_frame = df)
    df = create_total_avg_corners_last_3(data_frame = df)
    df = create_total_avg_corners_last_5(data_frame = df)
    df = create_total_avg_tackles_last_3(data_frame = df)
    df = create_total_avg_tackles_last_5(data_frame = df)
    df = create_total_avg_touches_last_3(data_frame = df)
    df = create_total_avg_touches_last_5(data_frame = df)
    df = create_avg_shots_last_3_and_5_h(data_frame = df)
    df = create_avg_shots_last_3_and_5_a(data_frame = df)
    df = create_cumulative_possession_h(data_frame = df)
    df = create_cumulative_possession_a(data_frame = df)
    df = create_cumulative_clearances_h(data_frame = df)
    df = create_cumulative_clearances_a(data_frame = df)
    df = create_total_avg_passes_last_3(data_frame = df)
    df = create_total_avg_passes_last_5(data_frame = df)
    df = create_total_n_matches_played(data_frame = df)
    df = create_cumulative_offsides_h(data_frame = df)
    df = create_cumulative_offsides_a(data_frame = df)
    df = create_cumulative_touches_h(data_frame = df)
    df = create_cumulative_touches_a(data_frame = df)
    df = create_cumulative_tackles_h(data_frame = df)
    df = create_cumulative_tackles_a(data_frame = df)
    df = create_cumulative_corners_h(data_frame = df)
    df = create_cumulative_corners_a(data_frame = df)
    df = create_cumulative_passes_h(data_frame = df)
    df = create_cumulative_passes_a(data_frame = df)
    df = create_cumulative_points_h(data_frame = df)
    df = create_cumulative_points_a(data_frame = df)
    df = create_cumulative_shots_h(data_frame = df)
    df = create_cumulative_shots_a(data_frame = df)
    df = create_total_avg_shots_last_3(data_frame = df)
    df = create_total_avg_shots_last_5(data_frame = df)
    df = create_n_matches_played(data_frame = df)
    df = create_max_and_dropped_points(data_frame = df)
    df = create_total_goals_conceded(data_frame = df)
    df = create_total_avg_possession_last_3(data_frame = df)
    df = create_total_avg_possession_last_5(data_frame = df)
    df = create_total_avg_shots_on_target(data_frame = df)
    df = create_total_avg_fouls_conceded(data_frame = df)
    df = create_total_avg_yellow_cards(data_frame = df)
    df = create_total_avg_clearances(data_frame = df)
    df = create_total_avg_possesion(data_frame = df)
    df = create_total_avg_offsides(data_frame = df)
    df = create_total_goals_scored(data_frame = df)
    df = create_total_avg_corners(data_frame = df)
    df = create_total_avg_touches(data_frame = df)
    df = create_total_avg_tackles(data_frame = df)
    df = create_total_avg_passes(data_frame = df)
    df = create_total_points_cum(data_frame = df)
    df = create_total_max_and_dropped_points(data_frame = df)
    df = create_goal_difference(data_frame = df)
    df = create_total_avg_shots(data_frame = df)
    df = create_derbies(data_frame = df)
    df = create_league_positions(data_frame = df)

    # Creating a list of reallocated features
    reallocated_features = ['season', 'match_week', 'match_date', 'month', 'day', 'weekday', 'referee', 'home_team', 'away_team', 'stadium', 'attendance',
                            'h_position', 'a_position', 'goals_h', 'goals_a', 'possession_h', 'possession_a', 'shots_on_target_h', 'shots_on_target_a', 'shots_h', 'shots_a', 'touches_h',
                            'touches_a', 'passes_h', 'passes_a', 'tackles_h', 'tackles_a', 'clearances_h', 'clearances_a', 'corners_h', 'corners_a', 'offsides_h',
                            'offsides_a', 'yellow_cards_h', 'yellow_cards_a', 'red_cards_h', 'red_cards_a', 'fouls_conceded_h', 'fouls_conceded_a', 
                            'formation_h', 'formation_a', 'result_h', 'result_a', 'points_h', 'points_a', 'total_n_matches_played_h',
                            'total_n_matches_played_a', 'total_max_points_h', 'total_max_points_a', 'total_points_h_cum', 'total_points_a_cum', 
                            'total_points_dropped_h', 'total_points_dropped_a', 'total_goals_scored_h', 'total_goals_scored_a', 'total_goals_conceded_h', 
                            'total_goals_conceded_a', 'total_avg_possession_h', 'total_avg_possession_a', 'total_avg_possession_last_3_h', 
                            'total_avg_possession_last_3_a', 'total_avg_possession_last_5_h', 'total_avg_possession_last_5_a', 'total_avg_shots_on_target_h', 
                            'total_avg_shots_on_target_a', 'total_avg_shots_on_target_last_3_h',
                            'total_avg_shots_on_target_last_3_a', 'total_avg_shots_on_target_last_5_h', 'total_avg_shots_on_target_last_5_a', 'total_avg_shots_h',
                            'total_avg_shots_a', 'total_avg_shots_last_3_h', 'total_avg_shots_last_3_a', 'total_avg_shots_last_5_h', 'total_avg_shots_last_5_a',
                            'total_avg_touches_h', 'total_avg_touches_a', 'total_avg_touches_last_3_h', 'total_avg_touches_last_3_a', 'total_avg_touches_last_5_h',
                            'total_avg_touches_last_5_a', 'total_avg_passes_h', 'total_avg_passes_a', 'total_avg_passes_last_3_h', 'total_avg_passes_last_3_a',
                            'total_avg_passes_last_5_h', 'total_avg_passes_last_5_a', 'total_avg_tackles_h', 'total_avg_tackles_a', 'total_avg_tackles_last_3_h',
                            'total_avg_tackles_last_3_a', 'total_avg_tackles_last_5_h', 'total_avg_tackles_last_5_a', 'total_avg_clearances_h', 
                            'total_avg_clearances_a', 'total_avg_clearances_last_3_h', 'total_avg_clearances_last_3_a', 'total_avg_clearances_last_5_h',
                            'total_avg_clearances_last_5_a', 'total_avg_corners_h', 'total_avg_corners_a', 'total_avg_corners_last_3_h', 'total_avg_corners_last_3_a',
                            'total_avg_corners_last_5_h', 'total_avg_corners_last_5_a', 'total_avg_offsides_h', 'total_avg_offsides_a', 'total_avg_offsides_last_3_h',
                            'total_avg_offsides_last_3_a', 'total_avg_offsides_last_5_h', 'total_avg_offsides_last_5_a', 'total_avg_yellow_cards_h', 
                            'total_avg_yellow_cards_a', 'total_avg_yellow_cards_last_3_h', 'total_avg_yellow_cards_last_3_a', 'total_avg_yellow_cards_last_5_h',
                            'total_avg_yellow_cards_last_5_a', 'total_avg_fouls_conceded_h', 'total_avg_fouls_conceded_a', 'total_avg_fouls_conceded_last_3_h',
                            'total_avg_fouls_conceded_last_3_a', 'total_avg_fouls_conceded_last_5_h', 'total_avg_fouls_conceded_last_5_a', 'n_matches_played_h',
                            'n_matches_played_a', 'max_points_h', 'max_points_a', 'points_h_cum', 'points_a_cum', 'points_dropped_h', 'points_dropped_a',
                            'goals_scored_h_cum', 'goals_scored_a_cum', 'goals_conceded_h_cum', 'goals_conceded_a_cum', 'avg_possession_h',
                            'avg_possession_a', 'avg_possession_last_3_h', 'avg_possession_last_3_a', 'avg_possession_last_5_h', 'avg_possession_last_5_a', 
                            'avg_shots_on_target_h', 'avg_shots_on_target_a', 'avg_shots_on_target_last_3_h', 'avg_shots_on_target_last_3_a', 
                            'avg_shots_on_target_last_5_h', 'avg_shots_on_target_last_5_a', 'avg_shots_h', 'avg_shots_a', 'avg_shots_last_3_h', 
                            'avg_shots_last_3_a', 'avg_shots_last_5_h', 'avg_shots_last_5_a', 'avg_touches_h', 'avg_touches_a', 'avg_touches_last_3_h', 
                            'avg_touches_last_3_a', 'avg_touches_last_5_h', 'avg_touches_last_5_a', 'avg_passes_h', 'avg_passes_a', 'avg_passes_last_3_h', 
                            'avg_passes_last_3_a', 'avg_passes_last_5_h', 'avg_passes_last_5_a', 'avg_tackles_h', 'avg_tackles_a', 'avg_tackles_last_3_h',
                            'avg_tackles_last_3_a', 'avg_tackles_last_5_h', 'avg_tackles_last_5_a', 'avg_clearances_h', 'avg_clearances_a', 
                            'avg_clearances_last_3_h', 'avg_clearances_last_3_a', 'avg_clearances_last_5_h', 'avg_clearances_last_5_a', 'avg_corners_h', 
                            'avg_corners_a', 'avg_corners_last_3_h', 'avg_corners_last_3_a', 'avg_corners_last_5_h', 'avg_corners_last_5_a', 'avg_offsides_h', 
                            'avg_offsides_a', 'avg_offsides_last_3_h', 'avg_offsides_last_3_a', 'avg_offsides_last_5_h', 'avg_offsides_last_5_a', 
                            'avg_yellow_cards_h', 'avg_yellow_cards_a', 'avg_yellow_cards_last_3_h', 'avg_yellow_cards_last_3_a', 'avg_yellow_cards_last_5_h',
                            'avg_yellow_cards_last_5_a', 'avg_fouls_conceded_h', 'avg_fouls_conceded_a', 'avg_fouls_conceded_last_3_h','avg_fouls_conceded_last_3_a', 
                            'avg_fouls_conceded_last_5_h', 'avg_fouls_conceded_last_5_a', 'is_boxing_day', 'finished_top_4_last_season_h', 
                            'finished_top_4_last_season_a', 'won_carabao_cup_last_season_h', 'won_carabao_cup_last_season_a', 'won_fa_cup_last_season_h', 
                            'won_fa_cup_last_season_a', 'won_epl_last_season_h', 'won_epl_last_season_a', 'was_in_ucl_last_season_h', 'was_in_ucl_last_season_a', 
                            'was_in_uel_last_season_h', 'was_in_uel_last_season_a', 'is_in_ucl_this_season_h', 'is_in_ucl_this_season_a', 'is_in_uel_this_season_h', 
                            'is_in_uel_this_season_a', 'traditional_top_6_h', 'traditional_top_6_a', 'newly_promoted_h', 'newly_promoted_a', 'total_goal_difference_h',
                            'total_goal_difference_a', 'goal_difference_h', 'goal_difference_a', 'positive_total_goal_difference_h', 'positive_total_goal_difference_a',                                                               'positive_goal_difference_h', 'positive_goal_difference_a', 'is_derby', 'derby_name', 'ground_truth', 'home_win', 'draw', 'away_win', 'link']

    # Reallocating the features
    df = df[reallocated_features]

    # Returning the data frame
    return df

# Running the script
if __name__ == '__main__':
    # Calling the function to apply feature engineering
    apply_feature_engineering()