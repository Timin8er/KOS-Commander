from PyQt5.QtCore import QAbstractItemModel, Qt, QModelIndex
from PyQt5.QtWidgets import QDialog
from KOSCommander.core import profileObject

class profilesListModel(QAbstractItemModel):

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

        if script is not None:
            self._script = script
            self._script.profiles.sort(key = lambda x: x.name)
            self._data = self._script.profiles
        else:
            self._script = None
            self._data = []

        self.beginInsertRows(QModelIndex(), 0, len(self._data))
        self.endInsertRows()


    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable


    def rowCount(self, index):
        return len(self._data)


    def columnCount(self, index):
        return 1


    def index(self, row, column, parent=QModelIndex()):
        if row < len(self._data):
            profile = self._data[row]
            return QAbstractItemModel.createIndex(self, row, column, profile)
        else:
            return QModelIndex()


    def parent(self, child):
        return QModelIndex()


    def data(self, index, role):
        if not index.isValid():
            return None

        profile = self._data[index.row()]

        if role == Qt.DisplayRole:
            if index.column() == 0:
                return profile.name


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                if section == 0:
                    return 'Profile'

        return QAbstractItemModel.headerData(self, section, orientation, role)


    def insertProfile(self, row=-1, profile=None):
        if profile is None:
            profile = profileObject()

        if row < 0:
            row = len(self._data)
            self._data.append(profile)
        else:
            self._data.insert(row, profile)
        self.loadData(self._script)
        return row


    def removeProfile(self, profile):
        self._data.remove(profile)
        self.loadData(self._script)
