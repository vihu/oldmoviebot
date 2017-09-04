'''
Creating a new SQLite database
'''

import sqlite3

def create_db(sqlite_file):
    ''' Create DB
    '''
    # Connecting to the database file
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    c.execute(''' CREATE TABLE replies
                  (submission_id TEXT PRIMARY KEY, imdb_id TEXT, movie TEXT, reply TEXT)
    ''')

    # Committing changes and closing the connection to the database file
    conn.commit()
    conn.close()
