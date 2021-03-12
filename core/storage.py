from KOSCommander import settings
import json
from . import scriptObject

def save(script_bjects):
    data = [i.encode() for i in script_bjects]
    with open(settings.SCRIPT_FILE, 'w') as sf:
        json.dump(sf, data, sort_keys=True, indent=4)


def load():
    with open(settings.SCRIPT_FILE) as sf:
        data = json.load(sf)
        data = [scriptObject.decode(i) for i in data]
        return data
