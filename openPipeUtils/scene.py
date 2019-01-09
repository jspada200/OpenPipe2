# Copyright 2018 - James Spadafora
# Open Pipe
# Data type for representing a scene containing file paths.

import os
import datetime
import json


class Scene():
    """Interact with a scene file."""

    def __init__(self, json_path=None, scene_dict=None):
        """
        Create empty object or from a json file.
            Args:
                json_path(str): A path to a json file containing the scene
                scene_dict(dict): If the info exists in dict form, use that.
        """
        self.tasks = []
        self._data = {}

        if scene_dict:
            self._data = scene_dict
        elif json_path and os.path.exists(json_path):
            self._data = json.loads(json_path)

    def merge(self, scene_obj):
        """Merge scene objects with this object being the main object."""
        new_data = scene_obj.update(self._data)
        self._data = new_data
        self._validate()

    def get_tasks(self):
        """Return top level tasks."""
        task_names = []
        for task_name, task_info in self._data.iteritems():
            if task_info.get('type') == 'task':
                task_names.append(task_name)
        return task_names

    def get_task(self, task_name):
        """Return dict of data for a task."""
        try:
            task_info = self._data[task_name]
            if task_info.get('type') == 'task':
                return task_info
            return {}
        except KeyError:
            return {}

    def create_or_update_task(self, task_name, author, notes, app_data):
        """
        Create a new task in the scene.

        Args:
            task_name(str): The name of the task to update or create
            author(str): The person editing this task
            notes (str): Notes associated with this task
            app_data(dict): Application specific dict with information about the files in this checkin.
                Should be structured like {app_name: { app_data=app_data }}
        """
        new_task_obj = Task(task_name,
                            author,
                            notes=notes)
        for app_name, app_info in app_data.iteritems():
            new_task_obj.add_application(app_name,
                                         app_info['scene'],
                                         additional_supporting_files=app_info.get('supporting_files', {}))
        self.tasks.append(new_task_obj)

    def _validate(self):
        """Ensure this scene is valid. Raise exception if not valid."""
        return True

class Task():
    """Represents something someone has done that has files associated with it."""

    def __init__(self, name, author, notes=None, date=None):
        """
        :param name: The name of the task. This can be anything that needs to be published
        :param author: The person who is editing this task
        :param notes: Any notes about this task
        :param date: Optional date, this is generated when there is a publish.
        """
        self.name = name
        self.author = author
        self.notes = notes
        self.date = date
        self.application_info = {}

    def add_application(self, application_name, scene_file, additional_supporting_files={}):
        """
        Add an application to this task.

        :param application_name: The name of the application that is being added
        :param scene_file: The main source file for the application
        :param additional_supporting_files: Files that are referenced by the main source file.
        """

        self.application_info[application_name] = {"scene": scene_file,
                                                   "supporting_files": additional_supporting_files}
