# Data Science Project: Premier League Engine

![](https://i.imgur.com/E56czoZ.jpg)

## Project Description
The goal of the project is to make accurate and precise predictions for the **English Premier League (EPL)** matches. The motivation behind the project actually came from my passion for football and taking into account that I am a huge **Manchester United** fan, choosing the EPL to start the project was inevitable. This project roughly took eight months to complete because of its scope and what I was trying to achieve. 

## Data Collection
Considering the data I was looking for was not available, I built a web scraping bot which I refer it as ***Scraper*** using **Selenium** framework in **Pyhon** programming language to scrape data from the official [website](https://www.premierleague.com) of the EPL. Taking into account that in game statistics for matches had been stored since 2006/07 season, I scraped all the data available from 2006/07 season. The bot initially scrapes **40** variables for each season which are as follow.

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

    In this kind of approach the confidence of a model for a given prediction increases when the time for a final whistle decreases. Let's take a look at Manchester United vs Arsenal match that took place in 2022-09-04 as an example. The score was 0-0 until the minute 35 and by that time a model would have made 2 predictions, one in minute 15 and the other one in minute 30. Since no team had found a breakthrough goal a model's probability for a given prediction would not be that accurate. Then in minute 35 Manchested United finally found the breakthrough goal which was in the third time partition and 10 minutes later the model would have made the third prediction at half time but with increased probability for a given prediction. Arsenal equalized in minute 60 and the model would have made the fourth prediction in which the probability of Manchester United beating Arsenal would have decreased and the probability of Arsenal defeating Manchester United away from home would be higher. Then in minute 66 and 75 the red devils scored their second and third goal and the probability of Manchester United defeating Arsenal at Old Trafford would have been much higher. This is the workflow of the online prediction. In order to build a model to make prediction online there needs to be a minute by minute data also known as **events data** for each match which is much harder to collect.
    
2. **Batch prediction** - Unlike online prediction batch prediction for this particular project is based on the idea of predicting the outcome of a football match before that particular match took place. By this logic, the features the scraper scraped cannot be used since they are derived from in game statistics. Primary approach when building a batch model for this particular project is based on teaching a model the historical behavior of teams. My initial idea had always been to build a model that was capable of predicting the outcome of a match beforehand which makes it much harder for two primary reasons.

    1. A model will not be using in game statistics but historical features which will be aggregation of various parameters of previous matches.
    2. Unexpected occations such as red cards, major players injured during a match, last minute penalties, virtual assistant referee (VAR) involvement might drastically change the final outcome of a match. Considering the fact that a batch model will not be using the in game statistics, it will be unaware of these unexpected occations.

## Feature Engineering
Considering the fact that I was going to build a model to predict the outcome of a football match before it even took place, I had to do some feature engineering. I created a Python script called **feature_engineering.py** which creates **283** features which are following.

---

1. **is_boxing_day** - Whether or not a match is played on a boxing day
2. **finished_top_4_last_season_h** - Whether or not a home team finished top four last season
3. **finished_top_4_last_season_a** - Whether or not an away team finished top four last season
4. **won_carabao_cup_last_season_h** - Whether or not a home team won Carabao cup last season
5. **won_carabao_cup_last_season_a** - Whether or not an away team won Carabao cup last season
6. **won_fa_cup_last_season_h** - Whether or not a home team won FA cup last season
7. **won_fa_cup_last_season_a** - Whether or not an away team won FA cup last season
8. **won_epl_cup_last_season_h** - Whether or not a home team won the EPL last season
9. **won_epl_cup_last_season_a** - Whether or not an away team won the EPL last season
10. **was_in_ucl_last_season_h** - Whether or not a home team was in Uefa Champions League last season
11. **was_in_ucl_last_season_a** - Whether or not an away team was in Uefa Champions League last season
12. **was_in_uel_last_season_h** - Whether or not a home team was in Uefa Europa League last season
13. **was_in_uel_last_season_a** - Whether or not a home team was in Uefa Europa League last season
14. **is_in_ucl_last_season_h** - Whether or not a home team is in Uefa Champions League this season
15. **is_in_ucl_last_season_a** - Whether or not an away team is in Uefa Champions League this season
16. **is_in_uel_last_season_h** - Whether or not a home team is in Uefa Europa League this season
17. **is_in_uel_last_season_a** - Whether or not an away team is in Uefa Europa League last season
18. **traditional_top_6_h** - Whether or not a home team is a traditional top six club
19. **traditional_top_6_a** - Whether or not an away team is a traditional top six club
20. **newly_promoted_h** - Whether or not a home team is a newly promoted team
21. **newly_promoted_a** - Whether or not an away team is a newly promoted team
22. **positive_total_goal_difference_h** - Whether or not a home team has a positive goal difference
23. **positive_total_goal_difference_a** - Whether or not an away team has a positive goal difference
24. **positive_goal_difference_h** - Whether or not a home team has a positive goal difference in home matches
25. **positive_goal_difference_a** - Whether or not an away team has a positive goal difference in away matches
26. **has_been_a_ucl_winner_h** - Whether or not a home team has won the Uefa Champions League at least once
27. **has_been_a_ucl_winner_a** - Whether or not an away team has won the Uefa Champions League at least once
28. **has_been_an_epl_winner_h** - Whether or not a home team has won the EPL at least once
29. **has_been_an_epl_winner_a** - Whether or not an away team has won the EPL at least once
30. **is_derby** - Whether or not a match is derby
31. **club_tier_h** - A tier of a home team based on trophies
32. **club_tier_a** - A tier of an away team based on trophies
33. **h_position** - A league position of a home team
34. **a_position** - A league position of an away team
35. **streak_h** - Form of a home team based on the last five matches
36. **streak_a** - Form of an away team based on the last five matches
37. **derby_name** - A name of a derby in case a match is a derby
38. **home_team** - A home team
39. **away_team** - An away team
40. **match_week** - A match week
41. **month** - A month a match took place
42. **day** - A day of a month a match took place
43. **weekday** - A day of a week a match took place
44. **total_n_matches_played_h** - The number of total matches played by a home team
45. **total_n_matches_played_a** - The number of total matches played by an away team
46. **total_max_points_h** - The maximum points a home team was supposed to get
47. **total_max_points_a** - The maximum points an away team was supposed to get
48. **total_points_h_cum** - The total number of points accumulated by a home team
49. **total_points_a_cum** - The total number of points accumulated by an away team
50. **total_avg_acc_points_h** - The average points accumulated by a home team
51. **total_avg_acc_points_a** - The average points accumulated by an away team
52. **total_avg_points_accumulated_last_3_h** - The average points accumulated by a home team in the last three matches
53. **total_avg_points_accumulated_last_3_a** - The average points accumulated by an away team in the last three matches
54. **total_avg_points_accumulated_last_5_h** - The average points accumulated by a home team in the last five matches
55. **total_avg_points_accumulated_last_5_a** - The average points accumulated by an away team in the last five matches
56. **total_points_dropped_h** - The total number of points dropped by a home team
57. **total_points_dropped_a** - The total number of points dropped by an away team
58. **total_avg_dropped_points_h** - The average number of points dropped by a home team
59. **total_avg_dropped_points_a** - The average number of points dropped by an away team
60. **total_avg_points_dropped_last_3_h** - The average number of points dropped by a home team in the last three matches
61. **total_avg_points_dropped_last_3_a** - The average number of points dropped by an away team in the last three matches
62. **total_avg_points_dropped_last_5_h** - The average number of points dropped by a home team in the last five matches
63. **total_avg_points_dropped_last_5_a** - The average number of points dropped by an away team in the last five matches
64. **total_goals_scored_h** - The total number of goals scored by a home team
65. **total_goals_scored_a** - The total number of goals scored by an away team
66. **total_avg_goals_scored_h** - The average number of goals scored by a home team
67. **total_avg_goals_scored_a** - The average number of goals scored by an away team
68. **total_avg_goals_scored_last_3_h** - The average number of goals scored by a home team in the last three matches
69. **total_avg_goals_scored_last_3_a** - The average number of goals scored by an away team in the last three matches
70. **total_avg_goals_scored_last_5_h** - The average number of goals scored by a home team in the last five matches
71. **total_avg_goals_scored_last_5_a** - The average number of goals scored by an away team in the last five matches
72. **total_goals_conceded_h** - The total number of goals conceded by a home team
73. **total_goals_conceded_a** - The total number of goals conceded by an away team
74. **total_avg_goals_conceded_h** - The average number of goals conceded by a home team
75. **total_avg_goals_conceded_a** - The average number of goals conceded by an away team
76. **total_avg_goals_conceded_last_3_h** - The average number of goals conceded by a home team in the last three matches
77. **total_avg_goals_conceded_last_3_a** - The average number of goals conceded by an away team in the last three matches
78. **total_avg_goals_conceded_last_5_h** - The average number of goals conceded by a home team in the last five matches
79. **total_avg_goals_conceded_last_5_a** - The average number of goals conceded by an away team in the last five matches
80. **total_avg_possession_h** - The average possession of a home team
81. **total_avg_possession_a** - The average possession of an away team
82. **total_avg_possession_last_3_h** - The average possession of a home team in the last three matches
83. **total_avg_possession_last_3_a** - The average possession of an away team in the last three matches
84. **total_avg_possession_last_5_h** - The average possession of a home team in the last five matches
85. **total_avg_possession_last_5_a** - The average possession of an away team in the last five matches
86. **total_shots_on_target_cum_h** - The total number of shots on target by a home team
87. **total_shots_on_target_cum_a** - The total number of shots on target by an away team
88. **total_avg_shots_on_target_h** - The average number of shots on target by a home team
89. **total_avg_shots_on_target_a** - The average number of shots on target by an away team
90. **total_avg_shots_on_target_last_3_h** - The average number of shots on target by a home team in the last three matches
91. **total_avg_shots_on_target_last_3_a** - The average number of shots on target by an away team in the last three matches
92. **total_avg_shots_on_target_last_5_h** - The average number of shots on target by a home team in the last five matches
93. **total_avg_shots_on_target_last_5_a** - The average number of shots on target by an away team in the last five matches
94. **total_shots_cum_h** - The total number of shots by a home team
95. **total_shots_cum_a** - The total number of shots by an away team
96. **total_avg_shots_h** - The average number of shots by a home team
97. **total_avg_shots_a** - The average number of shots by a home team
98. **total_avg_shots_last_3_h** - The average number of shots by a home team in the last three matches
99. **total_avg_shots_last_3_a** - The average number of shots by an away team in the last three matches
100. **total_avg_shots_last_5_h** - The average number of shots by a home team in the last five matches
101. **total_avg_shots_last_5_a** - The average number of shots by an away team in the last five matches
102. **total_avg_touches_h** - The average number of touches by a home team
103. **total_avg_touches_a** - The average number of touches by an away team
104. **total_avg_touches_last_3_h** - The average number of touches by a home team in the last three matches
105. **total_avg_touches_last_3_a** - The average number of touches by an away team in the last three matches
106. **total_avg_touches_last_5_h** - The average number of touches by a home team in the last five matches
107. **total_avg_touches_last_5_a** - The average number of touches by an away team in the last five matches
108. **total_avg_passes_h** - The average number of passes by a home team
109. **total_avg_passes_a** - The average number of passes by a away team
110. **total_avg_passes_last_3_h** - The average number of passes by a home team in the last three matches
111. **total_avg_passes_last_3_a** - The average number of passes by an away team in the last three matches
112. **total_avg_passes_last_5_h** - The average number of passes by a home team in the last five matches
113. **total_avg_passes_last_5_a** - The average number of passes by an away team in the last five matches
114. **total_avg_tackles_h** - The average number of tackles by a home team
115. **total_avg_tackles_a** - The average number of tackles by an away team
116. **total_avg_tackles_last_3_h** - The average number of tackles by a home team in the last three matches
117. **total_avg_tackles_last_3_a** - The average number of tackles by an away team in the last three matches
118. **total_avg_tackles_last_5_h** - The average number of tackles by a home team in the last five matches
119. **total_avg_tackles_last_5_a** - The average number of tackles by an away team in the last five matches
120. **total_avg_clearances_h** - The average number of clearances by a home team
121. **total_avg_clearances_a** - The average number of clearances by an away team
122. **total_avg_clearances_last_3_h** - The average number of clearances by a home team in the last three matches
123. **total_avg_clearances_last_3_a** - The average number of clearances by an away team in the last three matches
124. **total_avg_clearances_last_5_h** - The average number of clearances by a home team in the last five matches
125. **total_avg_clearances_last_5_a** - The average number of clearances by an away team in the last five matches
126. **total_avg_corners_h** - The average number of corners by a home team
127. **total_avg_corners_a** - The average number of corners by an away team
128. **total_avg_corners_last_3_h** - The average number of corners by a home team in the last three matches
129. **total_avg_corners_last_3_a** - The average number of corners by an away team in the last three matches
130. **total_avg_corners_last_5_h** - The average number of corners by a home team in the last five matches
131. **total_avg_corners_last_5_a** - The average number of corners by an away team in the last five matches
132. **total_avg_offsides_h** - The average number of offsides by a home team
133. **total_avg_offsides_a** - The average number of offsides by an away team
134. **total_avg_offsides_last_3_h** - The average number of offsides by a home team in the last three matches
135. **total_avg_offsides_last_3_a** - The average number of offsides by an away team in the last three matches
136. **total_avg_offsides_last_5_h** - The average number of offsides by a home team in the last five matches
137. **total_avg_offsides_last_5_a** - The average number of offsides by an away team in the last five matches
138. **total_avg_yellow_cards_h** - The average number of yellow cards by a home team
139. **total_avg_yellow_cards_a** - The average number of yellow cards by an away team
140. **total_avg_yellow_cards_last_3_h** - The average number of yellow cards by a home team in the last three matches
141. **total_avg_yellow_cards_last_3_a** - The average number of yellow cards by an away team in the last three matches
142. **total_avg_yellow_cards_last_5_h** - The average number of yellow cards by a home team in the last five matches
143. **total_avg_yellow_cards_last_5_a** - The average number of yellow cards by an away team in the last five matches
144. **total_avg_fouls_conceded_h** - The average number of fouls conceded by a home team
145. **total_avg_fouls_conceded_a** - The average number of fouls conceded by an away team
146. **total_avg_fouls_conceded_last_3_h** - The average number of fouls concededs by a home team in the last three matches
147. **total_avg_fouls_conceded_last_3_a** - The average number of fouls concededs by an away team in the last three matches
148. **total_avg_fouls_conceded_last_5_h** - The average number of fouls concededs by a home team in the last five matches
149. **total_avg_fouls_conceded_last_5_a** - The average number of fouls concededs by an away team in the last five matches
150. **total_s2g_cum_ratio_h** - The total goal to shots on target ratio for a home team
151. **total_s2g_cum_ratio_a** - The total goal to shots on target ratio for an away team
152. **total_s2g_ratio_last_3_h** - The goal to shots on target ratio for a home team in the last three matches
153. **total_s2g_ratio_last_3_a** - The goal to shots on target ratio for an away team in the last three matches
154. **total_s2g_ratio_last_5_h** - The goal to shots on target ratio for a home team in the last five matches
155. **total_s2g_ratio_last_5_a** - The goal to shots on target ratio for an away team in the last five matches
156. **total_s2s_cum_ratio_h** - The total shots on target to shots ratio for a home team
157. **total_s2s_cum_ratio_a** - The total shots on target to shots ratio for an away team
158. **total_s2s_ratio_last_3_h** - The shots on target to shots ratio for a home team in the last three matches
159. **total_s2s_ratio_last_3_a** - The shots on target to shots ratio for an away team in the last three matches
160. **total_s2s_ratio_last_5_h** - The shots on target to shots ratio for a home team in the last five matches
161. **total_s2s_ratio_last_5_a** - The shots on target to shots ratio for an away team in the last five matches
162. **n_matches_played_h** - Total number of home matches for a home team
163. **n_matches_played_a** - Total number of away matches for an away team
164. **max_points_h** - Maximum number of points a home could get in home fixtures
165. **max_points_a** - Maximum number of points an away could get in away fixtures
166. **points_h_cum** - The number of points accumulated in home fixtures for a home team
167. **points_a_cum** - The number of points accumulated in away fixtures for an away team
168. **avg_acc_points_h** - The average number of points accumulated by a home team in home fixtures
169. **avg_acc_points_a** - The average number of points accumulated by an away team in away fixtures
170. **avg_points_accumulated_last_3_h** - The average number of points accumulated by a home team in the last three home fixtures
171. **avg_points_accumulated_last_3_a** - The average number of points accumulated by an away team in the last three away fixtures
172. **avg_points_accumulated_last_5_h** - The average number of points accumulated by a home team in the last five home fixtures
173. **avg_points_accumulated_last_5_a** - The average number of points accumulated by an away team in the last five away fixtures
174. **points_dropped_h** - The number of points dropped in home fixtures for a home team
175. **points_dropped_a** - The number of points dropped in away fixtures for an away team
176. **avg_dropped_points_h** - The average number of points dropped by a home team in home fixtures
177. **avg_dropped_points_a** - The average number of points dropped by an away team in away fixtures
178. **avg_points_dropped_last_3_h** - The average number of points dropped by a home team in the last three home fixtures
179. **avg_points_dropped_last_3_a** - The average number of points dropped by an away team in the last three away fixtures
180. **avg_points_dropped_last_5_h** - The average number of points dropped by a home team in the last five home fixtures
181. **avg_points_dropped_last_5_a** - The average number of points dropped by an away team in the last five away fixtures
182. **goals_scored_h_cum** - The number of goals scored by a home team in home fixtures
183. **goals_scored_a_cum** - The number of goals scored by a away team in away fixtures
184. **avg_goals_scored_h** - The average number of goals scored by a home team in home fixtures
185. **avg_goals_scored_a** - The average number of goals scored by an away team in away fixtures
186. **avg_goals_scored_last_3_h** - The average number of goals scored by a home team in the last three home fixtures
187. **avg_goals_scored_last_3_a** - The average number of goals scored by an away team in the last three away fixtures
188. **avg_goals_scored_last_5_h** - The average number of goals scored by a home team in the last five home fixtures
189. **avg_goals_scored_last_5_a** - The average number of goals scored by an away team in the last five away fixtures
190. **goals_conceded_h_cum** - The number of goals conceded by a home team in home fixtures
191. **goals_conceded_a_cum** - The number of goals conceded by an away team in away fixtures
192. **avg_goals_conceded_h** - The average number of goals conceded by a home team in home fixtures
193. **avg_goals_conceded_a** - The average number of goals conceded by an away team in away fixtures
194. **avg_goals_conceded_last_3_h** - The average number of goals conceded by a home team in the last three home fixtures
195. **avg_goals_conceded_last_3_a** - The average number of goals conceded by an away team in the last three away fixtures
196. **avg_goals_conceded_last_5_h** - The average number of goals conceded by a home team in the last five home fixtures
197. **avg_goals_conceded_last_5_a** - The average number of goals conceded by an away team in the last five away fixtures
198. **avg_possession_h** - The average possession for a home team in home fixtures
199. **avg_possession_a** - The average possession for an away team in away fixtures
200. **avg_possession_last_3_h** - The average possession for a home team in the last three home fixtures
201. **avg_possession_last_3_a** - The average possession for an away team in the last three away fixtures
202. **avg_possession_last_5_h** - The average possession for a home team in the last five home fixtures
203. **avg_possession_last_5_a** - The average possession for an away team in the last five away fixtures
204. **shots_on_target_h_cum** - The total number of shots on target for a home team in home fixtures
205. **shots_on_target_a_cum** - The total number of shots on target for an away team in away fixtures
206. **avg_shots_on_target_h** - The average number of shots on target for a home team in home fixtures
207. **avg_shots_on_target_a** - The average number of shots on target for an away team in away fixtures
208. **avg_shots_on_target_last_3_h** - The average number of shots on target for a home team in the last three home fixtures
209. **avg_shots_on_target_last_3_a** - The average number of shots on target for an away team in the last three away fixtures
210. **avg_shots_on_target_last_5_h** - The average number of shots on target for a home team in the last five home fixtures
211. **avg_shots_on_target_last_5_a** - The average number of shots on target for an away team in the last five away fixtures
212. **shots_h_cum** - The total number of shots for a home team in home fixtures
213. **shots_a_cum** - The total number of shots for an away team in away fixtures
214. **avg_shots_h** - The average number of shots for a home team in home fixtures
215. **avg_shots_a** - The average number of shots for an away team in away fixtures
216. **avg_shots_last_3_h** - The average number of shots for a home team in the last three home fixtures
217. **avg_shots_last_3_a** - The average number of shots for an away team in the last three away fixtures
218. **avg_shots_last_5_h** - The average number of shots for a home team in the last five home fixtures
219. **avg_shots_last_5_a** - The average number of shots for an away team in the last five away fixtures
220. **avg_touches_h** - The average number of touches for a home team in home fixtures
221. **avg_touches_a** - The average number of touches for an away team in away fixtures
222. **avg_touches_last_3_h** - The average number of touches for a home team in the last three home fixtures
223. **avg_touches_last_3_a** - The average number of touches for an away team in the last three away fixtures
224. **avg_touches_last_5_h** - The average number of touches for a home team in the last five home fixtures
225. **avg_touches_last_5_a** - The average number of touches for a away team in the last five away fixtures
226. **avg_passes_h** - The average number of passes for a home team in home fixtures
227. **avg_passes_a** - The average number of passes for an away team in away fixtures
228. **avg_passes_last_3_h** - The average number of passes for a home team in the last three home fixtures
229. **avg_passes_last_3_a** - The average number of passes for an away team in the last three away fixtures
230. **avg_passes_last_5_h** - The average number of passes for a home team in the last five home fixtures
231. **avg_passes_last_5_a** - The average number of passes for an away team in the last five away fixtures
232. **avg_tackles_h** - The average number of tackles for a home team in home fixtures
233. **avg_tackles_a** - The average number of tackles for an away team in away fixtures
234. **avg_tackles_last_3_h** - The average number of tackles for a home team in the last three home fixtures
235. **avg_tackles_last_3_a** - The average number of tackles for an away team in the last three away fixtures
236. **avg_tackles_last_5_h** - The average number of tackles for a home team in the last five home fixtures
237. **avg_tackles_last_5_a** - The average number of tackles for an away team in the last five away fixtures
238. **avg_clearances_h** - The average number of clearances for a home team in home fixtures
239. **avg_clearances_a** - The average number of clearances for an away team in home fixtures
240. **avg_clearances_last_3_h** - The average number of clearances for a home team in the last three home fixtures
241. **avg_clearances_last_3_a** - The average number of clearances for an away team in the last three away fixtures
242. **avg_clearances_last_5_h** - The average number of clearances for a home team in the last five home fixtures
243. **avg_clearances_last_5_a** - The average number of clearances for an away team in the last five away fixtures
244. **avg_corners_h** - The average number of corners for a home team in home fixtures
245. **avg_corners_a** - The average number of corners for an away team in away fixtures
246. **avg_corners_last_3_h** - The average number of corners for a home team in the last three home fixtures
247. **avg_corners_last_3_a** - The average number of corners for an away team in the last three away fixtures
248. **avg_corners_last_5_h** - The average number of corners for a home team in the last five home fixtures
249. **avg_corners_last_5_a** - The average number of corners for an away team in the last five away fixtures
250. **avg_offsides_h** - The average number of offsides for a home team in home fixtures
251. **avg_offsides_a** - The average number of offsides for an away team in away fixtures
252. **avg_offsides_last_3_h** - The average number of offsides for a home team in the last three home fixtures
253. **avg_offsides_last_3_a** - The average number of offsides for an away team in the last three away fixtures
254. **avg_offsides_last_5_h** - The average number of offsides for a home team in the last five home fixtures
255. **avg_offsides_last_5_a** - The average number of offsides for an away team in the last five away fixtures
256. **avg_yellow_cards_h** - The average number of yellow cards for a home team in home fixtures
257. **avg_yellow_cards_a** - The average number of yellow cards for an away team in away fixtures
258. **avg_yellow_cards_last_3_h** - The average number of yellow cards for a home team in the last three home fixtures
259. **avg_yellow_cards_last_3_a** - The average number of yellow cards for an away team in the last three away fixtures
260. **avg_yellow_cards_last_5_h** - The average number of yellow cards for a home team in the last five home fixtures
261. **avg_yellow_cards_last_5_a** - The average number of yellow cards for an away team in the last five away fixtures
262. **avg_fouls_conceded_h** - The average number of fouls conceded for a home team in home fixtures
263. **avg_fouls_conceded_a** - The average number of fouls conceded for an away team in away fixtures
264. **avg_fouls_conceded_last_3_h** - The average number of fouls conceded for a home team in the last three home fixtures
265. **avg_fouls_conceded_last_3_a** - The average number of fouls conceded for an away team in the last three away fixtures
266. **avg_fouls_conceded_last_5_h** - The average number of fouls conceded for a home team in the last five home fixtures
267. **avg_fouls_conceded_last_5_a** - The average number of fouls conceded for an away team in the last five away fixtures
268. **s2g_cum_ratio_h** - The goal to shots on target ratio for a home team in home fixtures
269. **s2g_cum_ratio_a** - The goal to shots on target ratio for an away team in away fixtures
270. **s2g_ratio_last_3_h** - The goal to shots on target ratio for a home team in the last three home fixtures
271. **s2g_ratio_last_3_a** - The goal to shots on target ratio for an away team in the last three away fixtures
272. **s2g_ratio_last_5_h** - The goal to shots on target ratio for a home team in the last five home fixtures
273. **s2g_ratio_last_5_a** - The goal to shots on target ratio for an away team in the last five away fixtures
274. **s2s_cum_ratio_h** - The shots on target to shots ratio for a home team in home fixtures
275. **s2s_cum_ratio_a** - The shots on target to shots ratio for an away team in away fixtures
276. **s2s_ratio_last_3_h** - The shots on target to shots ratio for a home team in the last three home fixtures
277. **s2s_ratio_last_3_a** - The shots on target to shots ratio for an away team in the last three away fixtures
278. **s2s_ratio_last_5_h** - The shots on target to shots ratio for a home team in the last five home fixtures
279. **s2s_ratio_last_5_a** - The shots on target to shots ratio for an away team in the last five away fixtures
280. **n_epls_h** - The number of EPL titles won by a home team
281. **n_epls_a** - The number of EPL titles won by an away team
282. **n_ucls_h** - The number of UCL titles won by a home team
283. **n_ucls_a** - The number of UCL titles won by an away team
---

These features indicate the behavior of teams based on which a batch model will learn the previous behavior to predict the future behavior of a team. After running the feature_engineering.py script, the data for each season with batch features created is stored as a separate csv file. The feature engineered data for each season is then converted into a parquet file. Moreover, I am also planning to add some other features which are realted to clubs' off field activities when retraining the model. The initial list of those features are following.

1. **Net spend in the summer transfer window** - The higher the net spend in the summer transfer window the more ambitious the club is going into the season. Even though a higher net spend does not guarantee results it still provides information to the model about the statue of a club, because the bigger clubs have larger exposure and sponsorship deals to generate more revenue than the smaller clubs.
2. **Club takeover** - It is very important to understand whether or not there has been a takeover for a club in recent history because takeovers usually happen when club is not doing well not only on the pitch but also off the pitch which makes fans very angry at the board for not addressing the issues which eventually leads to takeover. In addition, when the takeover happens, the new board tend to appease the fans and spend big in the early years of management. As an example Saudi Arabia recently bought Newcastle United and they spent over 120 million pounds without selling anyone. This variable might be very valuable to the model as the model would learn patterns about clubs' ambition going into season.
3. **Sacking a manager** - Clubs usually decide to sack managers when a team fails to deliver on the pitch consequently. Football is a results' business and any manager is in danger of being sacked after poor run of form and results. When a new manager is appointed there is a period in football which is called **honeymoon** period that lasts three or five matches maximum in which team overperforms and actually gets results before going back to default settings. The model would learn the current state of a club in case its manager has been sacked in the summer or during a season while predicting increase in performance with a new manager in post.

## Modeling
Considering the fact that it is time based binary classification problem, I did not shuffle the training data since it was more important for the model to learn the behavior in previous seasons to predict into the upcoming season. The initial training data covers **12** years of data starting from **2006/07** season up until the end of **2017/18** season while **2018/19 - 2021/22** seasons were used as the test which can also be referred as **out of time (OOT)** samples. There are 20 teams in the division, while a single season lasts 38 weeks on average and in each week on average there are 10 matches. In a single season there are **380** matches and the training data contains **4560** matches from previous seasons whereas the test set contains **1520** matches. The features used in modeling have been categorized into **five** different groups which are following.

1. **Nominal features**
2. **Ordinal features**
3. **Binary features**
4. **Numeric features**
5. **Datetime features** 

All the algorithms were tested and in the end for the **Win** model the **Stacked** pipeline containing **Logistic Regression**, **Multi Layer Perceptron**, and **Light Gradient Boosted Machine (LightGBM)** algorithms prevailed with the highest **Area Under the Curve (AUC)** score on the test set. On the hand hand for the **Loss** model the **Voting** pipeline got the best **AUC** score on the test set using the previously mentioned algorithms while **Multi Layer Perceptron** was chosen for the **Draw** model. Modeling involved following algorithms.

| Algorithms|Win Model|Loss Model|Draw Model|
| -------- | -------- | -------- | -------- |
|Gaussian Naïve Bayes|False|False|False
|Logistic Regression|True|True|False
|Support Vector Machine|False|False|False
|K Nearest Neighbors|False|False|False
|Multi Layer Perceptron|True|True|True
|Decision Tree|False|False|False
|Random Forest|False|False|False
|Adaptive Boosting (AdaBoost)|False|False|False
|Light Gradient Boosted Machine (LightGBM)|True|True|False
|Gradient Boosting (GBM)|False|False|False
|Extreme Gradient Boosting (XGBoost)|False|False|False
|Category Boosting (CatBoost)|False|False|False
|Stacked|True|False|False
|Voting|False|True|False

The main evaluation metric for the project is **AUC** score since all outcomes of a football match are equally important to predict and the probability threshold has been applied based on **Balanced Accuracy** score which is calculated by this formula.

- **Balanced Accuracy Score = (Sensitivity + Specificity) / 2**

This is the architecture of the classifier pipeline with **Logistic Regression** as the estimator.

![](https://i.imgur.com/ymr2iPb.png)

This is the architecture of the classifier pipeline with **Multi Layer Perceptron** as the estimator.

![](https://i.imgur.com/MuyWFK0.png)

This is the architecture of the classifier pipeline with **Light Gradient Boosted Machine** as the estimator.

![](https://i.imgur.com/XupOTIL.png)

In order to maximize the evaluation metric both on train and test sets I applied probability thresholding between 10% and 90% probabilities. This is an example from the probability thresholding for the **Win** model.

![](https://i.imgur.com/wfH50rO.png)

This is the **confusion matrix**, **Recall & Precision Ratio** for train and test sets based on **Support Vector Machine** algorithm for the **Win** model.

![](https://i.imgur.com/WgG7YP6.png)

This is the **Receiver Operating Characteristics Curve (ROC)** curve for the train and test sets of the **Win** model.

![](https://i.imgur.com/b2iCq7y.png)

It would not be the best approach to use this model to predict the outcome of the matches of the current season since the training data should also include the most recent data. Therefore, I retrained the model by including the from **2018/19 -- 2021/22** seasons to the training set in which case **2022/23** *(current season)* would be the test set. In order to create an engine, I combined the models and a prediction with the maximum probability is the outcome of the engine. I have created **three** confidence interval boundaries for the engine predictions which are following.

1. **Low** - The outcome of a match with probability less than **50%** (exclusive)
2. **Medium** - The outcome of a match with probability between than **50%** (inclusive) and **65%** (exclusive)
3. **High** - The outcome of a match with probability greater equal than **65%** (inclusive)

Engine's performance is evaluated based on the predictions made with high confidence. Current accuracy of the engine on the train set is **77%** and **74%** on the test set.

![](https://i.imgur.com/VwUDOJR.png)

## Additional Information
I will maintain this project for the years to come and add other functionalities to the engine such as **online prediction** using in game statistics. In addition, I will also include new variables for the current engine and retrain it. Since the size of the training set is subject to increase each year, the change for the main algorithms used in modeling is expected.