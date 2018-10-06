import datamanager
from mayaUtils import utils
import maya.cmds as cmds
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
    dm = datamanager.DataManager(project)
    # Check to see if the asset or shot exists and create it if not
    workon = dm.get_shot_or_asset(name)

    node_settings = dm.settings.MAYA_NODE_PARSER
    filelist = {}
    for node in cmds.ls():
        ntype = cmds.nodeType(node)
        if ntype in node_settings.keys():
            filelist[node] = cmds.getAttr(node, node_settings[ntype])
    print filelist


