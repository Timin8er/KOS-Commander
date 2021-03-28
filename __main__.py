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


# telnet program example
# import socket, select, sys
# from . import settings
#
# #main function
# if __name__ == "__main__":
#
# 	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 	s.settimeout(2)
#
# 	# connect to remote host
# 	try :
# 		s.connect((settings.HOST, settings.PORT))
# 	except :
# 		print('Unable to connect')
# 		sys.exit()
#
# 	print('Connected to remote host')
#
# 	while 1:
# 		socket_list = [sys.stdin, s]
#
# 		# Get the list sockets which are readable
# 		read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])
#
# 		for sock in read_sockets:
# 			#incoming message from remote server
# 			if sock == s:
# 				data = sock.recv(4096)
# 				if not data :
# 					print('Connection closed')
# 					sys.exit()
# 				else :
# 					#print data
# 					sys.stdout.write(data)
#
# 			#user entered a message
# 			else :
# 				msg = sys.stdin.readline()
# 				s.send(msg)
