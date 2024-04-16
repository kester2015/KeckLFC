from ctypes import *


class SC10:
    sc10Lib = None
    isLoad = False

    @staticmethod
    def list_devices():
        """ List all connected mcm301 devices
        Returns:
           The mcm301 device list, each deice item is serialNumber/COM
        """
        str1 = create_string_buffer(10240)
        result = SC10.sc10Lib.List(str1, 10240)
        devicesStr = str1.value.decode("utf-8", "ignore").rstrip('\x00').split(',')
        length = len(devicesStr)
        i = 0
        devices = []
        devInfo = ["", ""]
        while i < length:
            str2 = devicesStr[i]
            if i % 2 == 0:
                if str2 != '':
                    devInfo[0] = str2
                else:
                    i += 1
            else:
                devInfo[1] = str2
                devices.append(devInfo.copy())
            i += 1
        return devices

    @staticmethod
    def load_library(path):
        SC10.sc10Lib = cdll.LoadLibrary(path)
        SC10.isLoad = True

    def __init__(self):
        lib_path = "./SC10CommandLib_win32.dll"
        if not SC10.isLoad:
            SC10.load_library(lib_path)
        self.hdl = -1

    def open(self, serialNo, nBaud, timeout):
        """ Open SC10 device
        Args:
            serialNo: serial number of SC10 device
            nBaud: the bit per second of port
            timeout: set timeout value in (s)
        Returns: 
            non-negative number: hdl number returned Successful; negative number: failed.
        """
        ret = -1
        if SC10.isLoad:
            ret = SC10.sc10Lib.Open(serialNo.encode('utf-8'), nBaud, timeout)
            if ret >= 0:
                self.hdl = ret
            else:
                self.hdl = -1
        return ret

    def is_open(self, serialNo):
        """ Check opened status of SC10 device
        Args:
            serialNo: serial number of SC10 device
        Returns: 
            0: SC10 device is not opened; 1: SC10 device is opened.
        """
        ret = -1
        if SC10.isLoad:
            ret = SC10.sc10Lib.IsOpen(serialNo.encode('utf-8'))
        return ret

    def close(self):
        """ Close opened SC10 device
        Returns: 
            0: Success; negative number: failed.
        """
        ret = -1
        if self.hdl >= 0:
            ret = SC10.sc10Lib.Close(self.hdl)
        return ret

    def set_baud_rate(self, baud_rate):
        """ set SC10's serial baud rate
        Args:
            baud_rate: SC10 baud rate, 0 for 9.6k and 1 for 115k
        Returns:
            0: Success; negative number: failed.
        """
        ret = -1
        if self.hdl >= 0:
            baud_rate_val = c_int(baud_rate)
            ret = SC10.sc10Lib.SetBaudRate(self.hdl, baud_rate_val)
        return ret

    def set_mode(self, mode):
        """ Set operating mode
        Args:
            mode: SC10 mode. 1-manual, 2-auto, 3-single, 4-repeat, 5-external gate
        Returns:
            0: Success; negative number: failed.
        """
        ret = -1
        if self.hdl >= 0:
            mode_val = c_int(mode)
            ret = SC10.sc10Lib.SetMode(self.hdl, mode_val)
        return ret

    def toggle_enable(self):
        """ Enable/Disable the shutter
        Args:
        Returns:
            0: Success; negative number: failed.
        """
        ret = -1
        if self.hdl >= 0:
            ret = SC10.sc10Lib.ToggleEnable(self.hdl)
        return ret

    def set_open_time(self, time):
        """ set open duration
        Args:
            time: shutter's open time in ms
        Returns:
            0: Success; negative number: failed.
        """
        ret = -1
        if self.hdl >= 0:
            time_val = c_int(time)
            ret = SC10.sc10Lib.SetOpenTime(self.hdl, time_val)
        return ret

    def set_close_time(self, time):
        """ set close duration
        Args:
            time: shutter's close time in ms
        Returns:
            0: Success; negative number: failed.
        """
        ret = -1
        if self.hdl >= 0:
            time_val = c_int(time)
            ret = SC10.sc10Lib.SetCloseTime(self.hdl, time_val)
        return ret

    def set_trigger_mode(self, mode):
        """ set the trigger mode
        Args:
            mode: 0:internal trigger mode,1:external trigger mode
        Returns:
            0: Success; negative number: failed.
        """
        ret = -1
        if self.hdl >= 0:
            mode_val = c_int(mode)
            ret = SC10.sc10Lib.SetTriggerMode(self.hdl, mode_val)
        return ret

    def set_external_trigger_mode(self, mode):
        """ Set Ex Trigger mode
        Args:
            mode: 0:set the output trigger to follow the shutter output when the SH05 is connected,
                   1: force the trigger output to follow the controller output when an SH05 is equipped
        Returns:
            0: Success; negative number: failed.
        """
        ret = -1
        if self.hdl >= 0:
            mode_val = c_int(mode)
            ret = SC10.sc10Lib.SetExternalTriggerMode(self.hdl, mode_val)
        return ret

    def set_repeat_count(self, repeat_count):
        """ Set repeat count
        Args:
            repeat_count: set the repeat count when in repeat mode, a value of 1-99
        Returns:
            0: Success; negative number: failed.
        """
        ret = -1
        if self.hdl >= 0:
            repeat_count_val = c_int(repeat_count)
            ret = SC10.sc10Lib.SetRepeatCount(self.hdl, repeat_count_val)
        return ret

    def get_baud_rate(self, baud_rate):
        """  Get baud rate
        Args:
            baud_rate: 0: 9.6k, 1:115k
        Returns:
            0: Success; negative number: failed.
        """
        ret = -1
        if self.hdl >= 0:
            baud_rate_val = c_int(0)
            ret = SC10.sc10Lib.GetBaudRate(self.hdl, byref(baud_rate_val))
            baud_rate[0] = baud_rate_val.value
        return ret

    def get_mode(self, mode):
        """  Get operating mode
        Args:
            mode: the mode value(1-5)
        Returns:
            0: Success; negative number: failed.
        """
        ret = -1
        if self.hdl >= 0:
            mode_val = c_int(0)
            ret = SC10.sc10Lib.GetMode(self.hdl, byref(mode_val))
            mode[0] = mode_val.value
        return ret

    def get_enable_state(self, enable_state):
        """  Get State
        Args:
            enable_state: 0: the shutter is disabled, 1: enabled
        Returns:
            0: Success; negative number: failed.
        """
        ret = -1
        if self.hdl >= 0:
            enable_state_val = c_int(0)
            ret = SC10.sc10Lib.GetEnableState(self.hdl, byref(enable_state_val))
            enable_state[0] = enable_state_val.value
        return ret

    def get_open_time(self, time):
        """  Get open duration
        Args:
            time: the shutter's open time in ms
        Returns:
            0: Success; negative number: failed.
        """
        ret = -1
        if self.hdl >= 0:
            time_val = c_int(0)
            ret = SC10.sc10Lib.GetOpenTime(self.hdl, byref(time_val))
            time[0] = time_val.value
        return ret

    def get_close_time(self, time):
        """  Get close duration
        Args:
            time: the shutter's close time in ms
        Returns:
            0: Success; negative number: failed.
        """
        ret = -1
        if self.hdl >= 0:
            time_val = c_int(0)
            ret = SC10.sc10Lib.GetCloseTime(self.hdl, byref(time_val))
            time[0] = time_val.value
        return ret

    def get_trigger_mode(self, mode):
        """  Get trigger mode
        Args:
            mode: 0:internal trigger mode,1:external trigger mode
        Returns:
            0: Success; negative number: failed.
        """
        ret = -1
        if self.hdl >= 0:
            mode_val = c_int(0)
            ret = SC10.sc10Lib.GetTriggerMode(self.hdl, byref(mode_val))
            mode[0] = mode_val.value
        return ret

    def get_external_trigger_mode(self, mode):
        """  Get Ex trigger mode
        Args:
            mode: external trigger mode
        Returns:
            0: Success; negative number: failed.
        """
        ret = -1
        if self.hdl >= 0:
            mode_val = c_int(0)
            ret = SC10.sc10Lib.GetExternalTriggerMode(self.hdl, byref(mode_val))
            mode[0] = mode_val.value
        return ret

    def get_repeat_count(self, repeat_count):
        """  GReturn the repeat count
        Args:
            repeat_count: repeat count, a value of 1-99
        Returns:
            0: Success; negative number: failed.
        """
        ret = -1
        if self.hdl >= 0:
            repeat_count_val = c_int(0)
            ret = SC10.sc10Lib.GetRepeatCount(self.hdl, byref(repeat_count_val))
            repeat_count[0] = repeat_count_val.value
        return ret

    def get_closed_state(self, state):
        """  Get closed state
        Args:
            state: 1: shutter is closed, 0: shutter is open
        Returns:
            0: Success; negative number: failed.
        """
        ret = -1
        if self.hdl >= 0:
            state_val = c_int(0)
            ret = SC10.sc10Lib.GetClosedState(self.hdl, byref(state_val))
            state[0] = state_val.value
        return ret

    def get_interlock_tripped(self, tripped_state):
        """  Get interlock tripped
        Args:
            tripped_state: 1: interlock is tripped, otherwise 0
        Returns:
            0: Success; negative number: failed.
        """
        ret = -1
        if self.hdl >= 0:
            tripped_state_val = c_int(0)
            ret = SC10.sc10Lib.GetInterlockTripped(self.hdl, byref(tripped_state_val))
            tripped_state[0] = tripped_state_val.value
        return ret

    def get_id(self, id):
        """  get the SC10 id
        Args:
            id: output string (255)
        Returns:
            0: Success; negative number: failed.
        """
        ret = -1
        if self.hdl >= 0:
            id_val = create_string_buffer(255)
            ret = SC10.sc10Lib.GetId(self.hdl, id_val)
            id[0] = id_val.value.decode("utf-8", "ignore").rstrip('\x00').replace("\r\n", "")
        return ret

    def save_settings(self):
        """  Save current baud rate and output trigger mode
        Args:
        Returns:
            0: Success; negative number: failed.
        """
        ret = -1
        if self.hdl >= 0:
            ret = SC10.sc10Lib.SaveSettings(self.hdl)
        return ret

    def store_configuration(self):
        """  Store configuration, save current settings(ex. mode, open time, close time) into EEPROM
        Args:
        Returns:
            0: Success; negative number: failed.
        """
        ret = -1
        if self.hdl >= 0:
            ret = SC10.sc10Lib.StoreConfiguration(self.hdl)
        return ret

    def load_configuration(self):
        """  Load configuration from EEPROM
        Args:
        Returns:
            0: Success; negative number: failed.
        """
        ret = -1
        if self.hdl >= 0:
            ret = SC10.sc10Lib.LoadConfiguration(self.hdl)
        return ret



