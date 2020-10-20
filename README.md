# Sport Animation Overview
A web application framework to visualize sports as a animation of player tracker data. This branch was adapted from the master to read in the slightly altered data fromat provided by [NFL Big Data Bowl 2021](https://www.kaggle.com/c/nfl-big-data-bowl-2021/overview). To see a live version of this, you may try visiting this link, although if it is not responding, feel free to reach out to me as a I don't keep the ec2 instance it runs on up at all times.

## Installation and Use
To try running this code, simply clone the repo, and ensure you have the libraries listed in the requirements.txt already in your local python environment, or as a part of a virtualenv. You will just need to edit `line 10` of the `app.py` file, to change the pointer for `data_file_path`. Additionally, you will need to run the `split_week_into_game_plays` in [the big_data_bowl_2021](https://github.com/hatfieldm48/sports_animation/blob/big_data_bowl_2021/big_data_bowl_helper_nb.ipynb) script which will break out the `weeks[i].csv` data files into individual tracking csv data files for each play of each game. The process for commented in cell 3 in the notebook.

From the cloned directory, running `python app.py` will create a local flask webapp where you can choose between these sample games, and then scroll through all the plays of that game to see each individual play animation.

## What it Looks Like
Take a look at the [wiki homepage](https://github.com/hatfieldm48/sports_animation/wiki) to see a gif video of what the animation looks like. You can hover over a player's icon to see the name. You can also click on that player to display a full play track of their location, along with a visualization of the closest player from the opposing team to them at all times.


