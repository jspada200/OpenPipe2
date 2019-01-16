# Copyright 2018 - James Spadafora
# Open Pipe
# Data type for representing a scene containing file paths.

# Test Push

import os
import datetime
import json
from . import constents as const


class Scene():
    """Interact with a scene file."""

    def __init__(self, json_path=None, scene_dict=None):
        """
        Create empty object or from a json file.
            Args:
                json_path(str): A path to a json file containing the scene
                scene_dict(dict): If the info exists in dict form, use that.
        """
        self._data = {}

        self.filepath = json_path

        if scene_dict:
            self._data = scene_dict
        elif json_path and os.path.exists(json_path):
            self._data = json.loads(json_path)

    def _load_from_dict(self, scene_dict):
        """
        Create the info in this object form a loaded dict

        :param scene_dict: Dict with scene info
        :return: None
        """
        for data_key, info in scene_dict.iteritems():
            if type(info) == dict:
                if info.get(const.DATA_TYPE_ID, '') == const.TASK_DATA_TYPE:
                    new_task = Task(data_key,
                                    info.get(const.AUTHOR),
                                    info.get(const.NOTES),
                                    info.get(const.DATE))
                    for app, appinfo in info.get(const.APP_FILES):
                        new_task.add_application(app,
                                                 appinfo.get(const.SCENE_FILE),
                                                 appinfo.get(const.SUPPORT_FILES))
                    self._data[data_key] = new_task
                    continue

            exec('self.{0} = {1}'.format(data_key, info))


    def merge(self, scene_obj):
        """Merge scene objects with this object being the main object."""
        new_data = scene_obj.update(self._data)
        self._data = new_data

    def get_tasks(self):
        """Return top level tasks."""
        task_names = []
        for task_name, task_info in self._data.iteritems():
            if task_info.get(const.DATA_TYPE_ID) == const.TASK_DATA_TYPE:
                task_names.append(task_name)
        return task_names

    def get_task(self, task_name):
        """Return dict of data for a task."""
        try:
            task_info = self._data[task_name]
            if task_info.get(const.DATA_TYPE_ID) == const.TASK_DATA_TYPE:
                return task_info
            return {}
        except KeyError:
            return {}

    def create_task(self, task_name, author, notes, app_data):
        """
        Create a new task in the scene.

        Args:
            task_name(str): The name of the task to update or create
            author(str): The person editing this task
            notes (str): Notes associated with this task
            app_data(dict): Application specific dict with information about the files in this checkin.
                Should be structured like {app_name: { app_data=app_data }}
        """
        if task_name in self._data.keys():
            raise RuntimeError("Unable to create task. Task already exists.")
        new_task_obj = Task(task_name,
                            author,
                            notes=notes)
        for app_name, app_info in app_data.iteritems():
            new_task_obj.add_application(app_name,
                                         app_info[const.SCENE_FILE],
                                         additional_supporting_files=app_info.get(const.SUPPORT_FILES, {}))
        self._data[task_name] = new_task_obj

    def export(self, filepath):
        export_dict = {}
        for data_key, info in self._data.iteritems():
            if type(info) == Task:
                export_dict[data_key] = info._export()
            else:
                export_dict[data_key] = info


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

        self.application_info[application_name] = {const.SCENE_FILE: scene_file,
                                                   const.SUPPORT_FILES: additional_supporting_files}

    def _export(self):
        """
        Export a dict containing the data needed in the shotfile.

        :return: Dict containing information about this task.
        """
        if not self.date:
            self.date = datetime.datetime.utcnow()

        export_info = {const.AUTHOR: self.author,
                       const.NOTES: self.notes,
                       const.DATE: self.date,
                       const.APP_FILES: self.application_info,
                       const.DATA_TYPE_ID: const.TASK_DATA_TYPE}
        return export_info