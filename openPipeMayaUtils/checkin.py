import datamanager
from openPipeMayaUtils import utils
import maya.cmds as cmds
# from PyQt5 import QtGui, QtCore, uic
# import sip
import maya.OpenMayaUI as mui


'''
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
'''

def checkin(name, project=None):
    """Check in a new shot or asset to the system."""
    if not project:
        project = utils.get_project()
    print(project)
    dm = datamanager.DataManager(project)
    # Check to see if the asset or shot exists and create it if not
    workon = dm.get_shot_or_asset(name)

    node_settings = dm.settings.MAYA_NODE_PARSER
    filelist = {}

    for ntype, attr in node_settings.items():
        for node in cmds.ls(et=ntype):
            filelist[node] = cmds.getAttr("{0}.{1}".format(node, attr))

    print(filelist)



