'''
Post a message on r/iwatchedanoldmovie with imdb information about the post
'''

import sqlite3
from time import sleep
import os.path
import praw
import config
from imdbpie import Imdb
from create_new_db import create_db

SUBREDDIT = 'oldmoviebottest'
QUESTIONS = ['watched', 'rewatched']
REPLY_TEMPLATE = "[Here's the best match from IMDB](http://imdb.com/title/{})"
DB_FILE = 'oldmoviebot.db'

def setup():
    ''' Setup local DB file
    '''
    if not os.path.exists(DB_FILE):
        print('Creating local DB File {}'.format(DB_FILE))
        create_db(DB_FILE)
    return

def main():
    ''' Login to reddit and process submissions
    '''
    reddit = praw.Reddit(username=config.username,
                         password=config.password,
                         client_id=config.client_id,
                         client_secret=config.client_secret,
                         user_agent='oldmoviebot (by /u/vihu)')

    subreddit = reddit.subreddit(SUBREDDIT)
    for submission in subreddit.stream.submissions():
        process_submission(submission)

def extract_movie_info(title):
    ''' Extract movie information from the submission title
    Only supports:
        * I watched movie name (year)
        * I rewatched movie name (year)
    Example:
        * I watched Dunkirk (2017)
        * I watched The Dark Knight (2008)
    as of now
    '''
    year = title[title.find("(")+1:title.find(")")]
    movie = ' '.join(title.split()[2:-1])
    return movie, year

def get_title_id(movie, year):
    ''' Get title_id from imdb API
    '''
    imdb = Imdb(anonymize=True)
    list_of_matches = imdb.search_for_title(movie)
    try:
        possible_match = next(filter(lambda x: x['year'] == year, list_of_matches))
        return possible_match['imdb_id']
    except StopIteration:
        print('No match for movie {}'.format(movie))

def update_db(submission_id, title_id, movie, reply):
    ''' Update DB with submission id and reply
    '''
    conn = sqlite3.connect('oldmoviebot.db')
    c = conn.cursor()
    c.execute('INSERT INTO replies VALUES (?,?,?,?);', (submission_id, title_id, movie, reply))
    conn.commit()
    conn.close()

def already_replied(submission_id):
    ''' Return data if already replied else None
    '''
    conn = sqlite3.connect('oldmoviebot.db')
    c = conn.cursor()
    c.execute("SELECT * FROM replies WHERE submission_id = ?;", (submission_id, ))
    data = c.fetchone()
    conn.commit()
    conn.close()
    return data

def process_submission(submission):
    ''' Process submission for given subreddit
    '''
    # title too big, ignore
    if len(submission.title.split()) > 10:
        return

    normalized_title = submission.title.lower()
    for question_phrase in QUESTIONS:
        if question_phrase in normalized_title:
            movie, year = extract_movie_info(submission.title)
            title_id = get_title_id(movie, year)
            if movie and year and title_id:
                try:
                    data = already_replied(submission.id)
                    if data is None:
                        print('Replying to: {}'.format(submission.title))
                        reply_text = REPLY_TEMPLATE.format(title_id)
                        print('Replying with: {}'.format(reply_text))
                        submission.reply(reply_text)
                        print('Updating DB with submission_id {}'.format(submission.id))
                        update_db(submission.id, title_id, movie, reply_text)
                    else:
                        print('Have already replied to {}, {}'.format(submission.id, submission.title))
                        continue
                except praw.objector.APIException:
                    print('Possible rate limit exception, pausing for some time...')
                    sleep(300)
                    continue
            # A reply has been made so do not attempt to match other phrases.
            break

if __name__ == '__main__':
    setup()
    main()
