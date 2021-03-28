from time import sleep, time
import telnetlib
from KOSCommander import settings
import os

class kosConnection():

    def __init__(self):

        self._connection = None
        self._time_deadline = 0


    def open(self):
        self._connection = telnetlib.Telnet(settings.HOST, settings.PORT, settings.TIMEOUT)

        self._connection.read_eager()
        self._connection.write(b'1\n')
        sleep(.2)
        self._connection.write(b'1\n')
        sleep(.2)
        self._connection.read_until(b'')


    def kosCommand(self, command_str):
        """ execute a single kos command """
        if self._time_deadline < time():
            self.open()

        self._time_deadline = time() + 15
        self._connection.write(f'{command_str}\n'.encode())
        print(command_str)
        self._connection.read_until(b'')
        sleep(.2)


    def kosStop(self):
        """ hault the kos terminal """
        if self._time_deadline < time():
            self.open()
        _ = self._connection.write(telnetlib.IP)


    def kosRunScript(self, script_instance, *args, volume=1, timeout=0):
        """  """
        args = [f'{volume}:/{script_instance.name}.ks'] + [str(i) for i in list(args)]
        com = '", "'.join(args)
        command_str = f'runpath("{com}").\n'
        self.kosCommand(command_str)

        if timeout:
            sleep(timeout)
            self.ks_stop()


    def kosUpload(self, script_instance):
        """ upload the given script object to the kos ship """

        # write script to temp file
        temp_file = os.path.join(settings.GAME_INSTANCE, 'Ships', 'Script', 'temp_upload.ks')

        with open(temp_file, 'w') as f:
            f.write(script_instance.text)

        # upload the file
        self.kosCommand(f'COPYPATH("1:/temp_upload.ks", "0:/{script_instance.name}.ks").')
