from PyQt5 import QtWidgets
from PyQt5.QtCore import QAbstractItemModel, Qt, QModelIndex
from PyQt5.QtWidgets import QItemDelegate

def decode(inputsData):
    inputs = []

    for data in inputsData:
        cls_name = data.get('cls', None)
        obj = None

        if cls_name == 'stringInput':
            obj = stringInput.decode(data)
        elif cls_name == 'intInput':
            obj = intInput.decode(data)

        if obj is not None:
            inputs.append(data)

    return inputs


def getForm(parent, script, profile=None):

    form = QtWidgets.QFormLayout(parent)
    form.addRow('Name', QtWidgets.QLabel('Value'))

    for input in script.inputs:
        form.addRow(input.name, input.getWidget())

    return form



class inputsTableModel(QAbstractItemModel):

    def __init__(self, *args, script=None, **kwargs):
        QAbstractItemModel.__init__(self, *args, **kwargs)
        self._script = None
        self._data = []
        self.loadData(script)


    def clear(self):
        self.beginRemoveRows(QModelIndex(), 0, len(self._data))
        self._data = []
        self.endRemoveRows()


    def loadData(self, script):
        self.clear()

        self._script = script
        self._data = script.inputs

        self.beginInsertRows(QModelIndex(), 0, len(self._data))
        self.endInsertRows()
        self.dataChanged.emit(self.index(0,0), self.index(len(self._data)-1, 2))


    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable


    def rowCount(self, index):
        return len(self._data)


    def columnCount(self, index):
        return 3


    def index(self, row, column, parent=QModelIndex()):
        if row >= 0 and row < len(self._data):
            input = self._data[row]
            return QAbstractItemModel.createIndex(self, row, column, input)
        else:
            return QModelIndex()


    def parent(self, child):
        return QModelIndex()


    def data(self, index, role):
        if not index.isValid():
            return None

        input = self._data[index.row()]

        if role == Qt.DisplayRole:
            if index.column() == 0:
                return input.name
            elif index.column() == 1:
                return input.type
            elif index.column() == 2:
                return input.helpText


    def setData(self, index, value, role=Qt.EditRole):
        input = self._data[index.row()]
        if role == Qt.EditRole:
            if index.column() == 0:
                input.name = value
            elif index.column() == 1:
                input.type = value
            elif index.column() == 2:
                input.helpText = value
            self.dataChanged.emit(index, index)
            return True
        return False


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                if section == 0:
                    return 'Name'
                elif section == 1:
                    return 'Default'
                elif section == 2:
                    return 'Help Text'

        return QAbstractItemModel.headerData(self, section, orientation, role)


    def insertInput(self, row=-1, input=None):
        if input is None:
            input = inputObject()

        if row < 0:
            row = len(self._data)

        self.beginInsertRows(QModelIndex(), row, row)
        self._data.insert(row, input)
        self.endInsertRows()

        return row


    def removeInput(self, input):
        row = self._data.index(input)
        self.beginRemoveRows(QModelIndex(), row, row)
        self._data.remove(input)
        self.endRemoveRows()



class inputTableDelagate(QItemDelegate):

    def createEditor(self, parent, option, index):
        # input = index.internalPointer()

        if index.column() == 0:
            w = QtWidgets.QLineEdit(parent)
        elif index.column() == 1:
            w = QtWidgets.QComboBox(parent)
            w.addItems(['string','int','float','enum'])
        elif index.column() == 2:
            w = QtWidgets.QLineEdit(parent)

        return w


    def setEditorData(self, editor, index):
        input = index.internalPointer()
        if index.column() == 0:
            editor.setText(input.name)
        elif index.column() == 1:
            editor.setCurrentText(input.type)
        elif index.column() == 2:
            editor.setText(input.helpText)


    def setModelData(self, editor, model, index):
        if index.column() == 0:
            model.setData(index, editor.text())
        elif index.column() == 1:
            model.setData(index, editor.currentText())
        elif index.column() == 2:
            model.setData(index, editor.text())
