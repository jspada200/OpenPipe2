# Copyright 2018 - James Spadafora
# Open Pipe
# Main low level AIP object for interacting with openPipe

from openPipeUtils import storage, settings, database, shot
import os

class DataManager(object):
    """Object for doing tasks with openPipe"""

    def __init__(self, projectBase):
        """Init the object for interacting with openPipe."""
        self.storage = storage.Storage(projectBase)
        self.settings = settings.Settings(projectBase)
        self.database = database.SQLiteDatabase(os.path.join(projectBase,
                                                             'openPipe',
                                                             'data'),
                                                initFile=True)
    def get_shots(self):
        """List all shots in the project."""
        return self.database.get_shots()

    def new_shot(self, shotname, firstframe, lastframe):
        """Create a new shot in the db and on the file system."""
        self.database.new_shot(shotname, firstframe, lastframe)

    def get_shot(self, shotname):
        """Build a shot object."""
        return shot.Shot(shotname, dm=self)