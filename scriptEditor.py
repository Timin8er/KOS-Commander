from .scriptEditorDesigner import Ui_scriptEditorDialog
from . import icons
from PyQt5.QtWidgets import QDialog

class scriptEditor(QDialog, Ui_scriptEditorDialog):

    def __init__(self, script, *args, **kwargs):
        QDialog.__init__(self, *args, **kwargs)

        self.setupUi(self)

        self.script = script

        self.nameEdit.setText(script.name)
        self.folderEdit.setText(script.folder)
        self.scriptTextEdit.setPlainText(script.text)
        self.isCommandCheckBox.setChecked(script.isCommand)


    @classmethod
    def edit(cls, script):
        if not script:
            return

        dlg = cls(script)
        if dlg.exec_():
            script.name = dlg.nameEdit.text()
            script.folder = dlg.folderEdit.text()
            script.text = dlg.scriptTextEdit.toPlainText()
            script.isCommand = dlg.isCommandCheckBox.isChecked()
            return True
