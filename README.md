# oldmoviebot
* Reddit bot for r/iwatchedanoldmovie
* Post imdb link for new submissions in [iwatchedanoldmovie](https://www.reddit.com/r/iwatchedanoldmovie)
* Keeps a local sqlite3 db to avoid posting to the same submission over n over again.

## Requirements
* python3, I've tested on python3.6.2 since that's what I had installed on my local machine.
* Clone this repo
* Create a virtualenv after cd into the cloned repo, command to do that:

```python3 -m venv venv```

* Install dependencies

```
pip install -r requirements.txt
```
* Create a config.py file in your working directory. I've included a sample one for you.
* Run using:

```
python old_movie_bot.py
```

## Credits
* [praw](https://praw.readthedocs.io/en/latest/), for reddit python API
* [imdb-pie](https://github.com/richardasaurus/imdb-pie), for imdb python API
* [busteroni](https://www.youtube.com/user/busterroni11), for the incredibly useful video on how to make a reddit bot

## LICENSE
* [GNU General Public License v3.0](https://github.com/vihu/oldmoviebot/blob/master/LICENSE)
* I bear no responsibility if this crashes your system (it shouldn't ideally)