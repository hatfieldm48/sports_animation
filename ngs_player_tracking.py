import time
import json
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation

## Start Big Data Bowl 2021 Functions
#####################################

'''
Given the game info dictionary, return a string representation
  of the game
'''
def game_info_to_string(game_info_dict):
	home = list(game_info_dict['homeTeamAbbr'].values())[0]
	away = list(game_info_dict['visitorTeamAbbr'].values())[0]
	week = list(game_info_dict['week'].values())[0]
	return home + ' vs ' + away + ': Week ' + str(week)

'''
given the file path of the broken out csv ngs data, return the list of all items
'''
def get_list_of_games(data_file_path):
	list_of_weeks = [x for x in os.walk(data_file_path)]

	#print (list_of_weeks[1])
	list_of_games = []
	for i in range(1, len(list_of_weeks)):
		path_week = list_of_weeks[i][0]
		game_files = [path_week + '/' + x for x in list_of_weeks[i][2]]
		list_of_games.extend(game_files)

	return list_of_games

'''
Get a dictionary, where the keys are gameIds, and values are a list of playIds of that game
'''
def get_games_plays_dict(data_file_path):
	list_of_weeks = [x for x in os.walk(data_file_path)]
	list_of_plays = []
	for i in range(1, len(list_of_weeks)):
		path_week = list_of_weeks[i][0]
		play_files = [path_week + '/' + x for x in list_of_weeks[i][2]]
		list_of_plays.extend(play_files)

	list_of_game_ids = list(set([x.split('/')[-2] + '/' + x.split('/')[-1].split('_')[0] for x in list_of_plays]))

	game_plays = {}
	for game_id in list_of_game_ids:
		list_of_g_play_ids = [x.split('/')[-1].split('_')[1][:-4] for x in list_of_plays if x.split('/')[-1].split('_')[0] == game_id]
		game_plays[game_id] = list_of_g_play_ids

	return game_plays

'''
Given the games dataframe and the uniqPlayId file path
  return a dictionary with the game information
'''
def get_game_info_from_csv_name(df_games, csv_file_path, game_id=''):
	if len(game_id) == 0:
		csv_file = csv_file_path.split('/')[-1]
		gameId = csv_file.split('_')[0]
	else:
		gameId = game_id
	df_filtered = df_games[df_games['gameId']==int(gameId)]

	return df_filtered.to_dict()

'''
Given the games dataframe and the uniqPlayId file path
  return a dictionary with the play information
'''
def get_play_info_from_csv_name(df_plays, csv_file_path): 
	csv_file = csv_file_path.split('/')[-1]
	gameId = csv_file.split('_')[0]
	playId = csv_file.split('_')[-1][:-4]
	df_filtered = df_plays[(df_plays['playId']==int(playId)) & (df_plays['gameId']==int(gameId))]

	return df_filtered.to_dict()

'''
Translate home/away to the actual team name (e.g. PHI)
'''
def team_nfl(team_val, home_team, away_team):
	if team_val=='home':
		return home_team
	elif team_val=='away':
		return away_team
	elif team_val=='football':
		return 'ball'
	else:
		return 'NA'
    

'''
Translate this format into the one made previously from the old json ngs data
'''    
def convert_to_animation_format(df_play, df_plays, df_games):
	#time converstion might be needed to strip away date (would store date in another field)

	#displayName --> player_id
	df_play = df_play.rename({'displayName': 'player_id'}, axis='columns')

	#Football/football vs ball

	#Create description from play_info
	play_info = get_play_info_from_csv_name(df_plays, list(df_play['uniqPlayId'])[0] + '.csv')
	play_description = list(play_info['playDescription'].values())[0]
	play_description = play_description.replace("'", "")
	df_play['description'] = play_description

	#create team_nfl from team and game_info
	game_info = get_game_info_from_csv_name(df_games, list(df_play['uniqPlayId'])[0] + '.csv')
	home_team = list(game_info['homeTeamAbbr'].values())[0]
	away_team = list(game_info['visitorTeamAbbr'].values())[0]
	df_play['team_nfl'] = df_play['team'].apply(lambda x: team_nfl(x, home_team, away_team))

	#uniqPlayId --> play_id

	#remove ' from player_id
	df_play['player_id'] = df_play['player_id'].apply(lambda x: x.replace("'", ""))

	#Set original order
	#time	x	y	s	a	dis	o	dir	event	nflId	displayName	jerseyNumber	position	frameId	team	gameId	playId	playDirection	route
	df_play_reduced = df_play[['uniqPlayId', 'description', 'time', 'player_id', 'team', 'team_nfl', 'x', 'y']]

	return df_play_reduced

