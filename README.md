# Sport Animation Overview
A web application framework to visualize sports as a animation of player tracker data. This branch was adapted from the master to read in the slightly altered data fromat provided by [NFL Big Data Bowl 2021](https://www.kaggle.com/c/nfl-big-data-bowl-2021/overview). To see a live version of this, you may try visiting [hatfieldmike.com](www.hatfieldmike.com), although if it is not responding, feel free to reach out to me as a I don't keep the ec2 instance it runs on up at all times.

## Installation and Use
To run this code, first clone the repo. Then you will need to edit line 10 of the `docker-compose.yml`. You will want to change the first part of the `:` to be the directory you have the big_data_bowl_2021 filesystem. To get the file system properly organized, you will need to run the `split_week_into_game_plays` in [the big_data_bowl_2021](https://github.com/hatfieldm48/sports_animation/blob/big_data_bowl_2021/big_data_bowl_helper_nb.ipynb) script which will break out the `weeks[i].csv` data files into individual tracking csv data files for each play of each game. The process is commented in cell 3 in the notebook. Once that's done, navigate to the directory, and run `docker compose up`. You should see the following output:

```
PS C:\Users\572784\Documents\Github\sports_animation> docker compose up
[+] Building 56.9s (9/9) FINISHED
 => [internal] load build definition from Dockerfile                                                                                                                                                                                    0.0s
 => => transferring dockerfile: 31B                                                                                                                                                                                                     0.0s
 => [internal] load .dockerignore                                                                                                                                                                                                       0.0s
 => => transferring context: 2B                                                                                                                                                                                                         0.0s
 => [internal] load metadata for docker.io/library/python:3.9.1                                                                                                                                                                        30.6s
 => [internal] load build context                                                                                                                                                                                                       0.2s
 => => transferring context: 19.36kB                                                                                                                                                                                                    0.1s
 => CACHED [1/4] FROM docker.io/library/python:3.9.1@sha256:ca8bd3c91af8b12c2d042ade99f7c8f578a9f80a0dbbd12ed261eeba96dd632f                                                                                                            0.0s
 => [2/4] ADD . /python-flask                                                                                                                                                                                                           0.1s
 => [3/4] WORKDIR /python-flask                                                                                                                                                                                                         0.1s
 => [4/4] RUN pip install -r requirements.txt                                                                                                                                                                                          22.6s
 => exporting to image                                                                                                                                                                                                                  3.3s
 => => exporting layers                                                                                                                                                                                                                 3.2s
 => => writing image sha256:ef7b5a03d9e1dfd6ef2e6c8e9ca2b9497db2f642270154daa5238599cce32ec3                                                                                                                                            0.0s
 => => naming to docker.io/library/sports_animation_app                                                                                                                                                                                 0.0s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
[+] Running 1/1
 - Container sports_animation_app_1  Created                                                                                                                                                                                            0.1s
Attaching to app_1
app_1  |  * Serving Flask app 'app' (lazy loading)
app_1  |  * Environment: production
app_1  |    WARNING: This is a development server. Do not use it in a production deployment.
app_1  |    Use a production WSGI server instead.
app_1  |  * Debug mode: on
app_1  |  * Running on all addresses.
app_1  |    WARNING: This is a development server. Do not use it in a production deployment.
app_1  |  * Running on http://172.23.0.2:5000/ (Press CTRL+C to quit)
app_1  |  * Restarting with stat
app_1  |  * Debugger is active!
app_1  |  * Debugger PIN: 526-165-709
```

Once successful, navigate to `http://localhost:5000/` in a web browser. You should now see a local flask webapp where you can choose between these sample games, and then scroll through all the plays of that game to see each individual play animation.

If you would prefer to run this without docker, you can refer back to the commit `baf866a3b7fee9e73616c5084f9efc0b50f53f9e` of this branch, which has the app setup to install only with the requirements.txt file as a local virtual environment. You will just need to edit `line 10` of the `app.py` file, to change the pointer for `data_file_path`.

## What it Looks Like
Take a look at the [wiki homepage](https://github.com/hatfieldm48/sports_animation/wiki) to see a gif video of what the animation looks like. You can hover over a player's icon to see the name. You can also click on that player to display a full play track of their location, along with a visualization of the closest player from the opposing team to them at all times.


