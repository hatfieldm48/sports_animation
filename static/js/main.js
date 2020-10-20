
/**
 * Function to update the data/figure/layout of the chart animation
 * this is called when the user selects a new play to view
 */
function replot_play (data, new_title) {
	//alert (data);
	console.log(data);
	play_id = data.split('/')[data.split('/').length - 1];
	console.log(play_id);
	//alert (play_id);
	console.log('https://raw.githubusercontent.com/hatfieldm48/nfl_ngs/master/play_json_files/' + play_id);

	//data = get('https://github.com/hatfieldm48/nfl_ngs/blob/master/854f1115-52bd-496e-96a3-d1b2da76edc8.json');
	data = get('https://raw.githubusercontent.com/hatfieldm48/nfl_ngs/master/play_json_files/' + play_id);
	data = JSON.parse(data);

	var lookup = {};
	function getData(time, team) {
		var byTime, trace;
		if (!(byTime = lookup[time])) {
			byTime = lookup[time] = {};
		}

		// If a container for this time and team doesn't exist yet, then create one
		if (!(trace = byTime[team])) {
			trace = byTime[team] = {
				x: [],
				y: [],
				id: [],
				text: [],
				team: [],
				marker: {size: [], sizemode: [], line: {color: [], width: []}}
			};
		}
		return trace;
	}

	// Need the data JSON to be in the format:
	//  {play_id, description, time, player_id, team, x, y}
	//play_id = '854f1115-52bd-496e-96a3-d1b2da76edc8';
	play_description = data['play_tracking']['play']['description'];
	ball_locations = data['play_tracking']['ball']['tracking'];
	home_players = data['play_tracking']['home']['players'];
	away_players = data['play_tracking']['away']['players'];
	all_tracking = [];

	for (i = 0; i < ball_locations.length; i++) {
		loc = ball_locations[i];
		//all_tracking.push([play_id, play_description, convert_time(loc['time']), 'ball', 'ball', loc['x'], loc['y']]);
		dict = {
			play_id: play_id,
			description: play_description,
			time: convert_time(loc['time']),
			player_id: 'ball',
			team: 'ball',
			team_nfl: 'ball',
			x: loc['x'],
			y: loc['y'],
		};
		all_tracking.push(dict);
	}
	for (i = 0; i < home_players.length; i++) {
		player = home_players[i];
		for (j = 0; j < player['tracking'].length; j++) {
			loc = player['tracking'][j];
			//all_tracking.push([play_id, play_description, convert_time(loc['time']), player['first_name'] + ' ' + player['last_name'], 'home', loc['x'], loc['y']]);
			dict = {
				play_id: play_id,
				description: play_description,
				time: convert_time(loc['time']),
				player_id: player['first_name'] + ' ' + player['last_name'],
				team: 'home',
				team_nfl: data['play_tracking']['home']['name'],
				x: loc['x'],
				y: loc['y'],
			};
			all_tracking.push(dict);
		}
	}
	for (i = 0; i < away_players.length; i++) {
		player = away_players[i];
		for (j = 0; j < player['tracking'].length; j++) {
			loc = player['tracking'][j];
			//all_tracking.push([play_id, play_description, convert_time(loc['time']), player['first_name'] + ' ' + player['last_name'], 'away', loc['x'], loc['y']]);
			dict = {
				play_id: play_id,
				description: play_description,
				time: convert_time(loc['time']),
				player_id: player['first_name'] + ' ' + player['last_name'],
				team: 'away',
				team_nfl: data['play_tracking']['away']['name'],
				x: loc['x'],
				y: loc['y'],
			};
			all_tracking.push(dict);
		}
	}

	//Get the teams (and team colors) before defining the trace datasets
	var teams = ['ball', 'home', 'away'];
	var teams_nfl_full = [];
	for (var i = 0; i < all_tracking.length; i++) {
		teams_nfl_full.push(all_tracking[i].team_nfl);
	}
	function onlyUnique(value, index, self) {
		return self.indexOf(value) === index;
	}
	var teams_nfl = teams_nfl_full.filter(onlyUnique); //The order will always be Ball, Home, Away
	var team_sizes = [1, 11, 11];
	var colors = ['rgba(232, 213, 38, 0.7)', get_team_color(teams_nfl[1]), get_team_color(teams_nfl[2])]

	// Go through each row, get the right trace, and append the data
	for (var i = 0; i < all_tracking.length; i++) {
		var datum = all_tracking[i];
		var trace = getData(datum.time, datum.team);
		trace.text.push(datum.player_id);
		trace.team.push(datum.team_nfl);
		trace.id.push(datum.id);
		trace.x.push(datum.x);
		trace.y.push(datum.y);
		trace.marker.size.push(10);
		trace.marker.sizemode.push('area');
		trace.marker.line.color.push(colors[teams_nfl.indexOf(datum.team_nfl)]);
		trace.marker.line.width.push(2);
		title = datum.description;
	}

	// Get the group names
	var times = Object.keys(lookup).sort();
	var firstTimes = lookup[times[0]];
	//console.log(firstTimes);
	/*var teams = ['ball', 'home', 'away'];
	var teams_nfl = ['ball', firstTimes['home']['team'][0], firstTimes['away']['team'][0]];
	//console.log(teams_nfl);
	//var colors = ['rgba(232, 213, 38, 0.7)', 'rgba(255, 55, 55, 0.3)', 'rgba(55, 55, 255, 0.3)']
	var colors = ['rgba(232, 213, 38, 0.7)', get_team_color(teams_nfl[1]), get_team_color(teams_nfl[2])]*/

	// Create the main traces, one for each team
	var traces = [];
	for (i = 0; i < teams.length; i++) {
		var data = firstTimes[teams[i]];
		// One small note. We're creating a single trace here, to which
		// the frames will pass data for the different times. It's
		// subtle, but to avoid data reference problems, we'll slice 
		// the arrays to ensure we never write any new data into our
		// lookup table:
		traces.push ({
			name: teams[i],
			x: data.x.slice(),
			y: data.y.slice(),
			id: data.id.slice(),
			text: data.text.slice(),
			mode: 'markers',
			marker: {
				size: 10,
				sizemode: 'area',
				color: colors[i],
				line: {color: colors[i], width: 2}
			}
		});
	}
	traces.push({
		id: 'def_prox',
		x: [],
		y: [],
		mode: 'markers+lines',
		name: 'defender proximity',
		line: {color: 'black'},
		type: 'scatter'
	});
	traces.push({
		id: 'player_tracing',
		x: [],
		y: [],
		mode: 'lines',
		name: 'player tracing',
		line: {color: 'rgb(55, 230, 255)', width: 5},
		//type: 'scatter'
	});

	// Create a frame for each time. Frames are effectively just
	// traces, except they don't need to contain the *full* trace
	// definition (for example, appearance). The frames just need
	// the parts the traces that change (here, the data)
	var frames = [];
	for (i = 0; i < times.length; i++) {
		data_ = teams.map(function (team) {
			return getData(times[i], team)
		});
		data_.push({
			id: 'def_prox',
			x: [],
			y: [],
			mode: 'markers+lines',
			name: 'defender proximity',
			line: {color: 'black'},
			type: 'scatter'
		});
		data_.push({ //This is the dataset to highlight the player tracing for the full play
			id: 'player_tracing',
			x: [],
			y: [],
			mode: 'lines',
			name: 'player tracing',
			line: {color: 'rgb(55, 230, 255)', width: 5},
			//type: 'scatter'
		});
		frames.push({
			name: times[i],
			data: data_
		})
	}

	// Now create slider steps, one for each frame. The slider
	// executes a plotly.js API command (plotly.animate)
	// In this example, we'll animate to one of the named frames
	// created in the above loop
	var sliderSteps = [];
	for (i = 0; i < times.length; i++) {
		sliderSteps.push ({
			method: 'animate',
			label: times[i],
			args: [[times[i]], {
				mode: 'immediate',
				transition: {duration: 40, easing: 'cubic-in-out'},
				frame: {duration: 50, redraw: false},
			}]
		});
	}

	var layout = {
		//title: title,
		xaxis: {
			//title: 'X Axis',
			range: [0, 120]
		},
		yaxis: {
			//title: 'Y Axis',
			range: [0, 53.34]
		},
		showlegend: true,
		legend: {"orientation": "h"},
		//width: 1664,
		height: 740,
		margin: {
			l: 40,
			r: 30,
			b: 10,
			t: 30,
			pad: 4
		},
		images: [{
			source: "https://raw.githubusercontent.com/hatfieldm48/nfl_ngs/master/football_field_grayscale.png",
			xref: "x",
			yref: "y",
			x: 0,
			y: 53.34,
			sizex: 120,
			sizey: 53.34,
			sizing: "stretch",
			opacity: 0.5,
			layer: "below"
		}],
		hovermode: 'closest',
		// We'll use updatemenus (whose functionality includes menus as
		// well as buttons) to create a play button and a pause button.
		// The play button works by passing `null`, which indicates that
		// Plotly should animate all frames. The pause button works by
		// passing `[null]`, which indicates we'd like to interrupt any
		// currently running animations with a new list of frames. Here
		// The new list of frames is empty, so it halts the animation.
		updatemenus: [{
			x: 0,
			y: 0,
			yanchor: 'top',
			xanchor: 'left',
			showactive: false,
			direction: 'left',
			type: 'buttons',
			pad: {t: 87, r: 10},
			buttons: [{
				method: 'animate',
				args: [null, {
					mode: 'immediate',
					fromcurrent: true,
					transition: {duration: 30, easing: 'cubic-in-out'},
					frame: {duration: 50, redraw: false}
				}],
				label: 'Play'
			}, {
				method: 'animate',
				args: [[null], {
					mode: 'immediate',
					transition: {duration: 0},
					frame: {duration: 0, redraw: false}
				}],
				label: 'Pause'
			}]
		}],
		// Finally, add the slider and use `pad` to position it
		// nicely next to the buttons.
		sliders: [{
			pad: {l: 130, t: 55},
			currentvalue: {
				visible: true,
				prefix: 'Time: ',
				xanchor: 'right',
				font: {size: 20, color: '#666'}
			},
			steps: sliderSteps
		}]
	};

	// Create the plot
	Plotly.newPlot('football_field_cht', {
		data: traces,
		layout: layout,
		frames: frames,
	});

	update_chart_title(new_title);

	//Creating the user click action
	var graphDiv = document.getElementById('football_field_cht');
	graphDiv.on('plotly_click', function(traces) {
	    /*
	    console.log(traces.points[0].data);
	    console.log(traces.points);
	    var index = traces.points[0].pointIndex;
	    var curve = traces.points[0].curveNumber;
	    for (var i = 0; i < frames.length; i++) {
	    	frame = frames[i];
	    	//Still need to figure out the team portion ... 
			//console.log(frame.data[2].marker.size, index);
	    	//frame.data[2].marker.size[index] = 20;
	    	frame.data[curve].marker.line.width[index] = 5;
	    	//line: Array(team_sizes[i]).fill({color: colors[i], width: 2})
	    	//console.log(frame.data[2].marker.size);
	    }*/
	    console.log(traces.points[0].data);
		console.log(traces.points);
		var index = traces.points[0].pointIndex;
		var curve = traces.points[0].curveNumber;
		if (curve != 0) {
			player_tracing_x = [];
			player_tracing_y = [];
			for (var i = 0; i < frames.length; i++) {
				frame = frames[i];
				frame.data[curve].marker.line.width[index] = 5;

				// Identify the closest defender
				//selected = [traces.points[0].data.x[index], traces.points[0].data.y[index]];
				selected = [frame.data[curve].x[index], frame.data[curve].y[index]];
				closest_defenders = [];
				for (var j = 0; j < 11; j++) {
					defender = [frame.data[3 - curve].x[j], frame.data[3 - curve].y[j]];
					distance = Math.sqrt(Math.pow(defender[0] - selected[0], 2) + Math.pow(defender[1] - selected[1], 2));
					//console.log(i, j, selected, defender, distance);
					closest_defenders.push([j, distance, defender]);
				}
				//.sort(function(a, b){return a-b});
				closest_defenders.sort(function(a, b){return a[1] - b[1]});
				//console.log(closest_defenders);
				var new_trace = {
					x: [selected[0], closest_defenders[0][2][0]],
					y: [selected[1], closest_defenders[0][2][1]],
					mode: 'markers+lines',
					name: 'defender proximity',
					line: {color: 'black'},
					type: 'scatter'
				}
				//frame.data.push(new_trace);
				frame.data[3] = new_trace;

				// 2) Get the velocity

				// 3) Setup the player tracing viz
				player_tracing_x.push(selected[0]);
				player_tracing_y.push(selected[1]);
			}

			for (var i = 0; i < frames.length; i++) {
				frame = frames[i];
				var new_trace = {
					x: player_tracing_x,
					y: player_tracing_y,
					mode: 'lines',
					name: 'player tracing',
					line: {color: 'rgba(55, 230, 255, 0.5)', width: 5},
					//type: 'scatter'
				};
				frame.data[4] = new_trace;
			}
		}

	});

}

