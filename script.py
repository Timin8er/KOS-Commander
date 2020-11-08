class scriptObject():

    def __init__(self):
        self.name = None
        self.folder = None
        self.inputs = []
        self.profiles = []
        self.text = ''
        self.onboard = False
        self.isCommand = False
        self.description = ''

    def encode(self):
        return {
            "name":self.name,
            "folder":self.folder,
            "inputs":[i.encode() for i in self.inputs],
            "profiles":[i.encode() for i in self.profiles],
            "text":self.text,
            "isCommand":self.isCommand,
            "description":self.description
        }

    @classmethod
    def decode(cls, data):
        obj = cls()
        obj.name = data.get('name', 'unnamed')
        obj.folder = data.get('folder', '')
        obj.inputs = [inputObject.decode(d) for d in data['inputs']]
        obj.profiles = [profileObject.decode(i) for i in data['profiles']]
        obj.text = data.get('text', '')
        obj.description = data.get('description', '')
        obj.isCommand = data.get('isCommand', False)
        return obj



class profileObject():

    def __init__(self):
        self.values = {}
        self.name = 'unnamed'


    def encode(self):
        return {
            'name':self.name,
            'values':self.values
        }

    @classmethod
    def decode(cls, data):
        obj = cls()
        obj.name = data.get('name', 'unnamed')
        obj.values = data.get('values', {})
        return obj



class inputObject():
    def __init__(self):
        self.name = 'unnamed'
        self.defaultValue = None
        self.helpText = ''
        self.type = 'string'

    def encode(self):
        return {
            "name":self.name,
            "cls":self.__class__.__name__,
            "defaultValue":self.defaultValue,
            "helpText":self.helpText,
            "type":self.type
        }

    @classmethod
    def decode(cls, data):
        obj = cls()
        obj.name = data['name']
        obj.helpText = data.get('helpText','')
        obj.defaultValue = data.get('defaultValue', None)
        obj.type = data.get('type', 'string')
        return obj


    def getValueWidget(self):
        return None


    def getEditWidget(self):
        pass
