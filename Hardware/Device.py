# Base class for devices
class Device:
    import pyvisa
    rm = pyvisa.ResourceManager()

    def __init__(self, addr, name=None, isVISA=True):
        self.addr = addr
        self.devicename = name
        self.isVISA = isVISA
        self.connected = False
        if isVISA:
            try:
                self.inst = self.rm.open_resource(addr)
            except:  # TODO： raise warning (or error?) here to help identify visa object create failure.
                pass

    def connect(self):
        if not self.connected:
            try:
                if self.isVISA:
                    self.inst.open()
                self.connected = True
                print(self.devicename + " connected")
                return 1
            except:
                import sys
                e = sys.exc_info()[0]
                print(f"Error:{e}")
                return -1
        return 0

    def disconnect(self):
        if self.connected:
            if self.isVISA:
                self.inst.close()
            self.connected = False
            print(self.devicename + " disconnected")
            return 1
        return 0

    def write(self, cmd):
        self.inst.write(cmd)

    def read(self):
        return self.inst.read()

    def query(self, cmd):
        return self.inst.query(cmd)
