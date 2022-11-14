# Importing Dependencies
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from chromedriver_py import binary_path

import pandas as pd
import numpy as np
import warnings
import time
import yaml
import os

# Filtering potential warnings
warnings.filterwarnings(action = 'ignore')

# Defining a function to load credentials
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

# Assigning dictionary object to a variable
config = load_credentials(filename = '/Users/kzeynalzade/Documents/EPL Redevelopment/epl_engine/Configuration/config.yml')

# Specifying the path for the driver and target URL
DRIVER_PATH = config.get('credentials').get('driver_path')
TARGET_URL = config.get('credentials').get('target_url')

# Adding an option to browse in an incognito mode
options = ChromeOptions()
options.add_argument(argument = '--incognito')

# Assigning the environment key to a variable
service_object = Service(binary_path)

# Defining a function to scrape the data for the last seven seasons
def scrape_data():
    for x in range(17):
        # driver = Chrome(executable_path = DRIVER_PATH, chrome_options = options)
        driver = Chrome(service = service_object, chrome_options = options)
        driver.get(url = TARGET_URL)
        driver.maximize_window()

        time.sleep(5)
        accept_all_cookies_full_xpath = '/html/body/div[2]/div/div/div[1]/div[5]/button[1]'
        WebDriverWait(driver = driver, timeout = 15).until(method = EC.element_to_be_clickable(mark = (By.XPATH, accept_all_cookies_full_xpath))).click()
        
        time.sleep(3)
        logo_xpath = '/html/body/header/div/a'
        WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, logo_xpath))).click()
        
        try:
            time.sleep(3)
            remove_advert = '/html/body/main/div[1]/nav/a[2]'
            WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, remove_advert))).click()
        except:
            pass

        time.sleep(3)
        results_full_xpath = '/html/body/header/div/nav/ul/li[3]/a'
        WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, results_full_xpath))).click()
        
        try:
            time.sleep(3)
            WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, remove_advert))).click()
        except:
            pass

        time.sleep(3)
        driver.execute_script(script = 'window.scrollTo(0, 200);')

        time.sleep(3)
        WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div[3]/div[1]/section/div[3]/div[2]"))).click()
        season = [x for x in driver.find_elements(by = By.CSS_SELECTOR, value = "li[role = 'option']") if x.text != ''][x]

        season.click()

        time.sleep(3)
        scroll = 1
        element = driver.find_element(by = By.TAG_NAME, value = 'body')

        while scroll != 145:
            element.send_keys(Keys.PAGE_DOWN)
            time.sleep(3)
            scroll += 2

        season = driver.find_element(by = By.XPATH, value = "/html/body/main/div[3]/div[1]/section/div[3]/div[2]").text
        teams = driver.find_elements(by = By.CSS_SELECTOR, value = "li[class = 'matchFixtureContainer']")
        links = driver.find_elements(by = By.CSS_SELECTOR, value = "div[class = 'fixture postMatch']")
        stadiums = driver.find_elements(by = By.CSS_SELECTOR, value = "span[class = 'stadiumName']")
        scores = driver.find_elements(by = By.CSS_SELECTOR, value = "span[class = 'score ']")

        home_teams = [home_team.get_attribute(name = 'data-home') for home_team in teams]
        away_teams = [away_team.get_attribute(name = 'data-away') for away_team in teams]
        goals_scored_by_home_team = [int(goal.text.split('-')[0]) for goal in scores]
        goals_scored_by_away_team = [int(goal.text.split('-')[1]) for goal in scores]
        links = ['https:' + link.get_attribute(name = 'data-href') for link in links]
        stadiums = [stadium.text.split(',')[0].strip() for stadium in stadiums]

        scraped_data_v1 = {'season':season, 
                           'home_team':home_teams, 
                           'away_team':away_teams, 
                           'goals_h':goals_scored_by_home_team, 
                           'goals_a':goals_scored_by_away_team, 
                           'stadium':stadiums, 
                           'link':links}

        df = pd.DataFrame(data = scraped_data_v1)

        features = ['match_week', 'match_date', 'month', 'day', 'weekday', 'referee', 'attendance']
        scraped_data_v2 = []

        for link in links:
            driver.get(url = link)
            driver.implicitly_wait(time_to_wait = 3)
            time.sleep(3)

            try:
                attendance = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.CSS_SELECTOR, "div[class = 'attendance hide-m']"))).text.split(': ')[1].replace(',', ''))
            except:
                attendance = np.nan

            match_week = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.CSS_SELECTOR, "div[class = 'long']"))).text.split()[1])
            match_date = pd.to_datetime(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.CSS_SELECTOR, "div[class = 'matchDate renderMatchDateContainer']"))).text)
            referee = WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.CSS_SELECTOR, "div[class = 'referee']"))).text
            weekday = match_date.weekday() + 1
            month = match_date.month
            day = match_date.day

            scraped_data_v2.append([match_week, match_date, month, day, weekday, referee, attendance])

        extension_df = pd.DataFrame(data = scraped_data_v2, columns = features)
        df = pd.concat(objs = [df, extension_df], axis = 1)

        features = ['possession_h', 'possession_a', 'shots_on_target_h', 'shots_on_target_a', 'shots_h', 'shots_a', 'touches_h', 'touches_a', 
                    'passes_h', 'passes_a', 'tackles_h', 'tackles_a', 'clearances_h', 'clearances_a', 'corners_h', 'corners_a', 'offsides_h', 
                    'offsides_a', 'yellow_cards_h', 'yellow_cards_a', 'red_cards_h', 'red_cards_a', 'fouls_conceded_h', 'fouls_conceded_a']

        scraped_data_v3 = []

        for link in links:
            driver.get(url = link)
            driver.implicitly_wait(time_to_wait = 3)

            time.sleep(3)
            driver.execute_script(script = 'window.scrollTo(0, 500)')

            time.sleep(3)
            WebDriverWait(driver = driver, timeout = 20).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[1]/div/div/ul/li[3]"))).click()

            time.sleep(3)
            driver.execute_script(script = 'window.scrollTo(0, 1000)')

            time.sleep(3)
            properties = len(driver.find_element(by = By.CSS_SELECTOR, value = "tbody[class = 'matchCentreStatsContainer']").find_elements(by = By.TAG_NAME, value = 'tr'))

            if properties == 12:
                possession_h = round(number = float(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[1]/td[1]"))).text), ndigits = 1)
                possession_a = round(number = 100 - possession_h, ndigits = 1)
                shots_on_target_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[2]/td[1]"))).text)
                shots_on_target_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[2]/td[3]"))).text)
                shots_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[3]/td[1]"))).text)
                shots_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[3]/td[3]"))).text)
                touches_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[4]/td[1]"))).text)
                touches_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[4]/td[3]"))).text)
                passes_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[5]/td[1]"))).text)
                passes_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[5]/td[3]"))).text)
                tackles_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[6]/td[1]"))).text)
                tackles_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[6]/td[3]"))).text)
                clearances_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[7]/td[1]"))).text)
                clearances_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[7]/td[3]"))).text)
                corners_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[8]/td[1]"))).text)
                corners_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[8]/td[3]"))).text)
                offsides_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[9]/td[1]"))).text)
                offsides_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[9]/td[3]"))).text)
                yellow_cards_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[10]/td[1]"))).text)
                yellow_cards_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[10]/td[3]"))).text)
                red_cards_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[11]/td[1]"))).text)
                red_cards_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[11]/td[3]"))).text)
                fouls_conceded_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[12]/td[1]"))).text)
                fouls_conceded_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[12]/td[3]"))).text)
            elif properties == 11:
                red_cards_h = 0
                red_cards_a = 0
                possession_h = round(number = float(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[1]/td[1]"))).text), ndigits = 1)
                possession_a = round(number = 100 - possession_h, ndigits = 1)
                shots_on_target_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[2]/td[1]"))).text)
                shots_on_target_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[2]/td[3]"))).text)
                shots_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[3]/td[1]"))).text)
                shots_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[3]/td[3]"))).text)
                touches_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[4]/td[1]"))).text)
                touches_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[4]/td[3]"))).text)
                passes_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[5]/td[1]"))).text)
                passes_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[5]/td[3]"))).text)
                tackles_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[6]/td[1]"))).text)
                tackles_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[6]/td[3]"))).text)
                clearances_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[7]/td[1]"))).text)
                clearances_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[7]/td[3]"))).text)
                corners_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[8]/td[1]"))).text)
                corners_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[8]/td[3]"))).text)
                offsides_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[9]/td[1]"))).text)
                offsides_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[9]/td[3]"))).text)
                yellow_cards_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[10]/td[1]"))).text)
                yellow_cards_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[10]/td[3]"))).text)
                fouls_conceded_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[11]/td[1]"))).text)
                fouls_conceded_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[11]/td[3]"))).text)
            elif properties == 10:
                offsides_h = 0
                offsides_a = 0
                red_cards_h = 0
                red_cards_a = 0
                possession_h = round(number = float(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[1]/td[1]"))).text), ndigits = 1)
                possession_a = round(number = 100 - possession_h, ndigits = 1)
                shots_on_target_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[2]/td[1]"))).text)
                shots_on_target_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[2]/td[3]"))).text)
                shots_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[3]/td[1]"))).text)
                shots_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[3]/td[3]"))).text)
                touches_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[4]/td[1]"))).text)
                touches_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[4]/td[3]"))).text)
                passes_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[5]/td[1]"))).text)
                passes_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[5]/td[3]"))).text)
                tackles_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[6]/td[1]"))).text)
                tackles_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[6]/td[3]"))).text)
                clearances_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[7]/td[1]"))).text)
                clearances_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[7]/td[3]"))).text)
                corners_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[8]/td[1]"))).text)
                corners_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[8]/td[3]"))).text)
                yellow_cards_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[9]/td[1]"))).text)
                yellow_cards_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[9]/td[3]"))).text)
                fouls_conceded_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[10]/td[1]"))).text)
                fouls_conceded_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[10]/td[3]"))).text)
            else:
                offsides_h = 0
                offsides_a = 0
                red_cards_h = 0
                red_cards_a = 0
                yellow_cards_h = 0
                yellow_cards_a = 0
                possession_h = round(number = float(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[1]/td[1]"))).text), ndigits = 1)
                possession_a = round(number = 100 - possession_h, ndigits = 1)
                shots_on_target_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[2]/td[1]"))).text)
                shots_on_target_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[2]/td[3]"))).text)
                shots_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[3]/td[1]"))).text)
                shots_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[3]/td[3]"))).text)
                touches_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[4]/td[1]"))).text)
                touches_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[4]/td[3]"))).text)
                passes_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[5]/td[1]"))).text)
                passes_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[5]/td[3]"))).text)
                tackles_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[6]/td[1]"))).text)
                tackles_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[6]/td[3]"))).text)
                clearances_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[7]/td[1]"))).text)
                clearances_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[7]/td[3]"))).text)
                corners_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[8]/td[1]"))).text)
                corners_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[8]/td[3]"))).text)
                fouls_conceded_h = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[9]/td[1]"))).text)
                fouls_conceded_a = int(WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[3]/div[2]/div[2]/table/tbody/tr[9]/td[3]"))).text)

            scraped_data_v3.append([possession_h, possession_a, shots_on_target_h, shots_on_target_a, shots_h, shots_a,
                                    touches_h, touches_a, passes_h, passes_a, tackles_h, tackles_a, clearances_h, clearances_a,
                                    corners_h, corners_a, offsides_h, offsides_a, yellow_cards_h, yellow_cards_a, 
                                    red_cards_h, red_cards_a, fouls_conceded_h, fouls_conceded_a])

        extension_df_2 = pd.DataFrame(data = scraped_data_v3, columns = features)
        df = pd.concat(objs = [df, extension_df_2], axis = 1)

        features = ['formation_h', 'formation_a']

        scraped_data_v4 = []

        for link in links:
            driver.get(url = link)
            driver.implicitly_wait(time_to_wait = 3)

            time.sleep(3)
            driver.execute_script(script = 'window.scrollTo(0, 500)')

            time.sleep(3)
            WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[1]/div/div/ul/li[2]"))).click()

            time.sleep(3)

            try:
                formation_h = WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[2]/div/div/div[1]/div/header/div/strong"))).text
                formation_a = WebDriverWait(driver = driver, timeout = 10).until(method = EC.element_to_be_clickable(mark = (By.XPATH, "/html/body/main/div/section[2]/div[2]/div[2]/div[2]/section[2]/div/div/div[3]/div/header/div/strong"))).text
            except:
                formation_h = np.nan
                formation_a = np.nan

            scraped_data_v4.append([formation_h, formation_a])

        extension_df_3 = pd.DataFrame(data = scraped_data_v4, columns = features)
        df = pd.concat(objs = [df, extension_df_3], axis = 1)
        season = df.season.unique()[0].replace('/', '-')
        df.to_csv(path_or_buf = f'/Users/kzeynalzade/Documents/EPL Redevelopment/epl_engine/Data/Unprocessed data/{season}_unprocessed.csv', index = False)

        print(f'Data for {season} season has been scraped successfully!')

        driver.close()

# Running the script
if __name__ == '__main__':
    # Calling the function
    scrape_data()