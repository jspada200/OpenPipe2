# Copyright 2018 - James Spadafora
# Open Pipe
# Data type for representing a shot in the API

from . import take

import os
import getpass
from datetime import datetime


class Shot():
    """Rep a shot in the API."""

    def __init__(self, shot, takes=[], reviews=[], dm=None, **kwargs):
        """
        Init the shot object.
        Args:
            shot(str): The shot ID
            dm(openPipe DataManager): Used to saving information on the shot
            takes(list:openPipe Take Objects)
            reviews(list:openPipe Review Objects)
        """
        self.name = shot
        self.takes = takes
        self.reviews = reviews
        self.workon_type = 'shot'
        self._dm = dm
        for k, v in kwargs.items():
            setattr(self, k, v)

        if self._dm:
            self._build_shot()
        self.dir = self._dm.files.get_shot_or_asset_dir(self.name)

    def _build_shot(self):
        """Init this shot object"""
        shot_data = self._dm.database.get_shot_data(self.name)
        for k, v in shot_data.items():
            if k == 'reviews':
                # Build review objects
                pass
            elif k == 'takes':
                if v:
                    for t in v:
                        self.takes.append(take.Take(self, take_data=t))
            else:
                setattr(self, k, v)

    def create_new_take(self, task_type, path="", created_by=None, hook_list=[]):
        """Build a new take for this shot."""
        take_number = len(self.takes)
        if not created_by:
            created_by = getpass.getuser()
        path, retarget_list = self._dm.files.new_take(self, take_number, path)
        new_take = take.Take(self,
                             take_number=take_number,
                             task_type=task_type,
                             path=path,
                             created_on=datetime.now(),
                             created_by=created_by,
                             retarget_list=retarget_list)
        self._dm.database.new_take(new_take)
        self.takes.append(new_take)
        return self.takes[-1], retarget_list

    def create_task_dir(self, tasktype):
        """Create a new taskdir for this shot."""
        tt = os.path.join(self.dir, tasktype)
        os.mkdir(tt)
        self._dm.files.build_task_struct(tt)

class Asset(Shot):
    """Rep a asset in the API."""

    def __init__(self, asset, takes=[], reviews=[], dm=None, **kwargs):
        """
        Init the Asset object.
        Args:
            asset(str): The asset ID
            dm(openPipe DataManager): Used to saving information on the shot
            takes(list:openPipe Take Objects)
            reviews(list:openPipe Review Objects)
        """
        Shot.__init__(self, asset, takes, reviews, dm, **kwargs)
        self.workon_type = 'asset'
