# Copyright 2018 - James Spadafora
# Open Pipe
# Utility classes for interacting with the DB.
import sqlite3
import mysql.connector as mysqlcon
from datetime import datetime
import os
from openPipeUtils import constents

class Database(object):
    """Base class for interacting with different DBs."""

    def __init__(self, dataDir, init_db=False):
        """Set up object."""
        pass

    def get_shots_or_assets(self):
        """Get a list of all shots."""
        return []

class SQLiteDatabase(Database):
    """Class for storing and getting data from an SQLite file."""

    def __init__(self, dm, dataDir, initDb=False):
        """
        Set up object and create a connection.

        Args:
            sqlitePath(str): Path to the datadir
            initFile(bool): Set up the file if it does not exist.
        """
        self.dataDir = dataDir
        sqlitePath = os.path.join(dataDir, 'db.sqlite')
        self._dm = dm

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
        self.cursor.execute(constents.SQLMAKETAKESHOTS)
        self.cursor.execute(constents.SQLMAKETAKEASSETS)
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
            self.cursor.execute(constents.SQLSELECTASSETS)
        else:
            self.cursor.execute(constents.SQLSELECTSHOTS)
        all = self.cursor.fetchall()
        if not keepOpen:
            self.connection.close()
        return all

    def get_shot_data(self, shot):
        """Get info for this shot."""
        shotdata = {}
        asset = False

        self.connect()
        self.cursor.execute(constents.SQLSELECTFROMSHOTS.format(shot))
        info = self.cursor.fetchone()
        if not info:
            asset = True
            self.cursor.execute(constents.SQLSELECTFROMASSETS.format(shot))
            info = self.cursor.fetchone()

        if not info:
            raise KeyError('No such shot {0} exists'.format(shot))

        shotdata['name'] = info[0]

        if not asset:
            shotdata['firstFrame'] = 0
            shotdata['lastFrame'] = 100
        self.connection.close()

        shotConnection, shotCur = self._get_shotdb(shot)
        shotCur.execute()
        all = shotCur.fetchall(constents.SQLLOCALSELECTFROMTAKES)

        takes = []
        # take_number INTEGER PRIMARY KEY, path text, created_on datetime, created_by text, task_type text
        for take in all:
            takes.append({'take_number': take[0],
                          'path': take[1],
                          'created_on': datetime.strptime(take[2], '%Y-%m-%d %X.%f'),
                          'created_by': take[3],
                          'task_type': take[4]})
        shotdata['takes'] = takes

        shotCur.execute(constents.SQLLOCALSELECTFROMREVIEWS)
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

    def __init__(self, dm, dataDir, initDb=False):
        """Create a database connection."""
        import mysql.connector
        self._dm = dm
        self.datadir = dataDir
        self._connectionsettings = self._dm.settings.get('MYSQL_SETTINGS', None)
        if not self._connectionsettings:
            raise AttributeError("No database information is set in the settings object.")
        if initDb:
            self.connect()

    def connect(self):
        self.connection = mysqlcon.connect(host=self._connectionsettings['host'],
                                           user=self._connectionsettings['user'],
                                           passwd=self._connectionsettings['password'],
                                           port=self._connectionsettings['port'])

        self.cursor = self.connection.cursor()

        # Check to see if our tables exist. If not, create them.
        self.cursor.execute("SHOW DATABASES")

        x = self.cursor.fetchall()

        if x:
            print("CURSOR " + str(x))

        if 'mydatabase2' not in str(x):
            self.init_starting_db()

    def init_starting_db(self):
        """Set up the main index for a new project."""
        print("Creating shots DB")
        self.cursor.execute("CREATE DATABASE mydatabase2")
        self.cursor.execute("USE mydatabase2")

        self.cursor.execute("CREATE TABLE shots (id INT AUTO_INCREMENT PRIMARY KEY, shotname VARCHAR(255))")
        self.cursor.execute("CREATE TABLE assets (id INT AUTO_INCREMENT PRIMARY KEY, assetname VARCHAR(255))")
        self.cursor.execute(constents.SQLMAKETAKETABLE)
        self.cursor.execute(constents.SQLMAKEREVIEWSTABLE)

    def get_shots_or_assets(self, keepOpen=False, assets=False):
        """Get a list of all shots."""
        self.cursor.execute("USE mydatabase2")
        if assets:
            self.cursor.execute("SELECT * from assets")
        else:
            self.cursor.execute("SELECT * from shots")
        all = self.cursor.fetchall()

        return all

    def get_shot_data(self, shot):
        """Get info for this shot."""
        self.cursor.execute("USE mydatabase2")
        shotdata = {}
        asset = False
        print(constents.SQLSELECTFROMSHOTS.format(shot))
        self.cursor.execute(constents.SQLSELECTFROMSHOTS.format(shot))
        info = self.cursor.fetchone()
        if not info:
            asset = True
            print(constents.SQLSELECTFROMASSETS.format(shot))
            self.cursor.execute(constents.SQLSELECTFROMASSETS.format(shot))
            info = self.cursor.fetchone()

        if not info:
            raise KeyError('No such shot {0} exists'.format(shot))

        shotdata['name'] = info[0]

        if not asset:
            shotdata['firstFrame'] = 0
            shotdata['lastFrame'] = 100
        self.cursor.execute(constents.SQLREMOTESELECTFROMTAKES.format(shot))
        all = self.cursor.fetchall()

        takes = []
        # take_number INTEGER PRIMARY KEY, path text, created_on datetime, created_by text, task_type text
        for take in all:
            takes.append({'take_number': take[0],
                          'path': take[1],
                          'created_on': datetime.strptime(take[2], '%Y-%m-%d %X.%f'),
                          'created_by': take[3],
                          'task_type': take[4]})
        shotdata['takes'] = takes

        self.cursor.execute(constents.SQLREMOTESELECTFROMREVIEWS.format(shot))
        all = self.cursor.fetchall()

        reviews = []
        for review in all:
            reviews.append({'id': review[0]})
        shotdata['reviews'] = reviews

        return shotdata

    def new_shot(self, shotname, firstframe, lastframe):
        """Create a new shot in the DB."""
        self.cursor.execute("USE mydatabase2")
        if shotname in self.get_shots_or_assets():
            raise ValueError('Shot {0} already exists in db.'.format(shotname))
        self.cursor.execute(constents.SQLNEWSHOT.format(shotname))

    def new_asset(self, assetname):
        """Create a new shot in the DB."""
        self.cursor.execute("USE mydatabase2")
        if assetname in self.get_shots_or_assets(assets=True):
            raise ValueError('Asset {0} already exists in db.'.format(assetname))
        self.cursor.execute(constents.SQLNEWASSET.format(assetname))

    # Takes
    def new_take(self, take):
        """Create a new take for a shot."""
        self.cursor.execute("USE mydatabase2")
        print("New take Called")
        # Create a DB for the shot
        shotConnection, shotCur = self._get_shotdb(take.shot.name)

        call = constents.SQLREMOTENEWTAKE.format(take_number=take.take_number,
                                                 path=take.path,
                                                 created_on=take.created_on,
                                                 created_by=take.created_by,
                                                 task_type=take.task_type,
                                                 shotname=take.shot.name)
        self.cursor.execute(call)

    def __del__(self):
        self.connection.close()