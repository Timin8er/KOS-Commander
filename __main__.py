import telnetlib
from time import sleep
from . import kos_connection
from PyQt5.QtWidgets import QApplication
from .ui import mainWindow
import sys

app = QApplication([])

# ['windowsvista', 'Windows', 'Fusion']
app.setStyle('Fusion')

mw = mainWindow()
mw.show()
sys.exit(app.exec_())
