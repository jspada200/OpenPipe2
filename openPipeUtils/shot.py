# Copyright 2018 - James Spadafora
# Open Pipe
# Data type for representing a shot in the API

class Shot(object):
    """Rep a shot in the API."""

    def __init__(self, shot, dm=None, **kwargs):
        """Init the shot object."""
        self.name = shot
        self._dm = dm
        for k, v in kwargs.items():
            setattr(self, k, v)
        if self._dm:
            self._build_shot()

    def _build_shot(self):
        """Init this shot object"""
        shot_data = self._dm.database.get_shot_data(self.name)
        for k, v in shot_data.items():
            if k == 'reviews':
                # Build review objects
                pass
            elif k == 'takes':
                # Build take objects
                pass
            else:
                setattr(self, k, v)