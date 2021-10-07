from utilities.touch.ScreenReader import ScreenReader
from ppadb.client import Client
class Interactor:

    class Display:
        def __init__(self, phys_size_str):
            self.width, self.height = [int(dimension) for dimension in phys_size_str.split()[-1].split("x")]
            self.middle = (self.width//2, self.height//2)

    def __init__(self, host, port , serial=None):
        client=Client(host, port)
         
        if len(client.devices()) == 0:
            raise IOError("No device connected")

        self.dev = client.devices()[0] if serial is None else client.device(serial)
        self.display = self.Display(self.dev.shell("wm size"))
        self.interactor = ScreenReader(self.dev)

