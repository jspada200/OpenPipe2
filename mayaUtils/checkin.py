# Copyright 2018 - James Spadafora
# Open Pipe
# Check in a new asset or shot to openPipe
import datamanager
from mayaUtils import utils
from PyQt4 import QtGui, QtCore, uic
import maya.OpenMayaUI as mui
import sip


class CheckinDialog(QtGui.QDialog):
    """A Dialog to check in a new shot or asset."""

    def __init__(self, parent=getMayaWindow()):
        super(CheckinDialog, self).__init__(parent)

        #Window title
        self.setWindowTitle('openPipe Checkin')


def getMayaWindow():
    """Get the maya main window as a QMainWindow instance."""
    ptr = mui.MQtUtil.mainWindow()
    return sip.wrapinstance(long(ptr), QtCore.QObject)


def checkin(name, tasktype, asset=False, project=None):
    """Check in a new shot or asset to the system."""
    if not project:
        project = utils.get_project()
    dm = datamanager.DataManager
    # Check to see if the asset or shot exists and create it if not
    workon = dm.get_shot_or_asset(name)

    # Build a list of all directories