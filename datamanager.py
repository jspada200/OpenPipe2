# Copyright 2018 - James Spadafora
# Open Pipe
# Main low level AIP object for interacting with openPipe

from openPipeUtils import settings, database, shot, filemanager
import os
import sys
import inspect


class DataManager(object):
    """Object for doing tasks with openPipe"""

    def __init__(self, projectBase):
        """Init the object for interacting with openPipe."""
        cm = inspect.getfile(inspect.currentframe())
        sys.path.append(os.path.join(os.path.dirname(cm), 'openPipeHooks'))

        self.files = filemanager.FileManager(projectBase, self)
        self.settings = settings.Settings(projectBase)
        self.database = database.SQLiteDatabase(os.path.join(projectBase,
                                                             'openPipe',
                                                             'data'),
                                                initFile=True)

    def get_shot_or_asset(self, name):
        """Return a shot or asset object."""
        try:
            return self.get_shot(name)
        except KeyError:
            try:
                return self.get_asset(name)
            except KeyError:
                raise KeyError("No such shot or asset.")


    # SHOTS
    def get_shots(self):
        """List all shots in the project."""
        return [x[0] for x in self.database.get_shots_or_assets()]

    def new_shot(self, shotname):
        """
        Create a new shot in the db and on the file system.
        Args:
            shotname(str) Unique ID for this shot

        Returns:
            New openPipe Shot
        """
        if shotname in self.get_shots():
            raise KeyError("Unable to create shot. This shot already exists!")
        self.database.new_shot(shotname, 0, 10)
        self.files.new_shot(shotname)
        return self.get_shot(shotname)

    def get_shot(self, shotname):
        """Build a shot object."""
        return shot.Shot(shotname, dm=self)

    # ASSETS

    def get_assets(self):
        """List all shots in the project."""
        return [x[0] for x in self.database.get_shots_or_assets(assets=True)]

    def new_asset(self, assetname):
        """
        Create a new shot in the db and on the file system.
        Args:
            assetname(str) Unique ID for this asset

        Returns:
            New openPipe Asset
        """
        if assetname in self.get_assets():
            raise KeyError("Unable to create asset. This asset already exists!")
        self.database.new_asset(assetname)
        self.files.new_asset(assetname)
        return self.get_asset(assetname)

    def get_asset(self, assetname):
        """Build a shot object."""
        return shot.Asset(assetname, dm=self)