### End Big Data Bowl 2021 Functions
####################################

'''
Function to convert the string time into something more usable
example time: 2018-09-16T17:59:29.500
'''
def convert_time(str_time):
	## Assuming every instance of time is split by 'T'
	time = str_time.split('T')[1]
	return time

'''
Function to setup the matplotlib plot
returns the plot
'''
def setup_plot():
	colors = ['blue'] * 11 + ['red'] * 11 + ['yellow']
	img = plt.imread('football_field.png')
	fig, ax = plt.subplots()
	x, y = [], []
	ax.imshow(img, extent=[0, 120, 0, 53.34])
	ax.set_title('Example Title')
	game = ax.scatter(x, y, s=5**2, c=colors, alpha=0.5)
	return game, fig, ax

'''
Utilize the matplotlib animation library to visualize the play
'''
def visualize_play(fig, game, df, t):
	ani = animation.FuncAnimation(fig, animate, frames=len(t), 
		fargs=(df, t, game,), interval=100)
	plt.show(block=False)

'''
Function to animate the ngs player tracking movement
  using matplotlib animation
'''
def animate(i, df, t, g, ax):
	df_frame = df[df['time']==t[i]]
	ax.set_title(list(df_frame['description'])[0])
	#i_time = i_time + 1
	x = []
	y = []
	x = x + list(df_frame[df_frame['team']=='home']['x'])
	y = y + list(df_frame[df_frame['team']=='home']['y'])
	x = x + list(df_frame[df_frame['team']=='away']['x'])
	y = y + list(df_frame[df_frame['team']=='away']['y'])
	x = x + list(df_frame[df_frame['player_id']=='ball']['x'])
	y = y + list(df_frame[df_frame['player_id']=='ball']['y'])
	g.set_offsets(np.c_[x,y])

