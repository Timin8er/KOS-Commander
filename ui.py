from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox
from PyQt5.QtGui import QIcon
from .mainWindowDesigner import Ui_KPI
from .scriptEditorDesigner import Ui_scriptEditorDialog
import os
from . import kos_connection, icons
from .scriptsTreeModel import scriptsTreeModel, scriptObject


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

        self.btnSaveProfile.clicked.connect(self.saveProfile)
        self.btnSaveProfile.setIcon(QIcon(icons.SAVE))

        # self.connection = kos_connection('127.0.0.1', '5410', 10)

        self.btnScriptInterupt.clicked.connect(lambda: self.connection.ks_stop())

        self.profiles_edit_unlocked = True
        self.btnLockProfiles.clicked.connect(self.toggleProfilesLock)
        self.btnLockProfiles.setIcon(QIcon(icons.LOCKED))

        self.command_edit_unlocked = True
        self.btnLockCommand.clicked.connect(self.toggleCommandLock)
        self.btnLockCommand.setIcon(QIcon(icons.LOCKED))

        self.scripts_tree_model = scriptsTreeModel()
        self.scriptsView.setModel(self.scripts_tree_model)
        self.scriptsView.expandAll()
        self.scriptsView.resizeColumnToContents(0)



    def toggleProfilesLock(self):
        self.profiles_edit_unlocked ^= True
        self.btnSaveProfile.setEnabled(self.profiles_edit_unlocked)
        self.profileNameEdit.setEnabled(self.profiles_edit_unlocked)
        self.btnLockProfiles.setIcon(QIcon(icons.LOCKED) if self.profiles_edit_unlocked else QIcon(icons.UNLOCKED))


    def toggleCommandLock(self):
        self.command_edit_unlocked ^= True
        self.commandEdit.setEnabled(self.command_edit_unlocked)
        self.btnLockCommand.setIcon(QIcon(icons.LOCKED) if self.command_edit_unlocked else QIcon(icons.UNLOCKED))


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

    def saveProfile(self):
        self.scripts_tree_model.save()
        QMessageBox.information(self, 'Save', 'Scripts Saved')


class scriptEditor(QDialog, Ui_scriptEditorDialog):

    def __init__(self, script, *args, **kwargs):
        QDialog.__init__(self, *args, **kwargs)

        self.setupUi(self)

        self.script = script

        self.nameEdit.setText(script.name)
        self.folderEdit.setText(script.folder)
        self.scriptTextEdit.setPlainText(script.text)


    @classmethod
    def edit(cls, script):
        if not script:
            return

        dlg = cls(script)
        if dlg.exec_():
            script.name = dlg.nameEdit.text()
            script.folder = dlg.folderEdit.text()
            script.text = dlg.scriptTextEdit.toPlainText()
            return True
