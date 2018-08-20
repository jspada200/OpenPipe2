# Copyright 2018 - James Spadafora
# Open Pipe
# Data type for representing a component in the API

class Component(object):
    """Rep a shot in the API."""

    def __init__(self, dm, shot, take, path):
        """Init the shot object."""
        self._dm = dm
        self.shot = ""
        self.takeNum = 0
        self.path = ""