'''
A function to organize all the data required to visualize
one play of NGS player tracking data
10/1/2018 Update: the new parameter f_names, allows for the visualization
  of multiple plays. The list should be pre ordered, which can be 
  accomplished using the order_plays function
'''
def extract_player_tracking_data(f_name = '', f_names = []):
	
	if (len(f_name) > 0):
		## Open the JSON file
		example_play_tracking = json.loads(open(f_name).read())
		
		## First, check if the play was deleted
		if ('is_deleted' in example_play_tracking['play_tracking']['play'].keys()):
			is_deleted = example_play_tracking['play_tracking']['play']['is_deleted']
			if (is_deleted):
				print ('This play: ', f_name, ' was deleted for unknown reasons.')
				return [], []

		## Read in the needed dictionary lists
		play_id = f_name.split('/')[-1] #play_id = example_play_tracking['play_tracking']['play']['sequence']
		try:
			play_description = example_play_tracking['play_tracking']['play']['description']
		except:
			play_description = 'error in getting the play description'
		try:
			ball_locations = example_play_tracking['play_tracking']['ball']['tracking']
		except:
			print ('ball location error', f_name)
		try:
			home_players = example_play_tracking['play_tracking']['home']['players']
			home_team = example_play_tracking['play_tracking']['home']['name']
		except:
			print ('home player error', f_name)
		try:
			away_players = example_play_tracking['play_tracking']['away']['players']
			away_team = example_play_tracking['play_tracking']['away']['name']
		except:
			print ('away player error', f_name)
		df_cols = ['play_id', 'description', 'time', 'player_id', 'team', 'team_nfl', 'x', 'y']

		## Create the dataframe for viz/analysis
		all_tracking = []
		for location in ball_locations:
			all_tracking.append([play_id, play_description.replace("'", ""), convert_time(location['time']), 'ball', 
				'ball', 'ball', location['x'], location['y']])
		for player in home_players:
			for location in player['tracking']:
				all_tracking.append([play_id, play_description.replace("'", ""), convert_time(location['time']), 
					player['first_name'].replace("'", "") + ' ' + player['last_name'].replace("'", ""), 
					'home', home_team, location['x'], location['y']])
		for player in away_players:
			for location in player['tracking']:
				all_tracking.append([play_id, play_description.replace("'", ""), convert_time(location['time']), 
					player['first_name'].replace("'", "") + ' ' + player['last_name'].replace("'", ""), 
					'away', away_team, location['x'], location['y']])

		df_all_tracking = pd.DataFrame.from_records(all_tracking, columns=df_cols)
		times = sorted(list(set(list(df_all_tracking['time']))))
		#print (df_all_tracking.head(20))
		print (times)
		print (df_all_tracking.columns)
		df_all_tracking.to_csv('example_df_all_tracking.csv', index=False)
		return df_all_tracking, times

	elif (len(f_names) > 0):
		all_tracking = []
		df_cols = ['play_id', 'description', 'time', 'player_id', 'team', 'x', 'y']

		for f_name in f_names:
			## Open the JSON file
			example_play_tracking = json.loads(open(f_name).read())
			
			## Read in the needed dictionary lists
			play_id = f_name.split('/')[-1] #play_id = example_play_tracking['play_tracking']['play']['sequence']
			play_description = example_play_tracking['play_tracking']['play']['description']
			ball_locations = example_play_tracking['play_tracking']['ball']['tracking']
			home_players = example_play_tracking['play_tracking']['home']['players']
			away_players = example_play_tracking['play_tracking']['away']['players']

			## Create the dataframe for viz/analysis
			for location in ball_locations:
				all_tracking.append([play_id, play_description.replace("'", ""), convert_time(location['time']), 'ball', 
					'ball', location['x'], location['y']])
			for player in home_players:
				for location in player['tracking']:
					all_tracking.append([play_id, play_description.replace("'", ""), convert_time(location['time']), 
						player['first_name'].replace("'", "") + ' ' + player['last_name'].replace("'", ""), 
						'home', location['x'], location['y']])
			for player in away_players:
				for location in player['tracking']:
					all_tracking.append([play_id, play_description.replace("'", ""), convert_time(location['time']), 
						player['first_name'].replace("'", "") + ' ' + player['last_name'].replace("'", ""), 
						'away', location['x'], location['y']])

		df_all_tracking = pd.DataFrame.from_records(all_tracking, columns=df_cols)
		times = sorted(list(set(list(df_all_tracking['time']))))
		#print (df_all_tracking.head(20))
		#print (times)
		return df_all_tracking, times

	else:
		return None, None

'''
Funtion to order the plays from a file repository
As they exist, the files are only ordered by randomly generated id strings
This function loads each json, and checks the quarter and game clock
it returns to ordered list of json files names, from start to finish of the game
'''
def order_plays(game_repo):
    plays = []
    for f in os.listdir(game_repo + '/'):
        play_tracking = json.loads(open(game_repo + '/' + f).read())
        quarter = int(play_tracking['play_tracking']['play']['quarter'])
        game_clock = play_tracking['play_tracking']['play']['game_clock']
        minute = float(game_clock.split(':')[0])
        second = float(game_clock.split(':')[1])
        game_time = minute + (second / 60.0)
        play = {'play_id': f, 'quarter': quarter, 'time': game_time}
        plays.append(play)
    df_plays = pd.DataFrame(plays).sort_values(['quarter', 'time'], ascending=[True, False])
    ordered_plays = list(df_plays['play_id'])
    return ordered_plays

