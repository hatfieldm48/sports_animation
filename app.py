from flask import Flask, flash, redirect, render_template, request, session, abort, g
import os
import json
import pandas as pd
import ngs_player_tracking

app = Flask(__name__)
ext_file_path = 'D:/Sports Analytics/sportradar/'


'''
@app.route('/player-tracking-animation?playselection', methods=['POST', 'GET'])
def reload_game():
	print ('IT WORKED')
'''

@app.route('/player-tracking-animation', methods=['POST', 'GET'])
def watch_game():
	if (request.method == 'POST'):
		#print (request.form)
		game = request.form['gameselection']
		plays = [game + '/' + file for file in os.listdir(game) if file.endswith('.json')]
		plays_display = []

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

		#play_to_viz_title = list(plays_display)[0]
		play_to_viz_title = list(df_sorted['play_description'])[0]
		print (play_to_viz_title)

		return render_template('player_tracking_animation.html', **locals())
	else:
		print ('Error')

@app.route('/')
def select_game():
	# Get the available list of games to visualize
	list_of_games = [x[0] for x in os.walk(ext_file_path)]
	list_of_games.remove(ext_file_path)
	game_keys = list(list_of_games)
	game_values = []
	list_of_games = [x.replace(ext_file_path, '') for x in list_of_games]
	for game in list_of_games:
		substrings = game.split('-')
		game_str = substrings[0].capitalize() + ' vs ' + substrings[1].capitalize() + ': ' + substrings[2][:-1].capitalize() + ' ' + str(substrings[2][-1])
		game_values.append(game_str)
	games_dict = dict(zip(game_keys, game_values))
	return render_template('select_game.html', **locals())

if __name__ == "__main__":
	app.run(debug=True)
