
from .Device import Device


class EatonPDU(Device):
    def __init__(self, addr='ASRL23::INSTR', name="Eaton PDU epduDC	192.168.0.160", isVISA=True):
        '''Eaton PDU epduDC'''
        super().__init__(addr=addr, name=name, isVISA=isVISA)
        self.inst.baud_rate = 9600
        # self.inst.read_termination = '\r\n'  # read_termination is not specified by default.
        self.inst.write_termination = '\r\n'  # write_termination is '\r\n' by default.

        self.__username = "kecklfc" # default password is "admin"
        self.__password = "astrocomb" # default password is its serial number # 192.168.0.160
        # self.__password = "H619N29036" # 192.168.0.143
        self.max_login_attempt = 2
        self.loggedin = False

    def test_loggedin(self):
        '''Test if the device is logged in. Return True if logged in, False if not.'''
        try:
            self.write("")
            tt = self.inst.read(termination='>')
            return ('pdu' in tt)
        except:
            return False

    def connect(self, login=True):
        cnt = super().connect()
        if login:
            lgin = self.login()
        return cnt, lgin

    def disconnect(self, logout=True):
        dcnt = super().disconnect()
        if logout:
            lgot = self.logout()
        return dcnt, lgot

    def login(self): # login to the device
        '''Login to the device. Return 1 if succeed, -1 if failed.'''
        if not self.connected:
            raise ConnectionError(self.devicename+": Should connect to device before Login.")
        self.loggedin = self.test_loggedin()
        if self.loggedin:
            print(self.devicename + ": Already logged in.")
            return 0
        fail_count = 0
        while fail_count<self.max_login_attempt:
            try:
                self.inst.clear()
                self.write("")
                print(self.inst.read(termination='in:'))
                self.write(self.__username)
                print(self.inst.read(termination='word:'))
                self.write(self.__password)
                tt = self.inst.read(termination='>')
                print(tt)
                if 'pdu' in tt:
                    print(self.devicename + ": Login succeed.")
                    self.loggedin = True
                    return 1
                else:
                    fail_count += 1
                    print(self.devicename + 
                          f": Login failed. You have {self.max_login_attempt - fail_count} attempts left.")
            except:
                fail_count += 1
                print(self.devicename + 
                      f": Login failed. You have {self.max_login_attempt - fail_count} attempts left.")
        
        print(self.devicename + ": Login Failed.")
        return -1

    def logout(self):
        if not self.loggedin:
            return 0
        self.write("quit")
        self.loggedin = False
        print(self.devicename + ": Logged out.")

    # Active Power Measurement
    def get_active_power(self, outlet=1):
        self.write(f"get PDU.OutletSystem.Outlet[{outlet}].ActivePower")
        return float(self.inst.read(termination='pdu#0>'))
    # current measurement
    def get_current(self, outlet=1):
        self.write(f"get PDU.OutletSystem.Outlet[{outlet}].Current")
        return float(self.inst.read(termination='pdu#0>'))

    # voltage measurement
    def get_voltage(self, outlet=1):
        self.write(f"get PDU.OutletSystem.Outlet[{outlet}].Voltage")
        return float(self.inst.read(termination='pdu#0>'))

    # power factor measurement
    def get_power_factor(self, outlet=1):
        self.write(f"get PDU.OutletSystem.Outlet[{outlet}].PowerFactor")
        return float(self.inst.read(termination='pdu#0>'))


if __name__=="__main__":
    eaton = EatonPDU()
    eaton.connect()
    eaton.write("get PDU.OutletSystem.Outlet.Count")
    print(eaton.inst.read(termination='pdu#0>'))
    eaton.write("set PDU.OutletSystem.Outlet[8].DelayBeforeShutdown 0")
    print(eaton.inst.read(termination='pdu#0>'))
    import time
    time.sleep(5)
    eaton.write("set PDU.OutletSystem.Outlet[8].DelayBeforeStartup 0")
    print(eaton.inst.read(termination='pdu#0>'))
    print(eaton.get_active_power(6))

    # ========== Below are already wrapped functions ==========
    # # eaton.login()
    # eaton.inst.clear()
    # # eaton.write("admin")
    # # eaton.write("H619N29040")
    # eaton.write("")
    # print(eaton.inst.read(termination='in:'))
    # eaton.write("kecklfc")
    # print(eaton.inst.read(termination='word:'))
    # eaton.write("astrocomb")
    # tt = eaton.inst.read(termination='>')
    # print(tt)
    # print('pdu' in tt)
    # eaton.write("get PDU.OutletSystem.Outlet.Count")
    # print(eaton.inst.read(termination='pdu#0>'))
    # eaton.write("quit")
    # # print(eaton.inst.read())
    # # import time
    # # for ii in range(1):
    # #     print(ii)
    # #     eaton.write("")
    # #     # eaton.write("admin")
    # #     # eaton.write("H619N29040")
    # #     print(eaton.inst.read(termination='in:'))

    # #     # eaton.inst.clear()
    # #     time.sleep(0.1)
