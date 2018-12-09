# Copyright 2018 - James Spadafora
# Open Pipe
# Utility classes for interacting with the DB.

import os
import re
import shutil
import json
from openPipeUtils import constents as opc
from openPipeHooks import maya_checkin_hooks

class FileManager(object):
    """Base class for dealing with storing and organizing file on the file system."""

    def __init__(self, project_dir, dm):
        """
        Init the object.
        Args:
            project_dir(str): Base dir for the project.
        """
        if not os.path.exists(project_dir):
            raise IOError("No such dir exists")
        self.project_dir = project_dir
        self._dm = dm

    def new_shot(self, shotname):
        """Build the dirs needed for the new shot."""
        os.makedirs(os.path.join(self.project_dir, 'scenes', shotname, 'publish', 'takes'))
        os.makedirs(os.path.join(self.project_dir, 'scenes', shotname, 'publish', 'reviews'))

    def new_asset(self, assetname):
        """Build the dirs needed for the new asset."""
        os.makedirs(os.path.join(self.project_dir, 'assets', assetname, 'publish', 'takes'))
        os.makedirs(os.path.join(self.project_dir, 'assets', assetname, 'publish', 'reviews'))

    def new_take(self, shot, take_number, scene_path):
        """
        Take all objects in the json take file and move to publish area.

        Args:
            shot(openPipe Shot object)
            take_number(int)
            scene_path(str): Path to the json containing the assets in this shot.
        """
        new_path = os.path.join(self.project_dir, 'scenes', shot.name, 'publish', 'takes', str(take_number))
        os.makedirs(new_path)
        shot._dm.files.build_task_struct(new_path)
        if os.path.exists(scene_path):
            pubed_scene_path = os.path.join(new_path, "take.{0}.json".format(str(take_number)))
            self._copy(scene_path, pubed_scene_path)


            retarget_list = self.process_scene(pubed_scene_path)

        return new_path.replace(self.project_dir, ''), retarget_list

    def _determin_file_type(self, filepath):
        """Figure out which dir the file should be published to."""
        for pdir, regex in self._dm.settings.TASKDIR_MAPPING.items():
            for r in regex:
                if re.match(r, filepath):
                    return pdir

    def process_scene(self, scene_path):
        """
        Givin a json scene file, move all needed assets to the publish takes folder.

        This function will attempt to move assets defined in the scene json to the takes folder. The function returns
        a dict of the original paths to the remapped paths so applications can update the scenes to point to the
        updated paths before finishing the publish.
        """
        pub_dir = os.path.dirname(scene_path)
        scene_def = json.loads(open(scene_path).read())

        # First start with supporting files. These files are referenced by the scenes
        remapping = {}
        new_sources = {}

        file_regex_mapping = self._dm.settings.get("TASKDIR_MAPPING", {"other" : ["*."]})

        # Allow a list of files or a dict of pub dirs
        org_src = scene_def.get(opc.SOURCES, [])
        if type(org_src) == dict:
            org_src = [org_src]

        def _add_to_new_sources(ns, f_type, ppath):
            if f_type not in ns:
                ns[f_type] = []
            ns[f_type].append(ppath)
            return ns

        for src in scene_def.get(opc.SOURCES, []):
            # Search for a file type for this file.
            if type(src) == dict:
                for file_type, sub_src in src.items():
                    for sub_src_path in sub_src:
                        print(type(sub_src))
                        pub_path = os.path.join(pub_dir, file_type, os.path.basename(sub_src_path))
                        self._copy(sub_src_path, pub_path)
                        remapping[sub_src_path] = pub_path
                        new_sources = _add_to_new_sources(new_sources, file_type, pub_path)

            else:
                file_type = self._determin_file_type(src)
                pub_path = os.path.join(pub_dir, file_type, os.path.basename(src))
                self._copy(src, pub_path)
                remapping[src] = pub_path

                new_sources = _add_to_new_sources(new_sources, file_type, pub_path)

        scene_def[opc.SOURCES] = new_sources

        # Now ensure the scenes are copied over and the hooks are called to update
        # the paths in these scenes.
        for file_type, src_path in scene_def.get(opc.SCENES).items():
            print(src_path)
            pub_path = os.path.join(pub_dir, "scenes", file_type, os.path.basename(src_path))
            self._copy(src_path, pub_path)

            import sys
            print(sys.path)
            hookfunc = eval(self._dm.settings.CHECKIN_HOOKS[file_type])
            hookfunc(pub_path, remapping)
            scene_def[file_type] = pub_path
        with open(scene_path, 'w') as f:
            json.dump(scene_def, f)

        return remapping


    def get_shot_or_asset_dir(self, name):
        assets_dir = os.path.join(self.project_dir, 'assets')
        shots_dir = os.path.join(self.project_dir, 'scenes')
        print("ASSETS " + assets_dir)
        print("shots " + shots_dir)
        print("name " + str(name))

        if os.path.isdir(os.path.join(assets_dir, name)):
            return os.path.join(assets_dir, name)
        elif os.path.isdir(os.path.join(shots_dir, name)):
            return os.path.join(shots_dir, name)
        else:
            raise IOError("No such asset or shot dir exists.")

    # Publishing and taskdirs

    def build_task_struct(self, basepath):
        """Build a basic task stucture."""
        if os.path.exists(basepath):
            for d in self._dm.settings.TASKDIR_STRUCT:
                os.makedirs(os.path.join(basepath, d))

        else:
            raise IOError("No such basepath to build taskdir in. {0}".format(basepath))

    def _copy(self, src, target):
        """Ensure the target dir exists then copy the file."""
        if not os.path.exists(os.path.dirname(target)):
            os.mkdir(os.path.dirname(target))
        shutil.copy(src, target)
