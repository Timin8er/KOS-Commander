from PyQt5.QtCore import QAbstractItemModel, Qt, QModelIndex
from PyQt5.QtGui import QIcon
import os
import json
from . import icons

class scriptObject():

    def __init__(self):
        self.name = None
        self.folder = None
        self.inputs = []
        self.profiles = []
        self.text = ''
        self.onboard = False
        self.isCommand = False

    def encode(self):
        return {
            "name":self.name,
            "folder":self.folder,
            "inputs":[i.encode() for i in self.inputs],
            "profiles":[i.encode() for i in self.inputs],
            "text":self.text,
            "isCommand":self.isCommand
        }

    @classmethod
    def decode(cls, data):
        obj = cls()
        obj.name = data.get('name', 'unnamed')
        obj.folder = data.get('folder', '')
        obj.inputs = [scriptInput.decode(i) for i in data['inputs']]
        obj.profiles = [scriptProfile.decode(i) for i in data['profiles']]
        obj.text = data.get('text', '')
        obj.isCommand = data.get('isCommand', False)
        return obj


class scriptInput():

    def __init__(self):
        self.name = 'unnamed'
        self.value = None
        self.limits = {}
        self.helpText = ''


    def encode(self):
        return {
            "name":self.name,
            "cls":self.__class__.__name__,
            "value":self.value,
            "limits":self.limits,
            "helpText":self.helpText
        }

    @property
    def decode(cls, data):
        obj = cls()
        obj.name = data['name']
        obj.value = data['value']
        obj.limits = data['limits']
        obj.helpText = data.get('helpText','')
        return obj


class scriptProfile():

    def __init__(self):
        self.name = None
        self.values = []

    def encode(self):
        return {
            "name":self.name,
            "values":self.values
        }

    @property
    def decode(cls, data):
        obj = cls()
        obj.name = data['name']
        obj.values = data['values']
        return obj


class folderItem():

    def __init__(self, path):
        self.name = os.path.basename(path)
        self.dirname = os.path.dirname(path)
        self.path = path


class scriptTreeNode():
    def __init__(self, data):
        self._data = data
        self._children = []
        self._parent = None
        self._row = 0

    def childCount(self):
        return len(self._children)

    def child(self, row):
        if row >= 0 and row < self.childCount():
            return self._children[row]

    def parent(self):
        return self._parent

    def row(self):
        return self._row

    def addChild(self, child):
        if not isinstance(child, scriptTreeNode):
            child = scriptTreeNode(child)

        child._parent = self
        child._row = len(self._children)
        self._children.append(child)


class scriptsTreeModel(QAbstractItemModel):

    scripts_file = os.path.join(os.path.dirname(__file__), 'scripts.json')

    def __init__(self, *args, **kwargs):
        QAbstractItemModel.__init__(self, *args, **kwargs)

        self._root = scriptTreeNode(None)

        self._data = []

        self.refresh()


    def clear(self):
        self.beginRemoveRows(QModelIndex(), 0, self._root.childCount())
        self._root._children = []
        self.endRemoveRows()


    def refresh(self, data=None):
        self.clear()

        if data is None:
            with open(self.scripts_file) as sf:
                data = json.load(sf)
            data = [scriptObject.decode(i) for i in data]
            self._data = data

        data.sort(key = lambda x: x.name)

        # build folders
        structure = {}
        for d in data:
            self.recursive_add_folder(structure, d.folder)

        # link folders
        for key, node in structure.items():
            if node._data.dirname:
                parent = structure[node._data.dirname]
                parent.addChild(node)
            else:
                self._root.addChild(node)

        # add scripts
        for d in data:
            if d.folder in structure:
                structure[d.folder].addChild(d)
            else:
                self._root.addChild(d)

        self.beginInsertRows(QModelIndex(), 0, self._root.childCount())
        self.endInsertRows()


    def save(self):
        data = [i.encode() for i in self._data]
        with open(self.scripts_file, 'w') as sf:
            sf.write(json.dumps(data))

    def recursive_add_folder(self, structure, path):
        if not path:
            return
        if path not in structure:
            structure[path] = scriptTreeNode(folderItem(path))
        path = os.path.dirname(path)
        if path:
            self.recursive_add_folder(structure, path)


    def index(self, row, column, _parent):
        if not _parent or not _parent.isValid():
            parent = self._root
        else:
            parent = _parent.internalPointer()

        if not QAbstractItemModel.hasIndex(self, row, column, _parent):
            return QModelIndex()

        child = parent.child(row)
        if child:
            return QAbstractItemModel.createIndex(self, row, column, child)
        else:
            return QModelIndex()


    def flags(self, index):
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable


    def parent(self, index):
        if index.isValid():
            p = index.internalPointer().parent()
            if p:
                return QAbstractItemModel.createIndex(self, p.row(), 0, p)
        return QModelIndex()


    def rowCount(self, index):
        if index.isValid():
            return index.internalPointer().childCount()
        return self._root.childCount()


    def columnCount(self, index):
        return 2


    def data(self, index, role):
        if not index.isValid():
            return None

        script = index.internalPointer()._data

        if role == Qt.DisplayRole:
            if index.column() == 0:
                return script.name

        if role == Qt.DecorationRole:
            if index.column() == 0:
                if isinstance(script, scriptObject):
                    if script.isCommand:
                        return QIcon(icons.COMMAND)
                    else:
                        return QIcon(icons.CODE)
                else:
                    return QIcon(icons.FOLDER)

            elif index.column() == 1 and isinstance(script, scriptObject):
                return QIcon(icons.CHECKED_CHECKBOX) if script.onboard else QIcon(icons.UNCHECKED_CHECKBOX)


    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                if section == 0:
                    return 'Name'
                elif section == 1:
                    return 'Onboard'

        return QAbstractItemModel.headerData(self, section, orientation, role)


    def insertScript(self, script):
        self._data.append(script)
        self.refresh(self._data)


    def removeScript(self, script):
        self._data.remove(script)
        self.refresh(self._data)
