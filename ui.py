from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtGui import QIcon
from .mainWindowDesigner import Ui_KPI
import os
from . import kos_connection, icons
from .scriptsTreeModel import scriptsTreeModel, scriptObject
from .inputProfilesModel import profileObject, inputsListModel
from .scriptEditor import scriptEditor


class mainWindow(QMainWindow, Ui_KPI):


    def __init__(self, *args, **kwargs):
        QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.setWindowIcon(QIcon(icons.ROCKET))

        self.btnConnection.setIcon(QIcon(icons.GPS_DISCONNECTED))

        self.btnNewScript.setIcon(QIcon(icons.NEW))
        self.btnNewScript.clicked.connect(self.newScript)

        self.btnEditScript.setIcon(QIcon(icons.EDIT))
        self.btnEditScript.clicked.connect(self.editScript)

        self.btnDeleteScript.setIcon(QIcon(icons.DELETE))
        self.btnDeleteScript.clicked.connect(self.deleteScript)

        self.btnSaveScripts.clicked.connect(self.saveScripts)
        self.btnSaveScripts.setIcon(QIcon(icons.SAVE))

        self.btnNewProfile.clicked.connect(self.newProfile)
        self.btnNewProfile.setIcon(QIcon(icons.NEW))

        self.btnDeleteProfile.clicked.connect(self.removeProfile)
        self.btnDeleteProfile.setIcon(QIcon(icons.DELETE))

        # self.connection = kos_connection('127.0.0.1', '5410', 10)

        self.btnLockScripts.clicked.connect(self.toggleScriptsLock)
        self.btnLockProfiles.clicked.connect(self.toggleProfilesLock)
        self.btnLockCommand.clicked.connect(self.toggleCommandLock)
        self.btnScriptInterupt.clicked.connect(lambda: self.connection.ks_stop())

        self.btnClearCommand.setIcon(QIcon(icons.CLEAR))
        self.btnClearCommand.clicked.connect(self.clear)

        self.scripts_tree_model = scriptsTreeModel()
        self.scriptsView.setModel(self.scripts_tree_model)
        self.scriptsView.expandAll()
        self.scriptsView.resizeColumnToContents(0)

        # ======================================================================
        self.profiles_model = inputsListModel()
        self.profilesView.setModel(self.profiles_model)

        self.clear()


    def clear(self):
        self.script_edit_unlocked = False
        self.toggleScriptsLock()

        self.profiles_edit_unlocked = False
        self.toggleProfilesLock()

        self.command_edit_unlocked = False
        self.toggleCommandLock()



    def toggleScriptsLock(self):
        self.script_edit_unlocked ^= True
        self.btnNewScript.setEnabled(self.script_edit_unlocked)
        self.btnEditScript.setEnabled(self.script_edit_unlocked)
        self.btnDeleteScript.setEnabled(self.script_edit_unlocked)
        self.btnLockScripts.setIcon(QIcon(icons.TOGGLE_ON) if self.script_edit_unlocked else QIcon(icons.TOGGLE_OFF))

    def toggleProfilesLock(self):
        self.profiles_edit_unlocked ^= True
        self.btnNewProfile.setEnabled(self.profiles_edit_unlocked)
        self.profileNameEdit.setEnabled(self.profiles_edit_unlocked)
        self.btnDeleteProfile.setEnabled(self.profiles_edit_unlocked)
        self.btnLockProfiles.setIcon(QIcon(icons.TOGGLE_ON) if self.profiles_edit_unlocked else QIcon(icons.TOGGLE_OFF))


    def toggleCommandLock(self):
        self.command_edit_unlocked ^= True
        self.commandEdit.setEnabled(self.command_edit_unlocked)
        self.btnLockCommand.setIcon(QIcon(icons.TOGGLE_ON) if self.command_edit_unlocked else QIcon(icons.TOGGLE_OFF))


    def currentScript(self):
        index = self.scriptsView.currentIndex()
        node = index.internalPointer()
        if not node:
            return
        script = index.internalPointer()._data

        if script and isinstance(script, scriptObject):
            return script
        else:
            return None


    def editScript(self):
        if scriptEditor.edit(self.currentScript()):
            self.scripts_tree_model.refresh(self.scripts_tree_model._data)
            self.scriptsView.expandAll()


    def newScript(self):
        obj = scriptObject()
        if scriptEditor.edit(obj):
            self.scripts_tree_model.insertScript(obj)
            self.scriptsView.expandAll()


    def deleteScript(self):
        script = self.currentScript()
        if not script:
            return

        msg = f'Are you sure you want to delete this script "{script.name}"?'
        reply = QMessageBox.warning(self, 'Delete', msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.scripts_tree_model.removeScript(script)
            self.scriptsView.expandAll()

    def saveScripts(self):
        self.scripts_tree_model.save()
        QMessageBox.information(self, 'Save', 'Scripts Saved')


    def newProfile(self):
        pass


    def removeProfile(self):
        pass
