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


# sc = kos_connection('127.0.0.1', '5410', 10)

# sc.ks_run('init', volume=0)
#
# for i in reversed(range(5)):
#     sleep(1)
#     print(i)
#
# sc.ks_run('launch', timeout=0)
# sleep(10)
# sc.ks_stop()
#
# sc.close()
# print('done')
