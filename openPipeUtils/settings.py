# Copyright 2018 - James Spadafora
# Open Pipe
# Gather and store settings for the project

import inspect
import os
import json


class Settings(object):
    """Object for interacting with settings for a project."""

    def __init__(self, projectBase=None):
        """Load and generate inital settings for a project."""
        if not projectBase:
            # This file/core/openPipe/scripts/projectroot
            self.projectBase = os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())),
                                            '..',
                                            '..',
                                            '..',
                                            '..')
        else:
            self.projectBase = projectBase

        # Find the settings json
        self.jsonSettingsFile = os.path.join(self.projectBase, 'openPipe', 'settings', 'openPipeSettings.json')

        if not os.path.isfile(self.jsonSettingsFile):
            self.generateInitalSettings()

        with open(self.jsonSettingsFile) as f:
            self.settings = json.load(f)

    def generateInitalSettings(self):
        """Generate the base project settings."""
        pass