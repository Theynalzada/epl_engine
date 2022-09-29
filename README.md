# Data Science Project: Premier League Engine

## Project Description
The goal of the project is to make accurate and precise predictions for the **English Premier League (EPL)** matches. The motivation behind the project actually came from my passion for football and taking into account that I am a huge **Manchester United** fan, choosing EPL to start the project was inevitable. This project roughly took eight months to complete because of its scope and what I was trying to achieve. 

## Data Collection
Considering the data I was looking for was not available, I built a web scraping bot which I refer it as scraper using **Selenium** framework in **Pyhon** programming language to scrape data from the official [website](https://www.premierleague.com) of EPL. The **2016/17** season for EPL was a turning point in many ways but mostly due to reputation of managers and the statue of the clubs they were appointed to. The managers such as Jose Mourinho (Manchester United), Pep Guardiola (Manchester City) and Antonio Conte (Chelsea) were introduced to EPL where Arsene Wenger (Arsenal), Jurgen Klopp (Liverpool) and Mauricio Pochettino (Spurs) were already operating. So, I decided to start scraping data from 2016/17 season up to the 2022/23 (*current season*) so that the data includes the most recent events in the league. The scraper initially scrapes **40** variables for each season which are as follow.

1. **season** - A season in which a match took place
2. **home_team** - A home team in a match
3. **away_team** - An away team in a match
4. **goals_h** - The number of goals scored by a home team in a match
5. **goals_a** - The number of goals scored by an away team in a match
6. **stadium** - The name of a stadium in which a match took place
7. **link** - The link of a match
8. **match_week** - The match week in which a match took place
9. **match_date** - The date of a match
10. **month** - The month of a match directly generated from the date of a match
11. **day** - The day of a match directly generated from the date of a match
12. **weekday** - The day of the week directly generated from the date of a match
13. **referee** - The name of a referee who officiated a match
14. **attendance** - The number of fans who attended a match
15. **possession_h** - The ball possession for a home team at the end of a match
16. **possession_a** - The ball possession for an away team at the end of a match 
17. **shots_on_target_h** - The number of shots on target by a home team at the end of a match
18. **shots_on_target_a** - The number of shots on target by an away team at the end of a match
19. **shots_h** - The number of shots by a home team at the end of a match
20. **shots_a** - The number of shots by an away team at the end of a match
21. **touches_h** - The number of touches by a home team at the end of a match
22. **touches_a** - The number of touches by an away team at the end of a match
23. **passes_h** - The number of passes by a home team at the end of a match
24. **passes_a** - The number of passes by an away team at the end of a match
25. **tackles_h** - The number of tackles by a home team at the end of a match
26. **tackles_a** - The number of tackles by an away team at the end of a match
27. **clearances_h** - The number of clearances by a home team at the end of a match
28. **clearances_a** - The number of clearances by an away team at the end of a match
29. **corners_h** - The number of corners by a home team at the end of a match
30. **corners_a** - The number of corners by an away team at the end of a match
31. **offsides_h** - The number of offsides by a home team at the end of a match
32. **offsides_a** - The number of offsides by an away team at the end of a match
33. **yellow_cards_h** - The number of yellow cards by a home team at the end of a match
34. **yellow_cards_a** - The number of yellow cards by an away team at the end of a match
35. **red_cards_h** - The number of red cards by a home team at the end of a match
36. **red_cards_a** - The number of red cards by an away team at the end of a match
37. **fouls_conceded_h** - The number of fouls conceded by a home team at the end of a match
38. **fouls_conceded_a** - The number of fouls conceded by an away team at the end of a match
39. **formation_h** - The formation used by a home team in a match 
40. **formation_a** - The formation used by an away team in a match 

All these variables contain aggregated data which is finalised after a final whistle. The scraped data for each season is stored as a separate csv file. 

## Target Selection
As there are three possible outcomes of any football match, it is easy to to frame the problem as a multiclass, however, I decided to convert it  from a multiclass to a binary problem, because instead of a single model that predicts all possible outcomes of a football match I wanted seperated models for each outcome. In addition to this, another reason why I decided to convert it is based on some algorithms such as Logistic Regression, Support Vector Machine and Multi Layer Perceptron not being compatible with multiclass approach but binary. Converting a multiclass into a binary problem involves two separate techniques

1. **One versus Rest (OVR)** - This technique which is also known as **One versus All (OVA)** is used when a negative class contains the observations of every other class that does not belong to a positive class. The outcome is based on the maximum probability which means that a prediction with a maximum probability is taken as an output. The major advantage of this approach is based on the fact you do not need to build separate models for all possible combination of unique classes in a dependent variable. This is usually the prefered approach since it is less time consuming. In case this approach is implemented there would be three models with following target variables.

    | Models| Positive Class | Negative Class |
    | -------- | -------- | -------- |
    | First Model     | Win     | Loss or Draw
    Second Model|Loss|Win or Draw
    Third Model|Draw|Win or Loss

2. **One versus One (OVO)** - Unlike previous, this approach requires to build seperate models for each possible combination of unique classes in a dependent variable. The major disadvantage of this technique is due to the fact that it might be very time consuming in case there are many unique classes in a dependent variable. In addition the outcome is selected based on voting system which means that all the models make predictions and the class with the most vote is choosen as the outcome. In case this approach is implemented there would be three models with following target variables.
    | Models| Positive Class | Negative Class |
    | -------- | -------- | -------- |
    | First Model     | Win     | Loss
    Second Model|Win|Draw
    Third Model|Loss|Win
    Fourth Model|Loss|Draw
    Fifth Model|Draw|Win
    Sixth Model|Draw|Loss

I proceeded with the former technique to build three separate models, one for each outcome. There are two types of predictions that can be made for a football match. 
1. **Online prediction** - This technique uses in game live statistics to predict an outcome of a football match. The major idea behind is based on a fixed amount of predictions at a particular time interval. Without taking extra time into account a duration of a football match is 90 minutes. There are various time partitions such as 5, 10, 15 minutes that can be used to make predictions while the number of predictions decrease when the time partition increases.

    - **The Number of Predictions** = (90 / Time Partition) - 1

    Based on the formula the number of predictions should be like this.

    - The number of predictions with 5 minutes partition is **17**.
    - The number of predictions with 10 minutes partition is **8**.
    - The number of predictions with 15 minutes partition is **5**.

    Taking 15 minutes partition is ideal as there will be six separate models based on following target
    
    1. **1 - 15** -> A multiclass model will be trained on historical data aggregated in the first 15 minutes of a football match to predict the outcome.
    2. **16 - 30** -> A multiclass model will be trained on historical data aggregated from minute 16 to minute 30 of a football match to predict the outcome.
    3. **31 - 45** -> A multiclass model will be trained on historical data aggregated from minute 31 to minute 45 of a football match to predict the outcome.
    4. **46 - 60** -> A multiclass model will be trained on historical data aggregated from minute 46 to minute 60 of a football match to predict the outcome.
    5. **61 - 75** -> A multiclass model will be trained on historical data aggregated from minute 61 to minute 75 of a football match to predict the outcome.

    In this kind of approach the confidence of a model for a given prediction increases when the time for a final whistle decreases. Let's take a look at Manchester United vs Arsenal match that took place in 2022-09-04 as an example. The score was 0-0 until the minute 35 and by that time a model would have made 2 predictions, one in minute 15 and the other one in minute 30. Since no team had found a breakthrough goal a model's probability for a given prediction would not be that accurate. Then in minute 35 Manchested United finally found the breakthrough goal which was in the third time partition and 10 minutes later the model would have made the third prediction at half time but with increased probability for a given prediction. Arsenal equalized in minute 60 and the model would have made the fourth prediction in which the probability of Manchester United beating Arsenal would have decreased and the probability of Arsenal defeating Manchester United away from home would be higher. Then in minute 66 and 75 the red devils scored their second and third goal and the probability of Manchester United defeating Arsenal at Old Trafford would have been much higher. This is the workflow of the online prediction. In order to build a model to make prediction online there needs to be a minute by minute data for each match which is much harder to collect.

2. **Batch prediction** - Unlike online prediction batch prediction for this particular project is based on the idea of predicting the outcome of a football match before that particular match took place. By this logic, the features the scraper scraped cannot be used since they are derived from in game statistics. Primary approach when building a batch model for this particular project is based on teaching a model the historical behavior of teams. My initial idea had always been to build a model that was capable of predicting the outcome of a match beforehand which makes it much harder for two primary reasons.

    1. A model will not be using in game statistics but historical features which will be aggregation of various parameters of previous matches.
    2. Unexpected occations such as red cards, major players injured during a match, last minute penalties, virtual assistant referee (VAR) involvement might drastically change the final outcome of a match. Considering the fact that a batch model will not be using the in game statistics, it will be unaware of these unexpected occations.

## Feature Engineering
Considering the fact that I was going to build a model to predict the outcome of a football match before it even took place, I had to do some feature engineering. I created a Python script called **feature_engineering.py** which creates **189** features which are following.

---

1. **is_boxing_day** - Whether or not a match took place on **boxing day** which is a unique fixture for EPL
2. **finished_top_4_last_season_h** - Whether or not a home team finished top four last season
3. **finished_top_4_last_season_a** - Whether or not an away team finished top four last season
4. **won_carabao_cup_last_season_h** - Whether or not a home team won Carabao Cup last season
5. **won_carabao_cup_last_season_a** - Whether or not an away team won Carabao Cup last season
6. **was_in_ucl_last_season_h** - Whether or not a home team was in Uefa Champions League (UCL) last season
7. **was_in_ucl_last_season_a** - Whether or not an away team was in UCL last season
8. **was_in_uel_last_season_h** - Whether or not a home team was in Uefa Europa League (UEL) last season
9. **was_in_uel_last_season_a** - Whether or not an away team was in UEL last season
10. **is_in_ucl_this_season_h** - Whether or not a home team is in UCL this season
11. **is_in_ucl_this_season_a** - Whether or not an away team is in UCL this season
12. **is_in_uel_this_season_h** - Whether or not a home team is in UEL this season
13. **is_in_uel_this_season_a** - Whether or not an away team is in UEL this season
14. **won_fa_cup_last_season_h** - Whether or not a home won FA Cup last season
15. **won_fa_cup_last_season_a** - Whether or not an away won FA Cup last season
16. **traditional_top_6_h** - Whether or not a home team is a traditional top six club
17. **traditional_top_6_a** - Whether or not an away team is a traditional top six club
18. **won_epl_last_season_h** - Whether or not a home team won English Premier League (EPL) last season
19. **won_epl_last_season_a** - Whether or not an away team won English Premier League (EPL) last season
20. **newly_promoted_h** - Whether or not a home team is a newly promoted team
21. **newly_promoted_a** - Whether or not an away team is a newly promoted team
22. **avg_shots_on_target_last_3_h** - Average number of shots on target in the last three home matches for a home team
23. **avg_shots_on_target_last_5_h** - Average number of shots on target in the last five home matches for a home team
24. **avg_shots_on_target_last_3_a** - Average number of shots on target in the last three away matches for an away team
25. **avg_shots_on_target_last_5_a** - Average number of shots on target in the last five away matches for an away team
26. **avg_fouls_conceded_last_3_h** - Average number of fouls conceded in the last three home matches for a home team
27. **avg_fouls_conceded_last_5_h** - Average number of fouls conceded in the last five home matches for a home team
28. **avg_fouls_conceded_last_3_a** - Average number of fouls conceded in the last three away matches for an away team
29. **avg_fouls_conceded_last_5_a** - Average number of fouls conceded in the last five away matches for an away team
30. **avg_yellow_cards_last_3_h** - Average number of yellow cards received in last three home matches for a home team
31. **avg_yellow_cards_last_5_h** - Average number of yellow cards received in last five home matches for a home team
32. **avg_yellow_cards_last_3_a** - Average number of yellow cards received in last three home matches for an away team
33. **avg_yellow_cards_last_5_a** - Average number of yellow cards received in last five home matches for an away team
34. **avg_possession_last_3_h** - Average ball possession in the last three home matches for a home team
35. **avg_possession_last_5_h** - Average ball possession in the last five home matches for a home team
36. **avg_possession_last_3_a** - Average ball possession in the last three away matches for an away team
37. **avg_possession_last_5_a** - Average ball possession in the last five away matches for an away team
38. **avg_clearances_last_3_h** - Average number of clearances in last three home matches for a home team
39. **avg_clearances_last_5_h** - Average number of clearances in last five home matches for a home team
40. **avg_clearances_last_3_a** - Average number of clearances in last three away matches for an away team
41. **avg_clearances_last_5_a** - Average number of clearances in last five away matches for an away team
42. **avg_shots_on_target_h** - Average shots on target in home matches for a home team
43. **avg_shots_on_target_a** - Average shots on target in away matches for an away team
44. **total_avg_shots_on_target_last_3_h** - Average shots on target in the last three matches for a home team
45. **total_avg_shots_on_target_last_3_a** - Average shots on target in the last three matches for an away team
46. **total_avg_shots_on_target_last_5_h** - Average shots on target in the last five matches for a home team
47. **total_avg_shots_on_target_last_5_a** - Average shots on target in the last five matches for an away team
48. **total_avg_fouls_conceded_last_3_h** - Average number of fouls conceded in the last three matches for a home team
49. **total_avg_fouls_conceded_last_3_a** - Average number of fouls conceded in the last three matches for an away team
50. **total_avg_fouls_conceded_last_5_h** - Average number of fouls conceded in the last five matches for a home team
51. **total_avg_fouls_conceded_last_5_a** - Average number of fouls conceded in the last five matches for an away team
52. **total_avg_yellow_cards_last_3_h** - Average number of yellow cards received in last three matches for a home team
53. **total_avg_yellow_cards_last_3_a** - Average number of yellow cards received in last three matches for an away team
54. **total_avg_yellow_cards_last_5_h** - Average number of yellow cards received in last five matches for a home team
55. **total_avg_yellow_cards_last_5_a** - Average number of yellow cards received in last five matches for an away team
56. **total_avg_clearances_last_3_h** - Average number of clearances in last three matches for a home team
57. **total_avg_clearances_last_3_a** - Average number of clearances in last three matches for an away team
58. **total_avg_clearances_last_5_h** - Average number of clearances in last five matches for a home team
59. **total_avg_clearances_last_5_a** - Average number of clearances in last five matches for an away team
60. **avg_offsides_last_3_h** - Average number of offsides in the last three matches for a home team
61. **avg_offsides_last_3_a** - Average number of offsides in the last three matches for an away team
62. **avg_offsides_last_5_h** - Average number of offsides in the last five matches for a home team
63. **avg_offsides_last_5_a** - Average number of offsides in the last five matches for an away team
64. **goals_conceded_h_cum** - Total number of goals conceded by a home team in home matches
65. **goals_conceded_a_cum** - Total number of goals conceded by an away team in away matches
66. **avg_fouls_conceded_h** - Average number of fouls conceded by a home team in home matches
67. **avg_fouls_conceded_a** - Average number of fouls conceded by an away team in away matches
68. **avg_corners_last_3_h** - Average number of corners in the last three home matches for a home team
69. **avg_corners_last_5_h** - Average number of corners in the last five home matches for a home team
70. **avg_corners_last_3_a** - Average number of corners in the last three home matches for an away team
71. **avg_corners_last_5_a** - Average number of corners in the last five home matches for an away team
72. **avg_touches_last_3_h** - Average number of touches in the last three home matches for a home team
73. **avg_touches_last_5_h** - Average number of touches in the last five home matches for a home team
74. **avg_touches_last_3_a** - Average number of touches in the last three away matches for an away team
75. **avg_touches_last_5_a** - Average number of touches in the last five away matches for an away team
76. **avg_tackles_last_3_h** - Average number of tackles in the last three home matches for a home team
77. **avg_tackles_last_5_h** - Average number of tackles in the last five home matches for a home team
78. **avg_tackles_last_3_a** - Average number of tackles in the last three away matches for an away team
79. **avg_tackles_last_5_a** - Average number of tackles in the last five away matches for an away team
80. **total_avg_offsides_last_3_h** - Total number of offsides by a home team in the last three matches
81. **total_avg_offsides_last_3_a** - Total number of offsides by an away team in the last three matches
82. **total_avg_offsides_last_5_h** - Total number of offsides by a home team in the last five matches
83. **total_avg_offsides_last_5_a** - Total number of offsides by an away team in the last five matches
84. **goals_scored_h_cum** - Total number of goals scored by a home team in home matches
85. **goals_scored_a_cum** - Total number of goals scored by an away team in away matches
86. **avg_yellow_cards_h** - Total number of yellow cards received by a home team in home matches
87. **avg_yellow_cards_a** - Total number of yellow cards received by an away team in away matches
88. **avg_passes_last_3_h** - Average number of passes in the last three home matches for a home team
89. **avg_passes_last_5_h** - Average number of passes in the last five home matches for a home team
90. **avg_passes_last_3_a** - Average number of passes in the last three away matches for an away team
91. **avg_passes_last_5_a** - Average number of passes in the last five away matches for an away team
92. **total_avg_corners_last_3_h** - Average number of corners for a home team in the last three matches
93. **total_avg_corners_last_3_a** - Average number of corners for an away team in the last three matches
94. **total_avg_corners_last_5_h** - Average number of corners for a home team in the last five matches
95. **total_avg_corners_last_5_a** - Average number of corners for an away team in the last five matches
96. **total_avg_tackles_last_3_h** - Average number of tackles for a home team in the last three matches
97. **total_avg_tackles_last_3_a** - Average number of tackles for an away team in the last three matches
98. **total_avg_tackles_last_5_h** - Average number of tackles for a home team in the last five matches
99. **total_avg_tackles_last_5_a** - Average number of tackles for an away team in the last five matches
100. **total_avg_touches_last_3_h** - Average number of touches for a home team in the last three matches
101. **total_avg_touches_last_3_a** - Average number of touches for an away team in the last three matches
102. **total_avg_touches_last_5_h** - Average number of touches for a home team in the last five matches
103. **total_avg_touches_last_5_a** - Average number of touches for an away team in the last five matches
104. **avg_shots_last_3_h** - Average number of shots for a home team in the last three home matches
105. **avg_shots_last_5_h** - Average number of shots for a home team in the last five home matches
106. **avg_shots_last_3_a** - Average number of shots for an away team in the last three away matches
107. **avg_shots_last_5_a** - Average number of shots for an away team in the last five away matches
108. **avg_possession_h** - Average ball possession for a home team in home matches
109. **avg_possession_a** - Average ball possession for an away team in away matches
110. **avg_clearances_h** - Average number of clearances for a home team in home matches
111. **avg_clearances_a** - Average number of clearances for an away team in away matches
112. **total_avg_passes_last_3_h** - Average number of passes for a home team in the last three matches
113. **total_avg_passes_last_3_a** - Average number of passes for an away team in the last three matches
114. **total_avg_passes_last_5_h** - Average number of passes for a home team in the last five matches
115. **total_avg_passes_last_5_a** - Average number of passes for an away team in the last five matches
116. **total_n_matches_played_h** - Total number of matches played by a home team
117. **total_n_matches_played_a** - Total number of matches played by an away team
118. **avg_offsides_h** - Average number of offsides by a home team in home matches
119. **avg_offsides_a** - Average number of offsides by an away team in away matches
120. **avg_touches_h** - Average number of touches by a home team in home matches
121. **avg_touches_a** - Average number of touches by an away team in away matches
122. **avg_tackles_h** - Average number of tackles by a home team in home matches
123. **avg_tackles_a** - Average number of tackles by an away team in away matches
124. **avg_corners_h** - Average number of corners by a home team in home matches
125. **avg_corners_a** - Average number of corners by an away team in away matches
126. **avg_passes_h** - Average number of passes by a home team in home matches
127. **avg_passes_a** - Average number of passes by an away team in away matches
128. **points_h_cum** - Total number of points accumulated by a home team in home matches
129. **points_a_cum** - Total number of points accumulated by an away team in away matches
130. **avg_shots_h** - Average number of shots by a home team in home matches
131. **avg_shots_a** - Average number of shots by an away team in away matches
132. **total_avg_shots_last_3_h** - Average number of shots by a home team in the last three matches
133. **total_avg_shots_last_3_a** - Average number of shots by an away team in the last three matches
134. **total_avg_shots_last_5_h** - Average number of shots by a home team in the last five matches
135. **total_avg_shots_last_5_a** - Average number of shots by an away team in the last five matches
136. **n_matches_played_h** - Total number of home matches for a home team
137. **n_matches_played_a** - Total number of away matches for an home team
138. **max_points_h** - Maximum number of points a home team can get from home matches
139. **max_points_a** - Maximum number of points an away team can get from away matches
140. **points_dropped_h** - Total number of points dropped in home matches for a home team
141. **points_dropped_a** - Total number of points dropped in away matches for an away team
142. **total_goals_conceded_h** - Total number of goals conceded by a home team
143. **total_goals_conceded_a** - Total number of goals conceded by an away team
144. **total_avg_possession_last_3_h** - Average ball possession for a home team in the last three matches
145. **total_avg_possession_last_3_a** - Average ball possession for an away team in the last three matches
146. **total_avg_possession_last_5_h** - Average ball possession for a home team in the last five matches
147. **total_avg_possession_last_5_a** - Average ball possession for an away team in the last five matches
148. **total_avg_shots_on_target_h** - Average number of shots on target for a home team
149. **total_avg_shots_on_target_a** - Average number of shots on target for an away team
150. **total_avg_fouls_conceded_h** - Average number of fouls conceded by a home team
151. **total_avg_fouls_conceded_a** - Average number of fouls conceded by an away team
152. **total_avg_yellow_cards_h** - Average number of yellow cards received by a home team
153. **total_avg_yellow_cards_a** - Average number of yellow cards received by an away team
154. **total_avg_clearances_h** - Average number of clearances for a home team
155. **total_avg_clearances_a** - Average number of clearances for an away team
156. **total_avg_possession_h** - Average ball possession for a home team
157. **total_avg_possession_a** - Average ball possession for an away team
158. **total_avg_offsides_h** - Average number of offsides a home team
159. **total_avg_offsides_a** - Average number of offsides an away team
160. **total_goals_scored_h** - Total number of goals scored by a home team
161. **total_goals_scored_a** - Total number of goals scored by an away team
162. **total_avg_corners_h** - Average number of corners for a home team
163. **total_avg_corners_a** - Average number of corners for an away team
164. **total_avg_touches_h** - Average number of touches for a home team
165. **total_avg_touches_a** - Average number of touches for an away team
166. **total_avg_tackles_h** - Average number of tackles for a home team
167. **total_avg_tackles_a** - Average number of tackles for an away team
168. **total_avg_passes_h** - Average number of passes for a home team
169. **total_avg_passes_a** - Average number of passes for an away team
170. **total_points_h_cum** - Total number of points accumulated by a home team
171. **total_points_a_cum** - Total number of points accumulated by an away team
172. **total_max_points_h** - Maximum number of points a home team can get
173. **total_max_points_a** - Maximum number of points an away team can get
174. **total_points_dropped_h** - Total number of points dropped by a home team
175. **total_points_dropped_a** - Total number of points dropped by an away team
176. **positive_total_goal_difference_h** - Whether or not a home team has a positive goal difference
177. **positive_total_goal_difference_a** - Whether or not an away team has a positive goal difference
178. **positive_goal_difference_h** - Whether or not a home team has a positive goal difference in home matches
179. **positive_goal_difference_a** - Whether or not an away team has a positive goal difference in away matches
180. **total_goal_difference_h** - Total goal difference for a home team
181. **total_goal_difference_a** - Total goal difference for an away team
182. **goal_difference_h** - Total goal difference for a home team in home matches
183. **goal_difference_a** - Total goal difference for an away team in away matches
184. **total_avg_shots_h** - Average number of shots for a home team
185. **total_avg_shots_a** - Average number of shots for an away team
186. **is_derby** - Whether or not a match is a derby
187. **derby_name** - A name of a derby in case a match is a derby
188. **h_position** - A league position of a home team
189. **a_position** - A league position of an away team

---

These features indicate the behavior of teams based on which a batch model will learn the previous behavior to predict the future behavior of a team. After running the feature_engineering.py script, the data for each season with batch features created is stored as a separate csv file. The feature engineered data for each season is then converted into a parquet file. Moreover, I am also planning to add some other features which are realted to clubs' off field activities when retraining the model. The initial list of those features are following.

1. **Net spend in the summer transfer window** - The higher the net spend in the summer transfer window the more ambitious the club is going into the season. Even though a higher net spend does not guarantee results it still provides information to the model about the statue of a club, because the bigger clubs have larger exposure and sponsorship deals to generate more revenue than the smaller clubs.
2. **Club takeover** - It is very important to understand whether or not there has been a takeover for a club in recent history because takeovers usually happen when club is not doing well not only on the pitch but also off the pitch which makes fans very angry at the board for not addressing the issues which eventually leads to takeover. In addition, when the takeover happens, the new board tend to appease the fans and spend big in the early years of management. As an example Saudi Arabia recently bought Newcastle United and they spent over 120 million pounds without selling anyone. This variable might be very valuable to the model as the model would learn patterns about clubs' ambition going into season.
3. **Sacking a manager** - Clubs usually decide to sack managers when a team fails to deliver on the pitch consequently. Football is a results' business and any manager is in danger of being sacked after poor run of form and results. When a new manager is appointed there is a period in football which is called **honeymoon** period that lasts three or five matches maximum in which team overperforms and actually gets results before going back to default settings. The model would learn the current state of a club in case its manager has been sacked in the summer or during a season while predicting increase in performance with a new manager in post.

## Modeling
Considering the fact that it is time based binary classification problem, I did not shuffle the training data since it was more important for the model to learn the behavior in previous seasons to predict into the upcoming season. The training data covers five years of data starting from **2016/17** season up until the end of **2020/21** season while **2021/22** season was used as the test which can also be referred as **out of time (OOT)** samples. There are 20 teams in the division, while a single season lasts 38 weeks and in each week on average there are 10 matches. In a single season there are **380** matches and the training data contains **1900** matches from previous seasons whereas the test set only contains **380** matches as it is a single season. 

Before building a classifier pipeline I created a custom transformer called **FeatureReallocator** which reallocates input features in a certain order and this is the first transformer of the entire pipeline. Then I categorized features into **four** different groups so that I could apply various preprocessing steps to each category separately.

1. Binary features
2. Ordinal features
3. Numeric features
4. Datetime features 

Apart from the datetime features, I created a separate pipeline for each category and the first transformer in each pipeline is **missing value imputation**. Even though there is no missing value present either in the train or the test data, it is always important to include the missing value imputation as the initial layer of the pipeline to handle potential problems in production environment. Since I want the model to understand the importance of league positions before a match took place, I used **ordinal encoder** to give more weights to the teams with higher league positions. 

All the algorithms were used while for the **Win & Loss** model **Support Vector Machine** prevailed as there was neither overfitting nor underfitting problem. Modeling involved following algorithms.

| Algorithms|Win Model|Loss Model|Draw Model|
| -------- | -------- | -------- | -------- |
|Gaussian Naïve Bayes|False|False|False
|Logistic Regression|False|False|False
|Support Vector Machine|True|True|False
|K Nearest Neighbors|False|False|False
|Multi Layer Perceptron|False|False|True
|Decision Tree|False|False|False
|Random Forest|False|False|False
|Adaptive Boosting (AdaBoost)|False|False|False
|Light Gradient Boosted Machine (LightGBM)|False|False|False
|Gradient Boosting (GBM)|False|False|False
|Extreme Gradient Boosting (XGBoost)|False|False|False
|Category Boosting (CatBoost)|False|False|False

The main evaluation metric for the project is **Balanced Accuracy** score which is calculated by this formula.

- **Balanced Accuracy Score** = (Sensitivity + Specificity) / 2

This is the initial architecture of the classifier pipeline for the **Win & Loss** models.

![](https://i.imgur.com/edUlCLv.png)

This is the initial architecture of the classifier pipeline for the **Draw** model.

![](https://i.imgur.com/EpZUs1m.png)

In order to maximize the evaluation metric both on train and test sets I applied probability thresholding between 10% and 90% probabilities. This is an example from the probability thresholding for the **Win** model.

![](https://i.imgur.com/VEqs9oA.jpg)

This is the **confusion matrix**, **Recall & Precision Ratio** for train and test sets based on **Support Vector Machine** algorithm for the **Win** model.

![](https://i.imgur.com/2gsVc5v.png)

![](https://i.imgur.com/t2Xtqnl.png)

This is the **Receiver Operating Characteristics Curve (ROC)** curve for the train and test sets of the **Win** model.

![](https://i.imgur.com/DA2dOqY.jpg)

It would not be the best approach to use this model to predict the outcome of the matches of the current season since the training data should also include the most recent data. Therefore, I retrained the model by including the **2021/22** season to the training set in which case **2022/23** *(current season)* would be the test set. I used **Bayesian Optimization** to find the best hyperparameters for each of the model. In order to create an engine, I combined the models and a prediction with the maximum probability is the outcome of the engine. I have created **five** confidence interval boundaries for the engine predictions which are following.

1. **Very Low** - The outcome of a match with probability lower than **35%**
2. **Low** - The outcome of a match with probability between **35%** (inclusive) and **55%** (exclusive)
3. **Medium** - The outcome of a match with probability between than **55%** (inclusive) and **65%** (exclusive)
4. **High** - The outcome of a match with probability between than **65%** (inclusive) and **85%** (exclusive)
5. **Very High** - The outcome of a match with probability greater equal than **85%**

Even though the engine makes predictions for any match, its performance is evaluted for matches in which the probability is greater equal than **65%**. Current accuracy of the engine on the train and the test set is **79%** which means that on average out of every 10 predictions with probability greater equal than **65%** the eight of those matches are correctly predicted.

![](https://i.imgur.com/gYFf5OR.jpg)

## Deployment
Apart from the primary engine there is also **shadow mode** engine which I built using **Logistic Regression** algorithm. The reason why I built another engine with different algorithm is due to the fact that I want to analyze and compare predictions of the engines and see how the shadow mode engine perform in production environment in comparison to the primary engine. Furthermore, I have also created a streamlit application which has been deployed and currently running on **Heroku** server, however, primary engine is the one that makes predictions in the application.

## Additional Information
I will maintain this project for the years to come and add other functionalities to the engine such as online prediction using in game statistics. In addition, I will also include new variables for the current engine and retrain it. Since the size of the training set is subject to increase each year, the change for the main algorithms used in modeling is expected.