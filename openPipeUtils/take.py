# Copyright 2018 - James Spadafora
# Open Pipe
# Data type for representing a take in the API

class Take(object):
    """Rep a take in the API."""

    def __init__(self, shot, takeData=None, **kwargs):
        """
        Init the take object.
        Args:
            shot(openPipe Shot Object): The shot to create this take for
            takeNumber (int) index for this take.
            path(str): Published path to the json take data
            createdOn(datetime): When this take was made
            createdBy(str): Who created this take
            takeData(dict): Used for construction of an existing take.
        """
        self.shot = shot
        self.take = take
        for k, v in kwargs.items():
            setattr(self, k, v)

        if takeData:
            self._build_take(takeData)

    def _build_take(self, takeData):
        """Build a take from the dict provided."""
        for k, v in takeData.items():
            setattr(self, k, v)