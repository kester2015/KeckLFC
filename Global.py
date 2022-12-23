import json
import datetime
from enum import Enum


class LFCStatus:
    debug = True

    def __init__(self):
        self.Warning = False
        self.WarningMsg = ""
        self.OSA_X = list(range(0, 100))
        self.OSA_Y = list(range(0, 100))
        self.RbLocked = False

    def intensityLocked(self):
        return abs(self.intenSet - self.intenActual) < 0.1

    def toJSON(self):
        out = {
            'timestamp': f"{datetime.datetime.now()}",
            'version': "20211119",
            'warning': self.Warning,
            'errmsg': self.WarningMsg,
            'Rblocked': self.RbLocked
        }
        return json.dumps(out)


class DeviceInfo(Enum):
    Waveshaper = 'SN201904'
    FPGA1 = 'rp-f072a9.local'
    FPGA2 = 'rp-f072ec.local'
    RbClock = 'ASRL3::INSTR'
    PendulumCNT90 = 'GPIB0::10::INSTR'