/**
 * Function to create the plotly animation chart of the first play
 * May reuse this for newly selected plays, or may create a new function, TBD 
 */
function plot_play (err, data) {
	// Create a lookup table to sort and regroup the columns of data,
	// first by time, then by team
	//console.log(data);
	data = JSON.parse(data);
	data_length = Object.keys(data['description']).length;
	console.log(data_length);
	console.log(data);
	var title = '';

	var lookup = {};
	function getData (time, team) {
		var byTime, trace;
		if (!(byTime = lookup[time])) {
			byTime = lookup[time] = {};
		}

		// If a container for this time and team doesn't exist yet, then create one
		if (!(trace = byTime[team])) {
			trace = byTime[team] = {
				x: [],
				y: [],
				id: [],
				text: [],
				team: [],
				marker: {size: [], sizemode: [], line: {color: [], width: []}}
				//marker: [{size: [], sizemode: [], color: [], line: []}]
			};
		}
		return trace;
	}

	//Get the teams (and team colors) before defining the trace datasets
	//var teams = ['ball', 'home', 'away'];
	var teams = ['football', 'home', 'away'];
	//var teams_nfl_full = [];
	var teams_nfl_full = Object.keys(data['team_nfl']).map(function(key){
		return data['team_nfl'][key];
	});
	//console.log(data['team_nfl']);
	//console.log(data['team_nfl'][15]);
	//console.log(data_team_nfl);
	/*for (var i = 0; i < data.length; i++) {
		teams_nfl_full.push(data[i].team_nfl);
	}*/
	function onlyUnique(value, index, self) {
		return self.indexOf(value) === index;
	}
	var teams_nfl = teams_nfl_full.filter(onlyUnique); //The order will always be Ball, Home, Away
	console.log(teams_nfl);
	var team_sizes = [1, 11, 11];
	var colors = ['rgba(232, 213, 38, 0.7)', get_team_color(teams_nfl[1]), get_team_color(teams_nfl[2])]

	// Go through each row, get the right trace, and append the data
	for (var i = 0; i < data_length; i++) {
		/*
		var datum = data[i];
		var trace = getData(datum.time, datum.team);
		trace.text.push(datum.player_id);
		trace.team.push(datum.team_nfl);
		trace.id.push(datum.id);
		trace.x.push(datum.x);
		trace.y.push(datum.y);
		trace.marker.size.push(10);
		trace.marker.sizemode.push('area');
		//trace.marker.line.push({color: 'rbga(51, 51, 51, 1)', width: 2});
		trace.marker.line.color.push(colors[teams_nfl.indexOf(datum.team_nfl)]);
		trace.marker.line.width.push(2);
		title = datum.description;*/
		var trace = getData(data['time'][i], data['team'][i]);
		trace.text.push(data['player_id'][i]);
		trace.team.push(data['team_nfl'][i]);
		trace.id.push(data['uniqPlayId'][i]);
		trace.x.push(data['x'][i]);
		trace.y.push(data['y'][i]);
		trace.marker.size.push(10);
		trace.marker.sizemode.push('area');
		//trace.marker.line.push({color: 'rbga(51, 51, 51, 1)', width: 2});
		trace.marker.line.color.push(colors[teams_nfl.indexOf(data['team_nfl'][i])]);
		trace.marker.line.width.push(2);
		title = data['description'][i];
	}

	// Get the group names
	var times = Object.keys(lookup).sort();
	var firstTimes = lookup[times[0]];
	//console.log(firstTimes);
	/*var teams = ['ball', 'home', 'away'];
	var team_sizes = [1, 11, 11];
	var teams_nfl = ['ball', firstTimes['home']['team'][0], firstTimes['away']['team'][0]];
	//console.log(teams_nfl);
	//var colors = ['rgba(232, 213, 38, 0.7)', 'rgba(255, 55, 55, 0.3)', 'rgba(55, 55, 255, 0.3)']
	var colors = ['rgba(232, 213, 38, 0.7)', get_team_color(teams_nfl[1]), get_team_color(teams_nfl[2])]*/

	// Create the main traces, one for each team
	var traces = [];
	for (i = 0; i < teams.length; i++) {
		var data = firstTimes[teams[i]];
		// One small note. We're creating a single trace here, to which
		// the frames will pass data for the different times. It's
		// subtle, but to avoid data reference problems, we'll slice 
		// the arrays to ensure we never write any new data into our
		// lookup table:
		traces.push ({
			name: teams[i],
			x: data.x.slice(),
			y: data.y.slice(),
			id: data.id.slice(),
			text: data.text.slice(),
			mode: 'markers',
			marker: {
				size: 10,
				sizemode: 'area',
				color: colors[i],
				line: {color: colors[i], width: 2}
			}
			/*marker: Array(11).fill({
				size: 10,
				sizemode: 'area',
				color: colors[i],
				line: {color: colors[i], width: 2}
			})*/
		});
	};
	traces.push({
		id: 'def_prox',
		x: [],
		y: [],
		mode: 'markers+lines',
		name: 'defender proximity',
		line: {color: 'black'},
		type: 'scatter'
	});
	traces.push({
		id: 'player_tracing',
		x: [],
		y: [],
		mode: 'lines',
		name: 'player tracing',
		line: {color: 'rgb(55, 230, 255)', width: 5},
		//type: 'scatter'
	});

	//Testing out creating the Line of Scrimmage nad First Down Line
	/*traces.push ({
		name: 'Line of Scrimmage',
		x: [35, 35],
		y: [0, 53.34],
		mode: 'lines',
		line: {
        	color: 'rgb(0, 45, 214)',
        	width: 2
		}
	});
	traces.push ({
		name: 'First Down',
		x: [45, 45],
		y: [0, 53.34],
		mode: 'lines',
		line: {
        	color: 'rgb(255, 193, 7)',
        	width: 2
		}
	});*/

	// Create a frame for each time. Frames are effectively just
	// traces, except they don't need to contain the *full* trace
	// definition (for example, appearance). The frames just need
	// the parts the traces that change (here, the data)
	var frames = [];
	for (i = 0; i < times.length; i++) {
		data_ = teams.map(function (team) {
			return getData(times[i], team)
		});
		data_.push({ //This is the dataset for the defender proximity
			id: 'def_prox',
			x: [],
			y: [],
			mode: 'markers+lines',
			name: 'defender proximity',
			line: {color: 'black'},
			type: 'scatter'
		});
		data_.push({ //This is the dataset to highlight the player tracing for the full play
			id: 'player_tracing',
			x: [],
			y: [],
			mode: 'lines',
			name: 'player tracing',
			line: {color: 'rgb(55, 230, 255)', width: 5},
			//type: 'scatter'
		});
		/*frames.push({
			name: times[i],
			data: teams.map(function (team) {
				return getData(times[i], team);
			}),
		});*/
		frames.push({
			name: times[i],
			data: data_,
		});
	}

	// Now create slider steps, one for each frame. The slider
	// executes a plotly.js API command (plotly.animate)
	// In this example, we'll animate to one of the named frames
	// created in the above loop
	var sliderSteps = [];
	for (i = 0; i < times.length; i++) {
		sliderSteps.push ({
			method: 'animate',
			label: times[i],
			args: [[times[i]], {
				mode: 'immediate',
				transition: {duration: 40, easing: 'cubic-in-out'},
				frame: {duration: 50, redraw: false},
			}]
		});
	}

	var layout = {
		//title: title,
		xaxis: {
			//title: 'X Axis',
			range: [0, 120]
		},
		yaxis: {
			//title: 'Y Axis',
			range: [0, 53.34]
		},
		showlegend: true,
		annotations: [
			{
				x: 10,
				y: 50,
				xref: 'x',
				yref: 'y',
				text: 'Distance from Defender: ',
				showarrow: false,
				align: 'left',
				/*arrowhead: 7,
				ax: 0,
				ay: -40*/
				bordercolor: '#ffffff',
				borderwidth: 2,
				borderpad: 4,
				bgcolor: '#ffffff',
				opacity: 0.8
			},
			{
				x: 10,
				y: 47,
				xref: 'x',
				yref: 'y',
				text: 'Velocity: ',
				showarrow: false,
				align: 'left',
				/*arrowhead: 7,
				ax: 0,
				ay: -40*/
				bordercolor: '#ffffff',
				borderwidth: 2,
				borderpad: 4,
				bgcolor: '#ffffff',
				opacity: 0.8
			}
		],
		legend: {"orientation": "h"},
		//width: 1664,
		height: 740,
		margin: {
			l: 40,
			r: 30,
			b: 10,
			t: 30,
			pad: 4
		},
		images: [{
			source: "https://raw.githubusercontent.com/hatfieldm48/nfl_ngs/master/football_field_grayscale.png",
			xref: "x",
			yref: "y",
			x: 0,
			y: 53.34,
			sizex: 120,
			sizey: 53.34,
			sizing: "stretch",
			opacity: 0.5,
			layer: "below"
		}],
		hovermode: 'closest',
		// We'll use updatemenus (whose functionality includes menus as
		// well as buttons) to create a play button and a pause button.
		// The play button works by passing `null`, which indicates that
		// Plotly should animate all frames. The pause button works by
		// passing `[null]`, which indicates we'd like to interrupt any
		// currently running animations with a new list of frames. Here
		// The new list of frames is empty, so it halts the animation.
		updatemenus: [{
			x: 0,
			y: 0,
			yanchor: 'top',
			xanchor: 'left',
			showactive: false,
			direction: 'left',
			type: 'buttons',
			pad: {t: 87, r: 10},
			buttons: [{
				method: 'animate',
				args: [null, {
					mode: 'immediate',
					fromcurrent: true,
					transition: {duration: 30, easing: 'cubic-in-out'},
					frame: {duration: 50, redraw: false}
				}],
				label: 'Play'
			}, {
				method: 'animate',
				args: [[null], {
					mode: 'immediate',
					transition: {duration: 0},
					frame: {duration: 0, redraw: false}
				}],
				label: 'Pause'
			}]
		}],
		// Finally, add the slider and use `pad` to position it
		// nicely next to the buttons.
		sliders: [{
			pad: {l: 130, t: 55},
			currentvalue: {
				visible: true,
				prefix: 'Time: ',
				xanchor: 'right',
				font: {size: 20, color: '#666'}
			},
			steps: sliderSteps
		}]
	};

	// Create the plot
	Plotly.plot('football_field_cht', {
		data: traces,
		layout: layout,
		frames: frames,
	});

	console.log(frames);

	//Creating the user click action
	var graphDiv = document.getElementById('football_field_cht');
	graphDiv.on('plotly_click', function(traces) {
		console.log(traces.points[0].data);
		console.log(traces.points);
		var index = traces.points[0].pointIndex;
		var curve = traces.points[0].curveNumber;
		if (curve != 0) {
			player_tracing_x = [];
			player_tracing_y = [];
			for (var i = 0; i < frames.length; i++) {
				frame = frames[i];
				frame.data[curve].marker.line.width[index] = 5;

				// 1) Identify the closest defender
				selected = [frame.data[curve].x[index], frame.data[curve].y[index]];
				closest_defenders = [];
				for (var j = 0; j < 11; j++) {
					defender = [frame.data[3 - curve].x[j], frame.data[3 - curve].y[j]];
					distance = Math.sqrt(Math.pow(defender[0] - selected[0], 2) + Math.pow(defender[1] - selected[1], 2));
					closest_defenders.push([j, distance, defender]);
				}
				closest_defenders.sort(function(a, b){return a[1] - b[1]});
				var new_trace = {
					x: [selected[0], closest_defenders[0][2][0]],
					y: [selected[1], closest_defenders[0][2][1]],
					mode: 'markers+lines',
					name: 'defender proximity',
					line: {color: 'black'},
					type: 'scatter'
				};
				frame.data[3] = new_trace;

				// 2) Get the velocity

				// 3) Setup the player tracing viz
				player_tracing_x.push(selected[0]);
				player_tracing_y.push(selected[1]);
			}
			//console.log(player_tracing);
			for (var i = 0; i < frames.length; i++) {
				frame = frames[i];
				var new_trace = {
					x: player_tracing_x,
					y: player_tracing_y,
					mode: 'lines',
					name: 'player tracing',
					line: {color: 'rgba(55, 230, 255, 0.5)', width: 5},
					//type: 'scatter'
				};
				frame.data[4] = new_trace;
			}
		}
	});

}

