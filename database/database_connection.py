import sqlite3


def connection(filename):
    """Establish a connection to the given database"""
    try:
        cnx = sqlite3.connect(filename)
        return cnx
    except sqlite3.OperationalError:
        print('Failed to connect to database')
