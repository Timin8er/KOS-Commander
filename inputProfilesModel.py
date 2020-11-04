from PyQt5.QtCore import QAbstractItemModel, Qt, QModelIndex
import os
from PyQt5.QtWidgets import QDialog

class profileObject():

    def __init__(self):
        self.values = {}
        self.name = 'unnamed'



class inputsListModel(QAbstractItemModel):

    scripts_file = os.path.join(os.path.dirname(__file__), 'scripts.json')

    def __init__(self, *args, **kwargs):
        QAbstractItemModel.__init__(self, *args, **kwargs)

        self._data = []
        self._script = None
        self.loadData()


    def clear(self):
        self.beginRemoveRows(QModelIndex(), 0, len(self._data))
        self._data = []
        self.endRemoveRows()


    def loadData(self, script=None):
        self.clear()

        if script:
            self._script = script

        if self._script:
            self._script.profiles.sort(key = lambda x: x.name)
            self._data = script.profiles
        else:
            self._data = []

        self.beginInsertRows(QModelIndex(), 0, len(self._data))
        self.endInsertRows()


    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable


    def rowCount(self, index):
        return len(self._data)


    def columnCount(self, index):
        return 1


    def data(self, index, role):
        if not index.isValid():
            return None

        profile = SELF._data(index.row())

        if role == Qt.DisplayRole:
            if index.column() == 0:
                return profile.name


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                if section == 0:
                    return 'Profile'

        return QAbstractItemModel.headerData(self, section, orientation, role)


    def insertProfile(self, row, profile):
        if row < 0:
            self._data.append(profile)
        else:
            self._data.insert(row, profile)
        self.loadData(self._data)


    def removeProfile(self, profile):
        self._data.remove(profile)
        self.loadData(self._data)
