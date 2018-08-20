# Copyright 2018 - James Spadafora
# Open Pipe
# Utility classes for interacting with the file system.

import os


class Storage(object):
    """Base class for writing to the file system."""

    def __init__(self, baseProject):
        """
        Set up object.

        Args:
            baseProject (str): The base folder for the project
        """
        if not os.path.isdir(baseProject):
            raise IOError('No such dir {0} exists'.format(baseProject))
        self.baseProject = baseProject
