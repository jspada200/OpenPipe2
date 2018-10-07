# Copyright 2018 - James Spadafora
# Open Pipe
# Utilities for working with maya
import maya.cmds as cmds


def get_project():
    """Get the currently open maya project and validate."""
    proj_path = cmds.workspace(q=True, rd=True)
    # Check to see if the workspace has a openPipe proj already

    return proj_path