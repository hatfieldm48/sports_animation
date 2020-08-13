import time
import json
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation

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

