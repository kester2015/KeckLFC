from Device import Device
import time


class KeysightFG_33500(Device):

    def __init__(
        self,
        addr="USB0::0x0957::0x2807::MY59003824::INSTR",
        name="Keysight Function Generator 33500 Series",
        isVISA=True,
    ):
        super().__init__(addr=addr, name=name, isVISA=isVISA)

    @property
    def IDN(self):
        return self.query("*IDN?")
    
if __name__ == "__main__":
    fg = KeysightFG_33500()
    fg.connect()
    print(fg.IDN)
    fg.disconnect()