# Copyright 2018 - James Spadafora
# Open Pipe
# Utility classes for interacting with the DB.
import sqlite3
from datetime import datetime
import os

class Database(object):
    """Base class for interacting with different DBs."""

    def __init__(self):
        """Set up object."""
        pass

    def get_shots_or_assets(self):
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
        self.cursor.execute('CREATE TABLE assets (assetname STRING PRIMARY KEY)')
        self.connection.commit()
        self.connection.close()

    def connect(self):
        print('Connecting')
        self.connection = sqlite3.connect(self.sqlitePath)
        self.cursor = self.connection.cursor()

    # Query

    def get_shots_or_assets(self, keepOpen=False, assets=False):
        """Get a list of all shots."""
        self.connect()
        if assets:
            self.cursor.execute('SELECT * from assets')
        else:
            self.cursor.execute('SELECT * from shots')
        all = self.cursor.fetchall()
        if not keepOpen:
            self.connection.close()
        return all

    def get_shot_data(self, shot):
        """Get info for this shot."""
        shotdata = {}
        asset = False

        self.connect()
        self.cursor.execute("SELECT * from shots WHERE shotname='{0}'".format(shot))
        info = self.cursor.fetchone()
        if not info:
            asset = True
            self.cursor.execute("SELECT * from assets WHERE assetname='{0}'".format(shot))
            info = self.cursor.fetchone()

        if not info:
            raise KeyError('No such shot {0} exists'.format(shot))

        shotdata['name'] = info[0]

        if not asset:
            shotdata['firstFrame'] = 0
            shotdata['lastFrame'] = 100
        self.connection.close()

        shotConnection, shotCur = self._get_shotdb(shot)
        shotCur.execute('SELECT * from takes')
        all = shotCur.fetchall()

        takes = []
        # take_number INTEGER PRIMARY KEY, path text, created_on datetime, created_by text, task_type text
        for take in all:
            takes.append({'take_number': take[0],
                          'path': take[1],
                          'created_on': datetime.strptime(take[2], '%Y-%m-%d %X.%f'),
                          'created_by': take[3],
                          'task_type': take[4]})
        shotdata['takes'] = takes

        shotCur.execute('SELECT * from reviews')
        all = shotCur.fetchall()

        reviews = []
        for review in all:
            reviews.append({'id': review[0]})
        shotdata['reviews'] = reviews
        shotConnection.close()

        return shotdata

    # New

    def new_shot(self, shotname, firstframe, lastframe):
        """Create a new shot in the DB."""
        self.connect()
        if shotname in self.get_shots_or_assets(keepOpen=True):
            raise ValueError('Shot {0} already exists in db.'.format(shotname))
        self.cursor.execute("INSERT INTO shots (shotname) VALUES ('{0}')".format(shotname))

        # Create a DB for the shot
        shotConnection, shotCur = self._get_shotdb(shotname)
        # take_number, path, created_on, created_by
        shotCur.execute('CREATE TABLE takes (take_number INTEGER PRIMARY KEY, path text, created_on datetime, created_by text, task_type text)')
        shotCur.execute('CREATE TABLE reviews (review_number INTEGER PRIMARY KEY)')

        shotConnection.commit()
        shotConnection.close()
        self.connection.commit()
        self.connection.close()

    def new_asset(self, assetname):
        """Create a new shot in the DB."""
        self.connect()
        if assetname in self.get_shots_or_assets(keepOpen=True, assets=True):
            raise ValueError('Asset {0} already exists in db.'.format(assetname))
        self.cursor.execute("INSERT INTO assets (assetname) VALUES ('{0}')".format(assetname))

        # Create a DB for the shot
        shotConnection, shotCur = self._get_shotdb(assetname)
        # take_number, path, created_on, created_by
        shotCur.execute('CREATE TABLE takes (take_number INTEGER PRIMARY KEY, path text, created_on datetime, created_by text, task_type text)')
        shotCur.execute('CREATE TABLE reviews (review_number INTEGER PRIMARY KEY)')

        shotConnection.commit()
        shotConnection.close()
        self.connection.commit()
        self.connection.close()

    # Takes
    def new_take(self, take):
        """Create a new take for a shot."""
        print("New take Called")
        # Create a DB for the shot
        shotConnection, shotCur = self._get_shotdb(take.shot.name)

        call = 'INSERT INTO takes (take_number, path, created_on, created_by, task_type) ' \
               'values({take_number}, "{path}", "{created_on}", "{created_by}", "{task_type}")'.format(take_number=take.take_number,
                                                                                  path=take.path,
                                                                                  created_on=take.created_on,
                                                                                  created_by=take.created_by,
                                                                                  task_type=take.task_type)
        print(call)
        shotCur.execute(call)
        shotConnection.commit()
        shotConnection.close()

    # Util

    def _get_shotdb(self, shot):
        """Get the path to the shot DB file."""
        shotDbPath = os.path.join(self.dataDir, '{0}_shotdb.sqlite'.format(shot))
        shotConnection = sqlite3.connect(shotDbPath)
        shotCur = shotConnection.cursor()
        return shotConnection, shotCur

class MySqlDatabase(Database):
    """Connect to a mySql database."""

    def __init__(self, dm):
        """Create a database connection."""
        import mysql.connector
        self._dm = _dm

        self._connectionsettings = self._dm.settings.get('MYSQL_SETTINGS', None)
        if not self._connectionsettings:
            raise AttributeError("No database information is set in the settings object.")

        self.dataconn = mysql.connector.connect(host=self._connectionsettings['host'],
                                                user=self._connectionsettings['user'],
                                                passwd=self._connectionsettings['password'],
                                                port=self._connectionsettings['port'])



