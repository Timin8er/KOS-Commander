from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QInputDialog, QAbstractScrollArea
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QAbstractItemModel, Qt, QModelIndex
from .scriptEditorDesigner import Ui_scriptEditorDialog
from . import icons
from .inputModel import inputsTableModel, inputTableDelagate
from KOSCommander.core import inputObject

class scriptEditor(QDialog, Ui_scriptEditorDialog):

    def __init__(self, script, *args, **kwargs):
        QDialog.__init__(self, *args, **kwargs)

        self.setupUi(self)

        self.script = script
        self.inputsForm = None

        self.nameEdit.setText(script.name)
        self.folderEdit.setText(script.folder)
        self.scriptTextEdit.setPlainText(script.text)
        self.descriptionEdit.setPlainText(script.description)
        self.isCommandCheckBox.setChecked(script.isCommand)

        self.inputs_model = inputsTableModel(script=script)
        self.inputsView.setModel(self.inputs_model)
        self.inputsView.setItemDelegate(inputTableDelagate())
        self.inputsView.resizeColumnToContents(0)
        self.inputsView.resizeColumnToContents(1)
        self.inputsView.resizeColumnToContents(2)
        self.inputs_model.dataChanged.connect(lambda: self.inputsView.resizeColumnToContents(0))
        self.inputs_model.dataChanged.connect(lambda: self.inputsView.resizeColumnToContents(1))
        self.inputs_model.dataChanged.connect(lambda: self.inputsView.resizeColumnToContents(2))

        self.btnAddInput.setIcon(QIcon(icons.NEW))
        self.btnAddInput.clicked.connect(self.appemndNewInput)

        self.btnRemoveInput.setIcon(QIcon(icons.DELETE))
        self.btnRemoveInput.clicked.connect(self.removeCurrentInput)


    def updateInputWidgets(self):
        self.inputsHLayout.removeWidget(self.inputsForm)

        self.inputsForm = QFormLayout()

        for i in script.inputs:
            nameedit = QLineEdit(i.name)
            nameedit.editingFinished.connect(lambda: setattr(i, 'name', nameEdit.text()))
            self.inputsForm.addRow(nameedit, i.getEditWidget())

        self.verticalLayout.insertLayout(1, self.inputsForm)


    def appemndNewInput(self):
        obj = inputObject()
        self.inputs_model.insertInput(-1, obj)


    def removeCurrentInput(self):
        index = self.inputsView.currentIndex()
        if index.row() > -1:
            input = self.script.inputs[index.row()]
            self.inputs_model.removeInput(input)


    @classmethod
    def edit(cls, script):
        if not script:
            return

        dlg = cls(script)
        if dlg.exec_():
            script.name = dlg.nameEdit.text()
            script.folder = dlg.folderEdit.text()
            script.text = dlg.scriptTextEdit.toPlainText()
            script.description = dlg.descriptionEdit.toPlainText()
            script.isCommand = dlg.isCommandCheckBox.isChecked()
            return True