/**
 * Function to get the request object from a url
 */
function get (yourUrl) {
    var Httpreq = new XMLHttpRequest(); // a new request
    Httpreq.open("GET",yourUrl,false);
    Httpreq.send(null);
    return Httpreq.responseText;          
}

/**
 * Function to convert string time to useable time
 */
function convert_time (str_time) {
	time = str_time.split('T')[1];
	return time;
}

/**
 * Change the chart title according to the newly clicked button
 */
function update_chart_title (new_title) {
	cht_title = document.getElementById('chart-title');
	cht_title.innerHTML = new_title;
}


/**
 * Get the correct primary color for the given NFL team
 */
function get_team_color (str_team_name) {
	var team_colors = {
		'ARI': 'rgba(135, 0, 39, 0.7)',
		'ATL': 'rgba(163, 13, 45, 0.7)',
		'BAL': 'rgba(26, 25, 95, 0.7)',
		'BUF': 'rgba(12, 46, 130, 0.7)',
		'CAR': 'rgba(0, 133, 202, 0.7)',
		'CHI': 'rgba(11, 22, 42, 0.7)',
		'CIN': 'rgba(211, 47, 30, 0.7)',
		'CLE': 'rgba(211, 47, 30, 0.7)',
		'DAL': 'rgba(0, 21, 50, 0.7)',
		'DEN': 'rgba(0, 35, 76, 0.7)',
		'DET': 'rgba(0, 78, 137, 0.7)',
		'GB': 'rgba(28, 45, 37, 0.7)',
		'HOU': 'rgba(0, 7, 28, 0.7)',
		'IND': 'rgba(1, 51, 105, 0.7)',
		'JAX': 'rgba(0, 101, 118, 0.7)',
		'KC': 'rgba(227, 24, 55, 0.7)',
		'LAC': 'rgba(0, 21, 50, 0.7)',
		'LA': 'rgba(0, 21, 50, 0.7)',
		'MIA': 'rgba(0, 142, 151, 0.7)',
		'MIN': 'rgba(79, 38, 131, 0.7)',
		'NE': 'rgba(0, 21, 50, 0.7)',
		'NO': 'rgba(159, 137, 88, 0.7)',
		'NYG': 'rgba(1, 35, 82, 0.7)',
		'NYJ': 'rgba(28, 45, 37, 0.7)',
		'OAK': 'rgba(166, 174, 176, 0.7)',
		'PHI': 'rgba(0, 49, 53, 0.7)',
		'PIT': 'rgba(238, 173, 30, 0.7)',
		'SF': 'rgba(170, 0, 0, 0.7)',
		'SEA': 'rgba(0, 21, 50, 0.7)',
		'TB': 'rgba(213, 10, 10, 0.7)',
		'TEN': 'rgba(0, 21, 50, 0.7)',
		'WAS': 'rgba(63, 16, 16, 0.7)',
	};
	return team_colors[str_team_name];
}
