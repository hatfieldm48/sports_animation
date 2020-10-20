from flask import Flask, flash, redirect, render_template, request, session, abort, g
import os
import json
import pandas as pd
import ngs_player_tracking
import math

app = Flask(__name__)
##ext_file_path = 'D:/Sports Analytics/sportradar/'
data_file_path = '../../NFL/big_data_bowl_2021/'
df_games = pd.read_csv(data_file_path + '/games.csv')
df_players = pd.read_csv(data_file_path + '/players.csv')
df_plays = pd.read_csv(data_file_path + '/plays.csv')

'''
@app.route('/player-tracking-animation?playselection', methods=['POST', 'GET'])
def reload_game():
	print ('IT WORKED')
'''

@app.route('/player-tracking-animation', methods=['POST', 'GET'])
def watch_game():
	if (request.method == 'POST'):
		#print (request.form)
		#print (list(request.form.keys())[0])
		if (list(request.form.keys())[0] == 'gameselection'):
			game = request.form['gameselection']
			print (game)
			#plays = [game + '/' + file for file in os.listdir(game) if file.endswith('.json')]
			plays = [file for file in os.listdir(data_file_path + game.split('/')[0]) if game.split('/')[-1] in file]
			##print (plays)
			plays_display = []

			for play in plays:
				play_info = ngs_player_tracking.get_play_info_from_csv_name(df_plays, play)
				play_description = list(play_info['playDescription'].values())[0]
				quarter = list(play_info['quarter'].values())[0]
				playId = list(play_info['playId'].values())[0]
				gameClock = list(play_info['gameClock'].values())[0]
				if gameClock=='nan': #if math.isnan(gameClock):
					gameClock = 0
				else:
					gameClockSort = (4-quarter)*15 + float(gameClock.split(':')[0]) + float(gameClock.split(':')[1])*(1.0/60.0)
				plays_display.append([gameClockSort, 'Q' + str(quarter) + ' ' + play_description, game.split('/')[0] + '/' + play])


			"""
			for play in plays:
				play_json = json.loads(open(play).read())
				
				## First, check if the play was deleted
				if ('is_deleted' in play_json['play_tracking']['play'].keys()):
					is_deleted = play_json['play_tracking']['play']['is_deleted']
					if (is_deleted):
						print ('This play: ', play, ' was deleted for unknown reasons.')
						continue

				try:
					play_description = play_json['play_tracking']['play']['description'].replace("'", "")
				except:
					play_description = 'error in getting the play description'
				try:
					play_quarter = play_json['play_tracking']['play']['quarter']
				except:
					play_quarter = 6
				try:
					play_gameclock = play_json['play_tracking']['play']['game_clock']
				except:
					play_gameclock = '99:59'
				try:
					play_down = play_json['play_tracking']['play']['down']
				except:
					play_down = 5
				try:
					play_ytg = play_json['play_tracking']['play']['ytg']
				except:
					play_ytg = -1
				time_sort = ((4 - play_quarter) * 15) + int(play_gameclock.split(':')[0]) + (float(play_gameclock.split(':')[1]) / 60.0)
				plays_display.append([time_sort, 'Q' + str(play_quarter) + ' ' + play_description, play])

			df_plays = pd.DataFrame.from_records(plays_display, columns=['time_sort', 'play_description', 'file'])
			df_sorted = df_plays.sort_values('time_sort', ascending=False)
			#plays_display = dict(zip(list(df_sorted['file']), list(df_sorted['play_description'])))
			plays_display = zip(list(df_sorted['file']), list(df_sorted['play_description']))

			#play_to_viz = ngs_player_tracking.extract_player_tracking_data(f_name=list(df_sorted['file'])[0])[0].to_html()
			#play_to_viz = ngs_player_tracking.extract_player_tracking_data(f_name=list(df_sorted['file'])[0])[0].to_csv(index=False)
			#play_to_viz = ngs_player_tracking.extract_player_tracking_data(f_name=list(df_sorted['file'])[0])[0].values
			play_to_viz = ngs_player_tracking.extract_player_tracking_data(f_name=list(df_sorted['file'])[0])[0].to_json(orient='records')
			"""

			play_to_viz_title = list(plays_display)[0][1]
			df_sorted = pd.DataFrame.from_records(plays_display, columns=['time_sort', 'play_description', 'file'])
			df_sorted = df_sorted.sort_values('time_sort', ascending=False)
			plays_display = zip(list(df_sorted['file']), list(df_sorted['play_description']))
			
			df_play = pd.read_csv(data_file_path + game.split('/')[0] + '/' + plays[0])
			#print (data_file_path + game.split('/')[0] + '/' + plays[0])
			play_to_viz = ngs_player_tracking.convert_to_animation_format(df_play, df_plays, df_games)
			play_to_viz = play_to_viz.to_json()

			#play_to_viz_title = list(df_sorted['play_description'])[0]
			print (play_to_viz_title)

			return render_template('player_tracking_animation.html', **locals())

		elif (list(request.form.keys())[0] == 'playselection'):
			selected_play = request.form['playselection']
			selected_play_file = data_file_path + selected_play
			selected_play_info = ngs_player_tracking.get_play_info_from_csv_name(df_plays, selected_play)
			play_to_viz_title = list(selected_play_info['playDescription'].values())[0]
			print (selected_play)

			game = selected_play.split('_')[0]
			plays = [file for file in os.listdir(data_file_path + game.split('/')[0]) if game.split('/')[-1] in file]
			plays_display = []

			for play in plays:
				play_info = ngs_player_tracking.get_play_info_from_csv_name(df_plays, play)
				play_description = list(play_info['playDescription'].values())[0]
				quarter = list(play_info['quarter'].values())[0]
				playId = list(play_info['playId'].values())[0]
				gameClock = list(play_info['gameClock'].values())[0]
				plays_display.append([playId, 'Q' + str(quarter) + ' ' + play_description, game.split('/')[0] + '/' + play])

			df_sorted = pd.DataFrame.from_records(plays_display, columns=['time_sort', 'play_description', 'file'])
			plays_display = zip(list(df_sorted['file']), list(df_sorted['play_description']))

			df_play = pd.read_csv(selected_play_file)	
			play_to_viz = ngs_player_tracking.convert_to_animation_format(df_play, df_plays, df_games)
			play_to_viz = play_to_viz.to_json()

			return render_template('player_tracking_animation.html', **locals())
		else:
			x=0
	else:
		print ('Error')

