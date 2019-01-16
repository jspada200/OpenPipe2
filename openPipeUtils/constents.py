# Copyright 2018 - James Spadafora
# Open Pipe
# Utility classes for interacting with the DB.

SOURCES = 'sources'
SCENES = 'scenes'

# Database
SHOTSANDASSETSDB = 'op_shots'

SQLMAKETAKESHOTS = 'CREATE TABLE shots (shotname STRING PRIMARY KEY)'
SQLMAKETAKEASSETS = 'CREATE TABLE assets (assetname STRING PRIMARY KEY)'

SQLSELECTASSETS = 'SELECT * from assets'
SQLSELECTSHOTS = 'SELECT * from shots'
SQLSELECTFROMSHOTS = 'SELECT * from shots WHERE shotname="{0}"'
SQLSELECTFROMASSETS = 'SELECT * from assets WHERE assetname="{0}"'
SQLSELECTFROMTAKES = 'SELECT * from takes WHERE shotname="{0}"'
SQLSELECTFROMREVIEWS = 'SELECT * from reviews WHERE shotname="{0}"'

SQLLOCALSELECTFROMTAKES = 'SELECT * from takes'
SQLLOCALSELECTFROMREVIEWS = 'SELECT * from reviews'

SQLREMOTESELECTFROMTAKES = 'SELECT * from takes WHERE shotname="{0}"'
SQLREMOTESELECTFROMREVIEWS = 'SELECT * from reviews WHERE shotname="{0}"'

SQLNEWSHOT = 'INSERT INTO shots (shotname) VALUES ("{0}")'
SQLNEWASSET = 'INSERT INTO assets (assetname) VALUES ("{0}")'

SQLMAKETAKETABLE = 'CREATE TABLE takes (take_number INTEGER PRIMARY KEY, path text, created_on datetime, created_by text, task_type text, shotname text)'
SQLMAKEREVIEWSTABLE = 'CREATE TABLE reviews (review_number INTEGER PRIMARY KEY, shotname text)'

SQLREMOTENEWTAKE = ('INSERT INTO takes (take_number, path, created_on, created_by, task_type, shotname) '
                    'values({take_number}, "{path}", "{created_on}", "{created_by}", "{task_type}", "{shotname}")')

# DATA IDENTIFIERS
DATA_TYPE_ID = '#type'
TASK_DATA_TYPE = '#task'
AUTHOR = 'author'
DATE = 'date'
NOTES = 'notes'
SCENE_FILE = 'scene_file'
SUPPORT_FILES = 'supporting_files'
APP_FILES = 'application_files'