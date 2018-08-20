# Copyright 2018 - James Spadafora
# Open Pipe
# Utility classes for interacting with the DB.
import sqlite3
import os

class Database(object):
    """Base class for interacting with different DBs."""

    def __init__(self):
        """Set up object."""
        pass

    def get_shots(self):
        """Get a list of all shots."""
        return []

class SQLiteDatabase(Database):
    """Class for storing and getting data from an SQLite file."""

    def __init__(self, dataDir, initFile=False):
        """
        Set up object and create a connection.

        Args:
            sqlitePath(str): Path to the datadir
            initFile(bool): Set up the file if it does not exist.
        """
        self.dataDir = dataDir
        sqlitePath = os.path.join(dataDir, 'db.sqlite')

        if not os.path.isfile(sqlitePath) and not initFile:
            raise IOError('No SQLite file exists for the project.')
        elif not os.path.isfile(sqlitePath) and initFile:
            self.initDb(sqlitePath)
        else:
            self.sqlitePath = sqlitePath
            self.connection = sqlite3.connect(self.sqlitePath)
            self.cursor = self.connection.cursor()

    def initDb(self, sqlitePath):
        """Set up the sqlite file."""
        self.sqlitePath = sqlitePath
        print(self.sqlitePath)
        self.connection = sqlite3.connect(self.sqlitePath)
        self.cursor = self.connection.cursor()

        # Build the shotlist table
        self.cursor.execute('CREATE TABLE shots (shotname STRING PRIMARY KEY)')
        self.connection.commit()
        self.connection.close()

    def connect(self):
        print('Connecting')
        self.connection = sqlite3.connect(self.sqlitePath)
        self.cursor = self.connection.cursor()

    # Query

    def get_shots(self, keepOpen=False):
        """Get a list of all shots."""
        self.connect()
        self.cursor.execute('SELECT * from shots')
        all = self.cursor.fetchall()
        if not keepOpen:
            self.connection.close()
        return all

    def get_shot_data(self, shot):
        """Get info for this shot."""
        shotdata = {}

        self.connect()
        self.cursor.execute("SELECT * from shots WHERE shotname='{0}'".format(shot))
        info = self.cursor.fetchone()
        if not info:
            raise KeyError('No such shot {0} exists'.format(shot))
        shotdata['name'] = info[0]
        shotdata['firstFrame'] = 0
        shotdata['lastFrame'] = 100
        self.connection.close()

        shotConnection, shotCur = self._get_shotdb(shot)
        shotCur.execute('SELECT * from takes')
        all = shotCur.fetchall()

        takes = []
        for take in all:
            takes.append({'id': take[0]})
        shotdata['takes'] = takes

        shotCur.execute('SELECT * from reviews')
        all = shotCur.fetchall()

        reviews = []
        for review in all:
            reviews.append({'id': review[0]})
        shotdata['reviews'] = reviews
        shotConnection.close()

        return shotdata

    # Save

    def new_shot(self, shotname, firstframe, lastframe):
        """Create a new shot in the DB."""
        self.connect()
        if shotname in self.get_shots(keepOpen=True):
            raise ValueError('Shot {0} already exists in db.'.format(shotname))
        self.cursor.execute("INSERT INTO shots (shotname) VALUES ('{0}')".format(shotname))

        # Create a DB for the shot
        shotConnection, shotCur = self._get_shotdb(shotname)

        shotCur.execute('CREATE TABLE takes (takeid INTEGER PRIMARY KEY)')
        shotCur.execute('CREATE TABLE reviews (reviewid INTEGER PRIMARY KEY)')

        shotConnection.commit()
        shotConnection.close()
        self.connection.commit()
        self.connection.close()

    # Util

    def _get_shotdb(self, shot):
        """Get the path to the shot DB file."""
        shotDbPath = os.path.join(self.dataDir, '{0}_shotdb.sqlite'.format(shot))
        shotConnection = sqlite3.connect(shotDbPath)
        shotCur = shotConnection.cursor()
        return shotConnection, shotCur