@app.route('/')
def select_game():
	# Get the available list of games to visualize
	list_of_games = ngs_player_tracking.get_list_of_games(data_file_path)
	game_plays = ngs_player_tracking.get_games_plays_dict(data_file_path)
	print (game_plays)
	"""
	game_keys = list(list_of_games)
	game_values = []
	list_of_games = [x.replace(ext_file_path, '') for x in list_of_games]
	for game in list_of_games:
		substrings = game.split('-')
		game_str = substrings[0].capitalize() + ' vs ' + substrings[1].capitalize() + ': ' + substrings[2][:-1].capitalize() + ' ' + str(substrings[2][-1])
		game_values.append(game_str)
	games_dict = dict(zip(game_keys, game_values))
	"""

	## TO DO:
	# [x] create mapping of plays to games (list_of_games is actually the full list of plays now, but game_values is created correctly, just duplicated)
	# [x] create ordered list of play ids for each game by timestamp
	# [ ] create ordering of the games (by week, alphabetically within those)
		#Might run into issues with python dictionaries not being order, and it seems like I need to pass a dictionary 
	# [ ] copy new code to plot_play over to replot_ply in main.js
		#Might not need to do this since the code will only ever call plot_play now
		
	game_keys = list(game_plays.keys()) #game_keys = list(list_of_games)
	game_values = [ngs_player_tracking.game_info_to_string(ngs_player_tracking.get_game_info_from_csv_name(df_games, '', x.split('/')[-1])) for x in game_keys]
	#print (game_keys)
	#print (game_values)
	games_dict = dict(zip(game_keys, game_values))
	###games_dict = sorted(games_dict.items(), key=lambda x: x[1][len(': Week ') + x[1].index(':'):])

	return render_template('select_game.html', **locals())

if __name__ == "__main__":
	app.run(debug=True)
