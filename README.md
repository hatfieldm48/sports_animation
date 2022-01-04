# Sport Animation Overview
A web application framework to visualize sports as a animation of player tracker data. The current build does this using a sample of data provided by the NFL NextGenStats from games during the 2018 season. To see a live version of this, you may try visiting [this link](http://3.16.75.248/), although if it is not responding, feel free to reach out to me as a I don't keep the ec2 instance it runs on up at all times.

## Installation and Use
To try running this code, simply clone the repo, and ensure you have the libraries listed in the requirements.txt already in your local python environment, or as a part of a virtualenv. To find the sample data, you can also download that from [this repo](https://github.com/hatfieldm48/nfl_ngs). You will just need to edit `line 7` of the `app.py` file, to change the pointer for `ext_file_path`.

From the cloned directory, running `python app.py` will create a local flask webapp where you can choose between these sample games, and then scroll through all the plays of that game to see each individual play animation.

## What it Looks Like
Take a look at the [wiki homepage](https://github.com/hatfieldm48/sports_animation/wiki) to see a gif video of what the animation looks like. You can hover over a player's icon to see the name. You can also click on that player to display a full play track of their location, along with a visualization of the closest player from the opposing team to them at all times.


