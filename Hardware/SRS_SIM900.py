import warnings
import time

from .Device import Device
import numpy as np
import matplotlib.pyplot as plt
import numbers
import os
from decimal import Decimal

''' Author: Maodong Gao, version 0.0, Aug 18 2022 '''
''' PLEASE FOLLOW camelCase Convention to maintain '''


class SRS_SIM900(Device):

    def __init__(self, addr='ASRL21::INSTR', name="Stanford Research System SIM900"):
        super().__init__(addr=addr, name=name)

        self.__activation_timeout = 3  # time to wait for device to turn on/off activation and channel status. in unit of second.
        self.inst.timeout = 25000  # communication time-out time set in units of ms
        self.inst.baud_rate = 9600  # baud rate is 9600 by default. THIS SETTING IS NECESSARY for success communication
        self.inst.read_termination = '\r\n'  # read_termination is not specified by default.
        self.inst.write_termination = '\r\n'  # write_termination is '\r\n' by default.

        self.__escstr = 'xyx'
        self.prepend = ''
        self.escstr = self.__escstr
        self.active_module = None

    def printStatus(self):

        def highlight_status(status_string):
            """Color refer https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal"""
            if status_string in ['UNLOCKED', 'ON']:  # Show a green color
                return "\x1b[1;34;42m" + status_string + "\x1b[0m"
            elif status_string in ['LOCKED', 'OFF']:  # Show a red color
                return "\x1b[1;34;41m" + status_string + "\x1b[0m"
            else:
                return status_string

        message = str(self.devicename).center(81, '-') + "\n"
        message = message + "Stanford Research System SIM900 Status Summary".center(80, '-') + "\n"

        message = message + "Stanford Research System SIM900 Status Summary Ends".center(80, '-') + "\n"
        print(message)
        return message

    def clear(self):
        self.inst.clear()
        # self.inst.write('*CLS')
        # self.prepend = ''
        # self.escstr = self.__escstr
        self.active_module = None

    def query_slot(self, slot, query, clear=True):
        self.switch_to(slot, clear=clear)
        try:
            return self.inst.query(query)
        except VisaIOError:
            time.sleep(1)
            return self.inst.query(query)

    def write_slot(self, slot, text, clear=True):
        self.switch_to(slot, clear=clear)
        try:
            self.inst.write(text)
        except VisaIOError:
            time.sleep(1)
            self.inst.write(text)

    def read_slot(self, slot, clear=True):
        self.switch_to(slot, clear=clear)
        try:
            return self.inst.read()
        except VisaIOError:
            time.sleep(1)
            return self.inst.read()

    def switch_to(self, slot, clear=True):
        # Modified by Maodong: Don't check anymore, clear device anyway.
        #if self.active_module != slot:
        if clear:
            self.clear()
            if slot == 0:
                # self.clear()
                # self.active_module = None
                # print(self.devicename+": Active slot switched to None. Mainframe is active.")
                return
            self.inst.write('{}CONN {}, "{}"'.format(self.prepend, slot, self.escstr))
            # Maodong: After modification, prepend here will always be ''
            # self.prepend = self.escstr # Maodong: In pronciple, this is not necessary since will be cleared to '' anyway
            self.active_module = slot
        else:
            if slot == 0:
                self.clear()
                return
            if self.active_module != slot:
                self.inst.write('{}CONN {}, "{}"'.format(self.prepend, slot, self.escstr))
                self.active_module = slot
        # print(self.devicename+": Active slot switched to Num. "+str(slot)+".")


class SRS_PIDcontrol_SIM960(object):

    def __init__(self, mainframe, slot: int, name="SRS PID controller SIM960"):
        # mainframe is an instance of SRS_SIM900
        self.mainframe = mainframe
        self.slot = slot
        self.devicename = name
        self.query_interval = 0.2  # seconds

        self.__prop_gain_max = 1e3  # minP = -maxP, sign stands for polarity
        self.__prop_gain_resolution = 1e-1
        self.__intg_gain_max = 5e5  # in 1/seconds
        self.__intg_gain_min = 1e-2  # in 1/seconds
        self.__intg_gain_resolution = 1e-2  # in 1/seconds
        self.__derv_gain_max = 10  # in seconds
        self.__derv_gain_min = 1e-6  # in seconds
        self.__derv_gain_resolution = 1e-6  # in seconds

        self.__outoffset_max = 10  # in Volt
        self.__outoffset_min = -10  # in Volt
        # self.__outoffset_resolution = 1e-3  # in Volt
        self.__outoffset_resolution = None

        self.__setpoint_max = 10  # in Volt
        self.__setpoint_min = -10  # in Volt
        self.__setpoint_resolution = 1e-3  # in Volt
        # self.__setpoint_resolution = None

        self.__manual_output_max = 10  # in Volt
        self.__manual_output_min = -10  # in Volt
        self.__manual_output_resolution = 1e-3  # in Volt
        # self.__manual_output_resolution = None  # in Volt
        self.manual_output_ramp = 0.0  # Volt

        self.__spramprate_max = 1e4  # in V/s
        self.__spramprate_min = 1e-3  # in V/s
        self.__spramprate_resolution = None

        self.__output_lowerlim_resolution = 1e-2 # in Volt
        self.__output_upperlim_resolution = 1e-2 # in Volt

    def write(self, cmd, clear=True):
        if clear:  # clear=True means robust is important, otherwise speed is important
            time.sleep(self.query_interval)
        self.mainframe.write_slot(self.slot, cmd, clear=clear)

    def query(self, cmd, clear=True):
        if clear:
            time.sleep(self.query_interval)
        return self.mainframe.query_slot(self.slot, cmd, clear=clear)

    def read(self, cmd, clear=True):
        if clear:
            time.sleep(self.query_interval)
        return self.mainframe.read_slot(self.slot, cmd, clear=clear)

    def printStatus(self):

        def highlight_status(status_string):
            """Color refer https://stackoverflow.com/questions/287871/how-to-print-colored-text-to-the-terminal"""
            if status_string in ['UNLOCKED', 'ON', 'PID']:  # Show a green color
                return "\x1b[1;34;42m" + status_string + "\x1b[0m"
            elif status_string in ['LOCKED', 'OFF', 'MAN']:  # Show a red color
                return "\x1b[1;34;41m" + status_string + "\x1b[0m"
            else:
                return status_string

        message = str(self.devicename).center(81, '-') + "\n"
        message = message + "|" + "SRS PID controller SIM960 Status Summary".center(80, '-') + "\n"
        message = message + "|" + ','.join(self.equipment_IDN.split(',')[1:]).center(80, '-') + "\n"
        message = message + "|\t" + "Output mode:\t" + highlight_status(
            self.output_mode) + f",\tOutput limit: {self.output_lowerlim:.3f}V TO {self.output_upperlim:.3f}V\n"
        message = message + "|\t" + f"Measured input:\t {self.measure_input}V" + "\n"
        message = message + "|\t" + f"Amplified error:\t {self.amplified_error}V" + "\n"
        message = message + "|\t" + f"Instant Output voltage:\t {self.output_voltage}V\n"
        message = message + "|\t" + f"Manual output set:\t {self.manual_output}V" + "\n"
        message = message + "|\t" + " Set Point related".center(50, '=') + '\n'
        message = message + "|\t\t" + f"Internal setpoint = {self.setpoint} V, Ramping " + highlight_status(
            self.spramp_status) + '\n'
        message = message + "|\t\t" + f"Setpoint input mode " + self.setpoint_input_mode + f", Ext setpoint input {self.setpoint_input}V" + '\n'
        message = message + "|\t\t" + f"Setpoint RAMP speed = {self.spramprate} V/s, action " + highlight_status(
            self.spramp_action) + "\n"
        message = message + "|\t" + " P,I,D and Offset Status".center(50, '=') + "\n"
        message = message + "|\t\t" + f" P = {self.prop_gain}    , \taction = " + highlight_status(
            self.prop_action) + "\n"
        message = message + "|\t\t" + f" I = {self.intg_gain} 1/s, \taction = " + highlight_status(
            self.intg_action) + "\n"
        message = message + "|\t\t" + f" D = {self.derv_gain}   s, \taction = " + highlight_status(
            self.derv_action) + "\n"
        message = message + "|\t\t" + f"Off = {self.outoffset}  V, \taction = " + highlight_status(
            self.outoffset_action) + "\n"
        message = message + "SRS PID controller SIM960 Status Summary Ends".center(80, '-') + "\n"
        print(message)
        return message

    def set_manual_output_max(self, num):
        self.__manual_output_max = num

    def set_manual_output_min(self, num):
        self.__manual_output_min = num

    @property
    def serialNumber(self):
        return self.equipment_IDN.split(',')[-2]

    @property
    def equipment_IDN(self):
        return self.query("*IDN?")

    # ----P,I,D,Offset related----
    @property
    def prop_action(self):
        return self.get_prop_action()

    @prop_action.setter
    def prop_action(self, status):
        self.set_prop_action(status)

    @property
    def intg_action(self):
        return self.get_intg_action()

    @intg_action.setter
    def intg_action(self, status):
        self.set_intg_action(status)

    @property
    def derv_action(self):
        return self.get_derv_action()

    @derv_action.setter
    def derv_action(self, status):
        self.set_derv_action(status)

    @property
    def outoffset_action(self):
        return self.get_outoffset_action()

    @outoffset_action.setter
    def outoffset_action(self, status):
        self.set_outoffset_action(status)

    @property
    def prop_gain(self):
        return self.get_prop_gain()

    @prop_gain.setter
    def prop_gain(self, num):
        self.set_prop_gain(num)

    @property
    def intg_gain(self):
        return self.get_intg_gain()

    @intg_gain.setter
    def intg_gain(self, num):
        self.set_intg_gain(num)

    @property
    def derv_gain(self):
        return self.get_derv_gain()

    @derv_gain.setter
    def derv_gain(self, num):
        self.set_derv_gain(num)

    @property
    def outoffset(self):
        return self.get_outoffset()

    @outoffset.setter
    def outoffset(self, num):
        self.set_outoffset(num)

    # ====Output mode related====
    @property
    def output_mode(self):  # will be 'MAN' or 'PID'
        return self.get_output_mode()

    @output_mode.setter
    def output_mode(self, status):  # available_status = ['0','1','pid','man']
        self.set_output_mode(status)

    # Setpoint setting related
    @property
    def setpoint_input_mode(self):  # will be 'EXT' or 'INT'
        return self.get_setpoint_input_mode()

    @setpoint_input_mode.setter
    def setpoint_input_mode(self, status):  # available_status = ['0','1','int','ext']
        self.set_setpoint_input_mode(status)

    @property
    def setpoint(self):
        return self.get_setpoint()

    @setpoint.setter
    def setpoint(self, num):
        self.set_setpoint(num)

    # Setpoint ramping related
    @property
    def spramp_action(self):
        return self.get_spramp_action()

    @spramp_action.setter
    def spramp_action(self, status):
        self.set_spramp_action(status)

    @property
    def spramprate(self):
        return self.get_spramprate()

    @spramprate.setter
    def spramprate(self, num):
        self.set_spramprate(num)

    @property
    def spramp_status(self):
        return self.get_spramp_status()

    # Manual output setpoint
    @property
    def manual_output(self):
        return self.get_manual_output()

    @manual_output.setter
    def manual_output(self, num):
        self.set_manual_output(num)

    # Output limits
    @property
    def output_upperlim(self):
        return self.get_output_upperlim()

    @output_upperlim.setter
    def output_upperlim(self, num):
        self.set_output_upperlim(num)

    @property
    def output_lowerlim(self):
        return self.get_output_lowerlim()

    @output_lowerlim.setter
    def output_lowerlim(self, num):
        self.set_output_lowerlim(num)

    # Monitors
    @property
    def setpoint_input(self):
        return self.get_setpoint_input()

    @property
    def measure_input(self):
        return self.get_measure_input()

    @property
    def amplified_error(self):
        return self.get_amplified_error()

    @property
    def output_voltage(self):
        return self.get_output_voltage()

    def manual_sweep(self, voltage_list, start_pause=1, interval_pause=0.1, plot=True):
        self.mainframe.clear()
        self.output_mode = 'MAN'
        voltage_list = np.array(voltage_list)
        measure_input = np.zeros(shape=voltage_list.shape)
        from tqdm import tqdm
        for ii, vol in enumerate(tqdm(voltage_list)):
            try:
                self.write(f"MOUT{vol:.3f}", clear=False)
                time.sleep(start_pause) if ii == 0 else time.sleep(interval_pause)
                measure_input[ii] = float(self.query("MMON?", clear=False))
            except:
                continue
        if plot:
            plt.figure()
            plt.plot(voltage_list, measure_input)
            plt.xlabel("Manual output voltage (V)")
            plt.ylabel("System Error signal input (V)")
            plt.title("Manual output Ramp response")
            plt.show()
        return measure_input

    ## ------------------Controller Settings------------------
    # PCTL(?) z 3 – 10 Proportional action ON/OFF
    def get_prop_action(self, clear=True):
        cmd = "PCTL"
        return self.__get_onoff_withcmd(cmd, clear=clear)

    def set_prop_action(self, status, clear=True):
        cmd = "PCTL"
        self.__set_onoff_withcmd(cmd, status, printstr="Proportional Gain Calculator action", clear=clear)

    # ICTL(?) z 3 – 10 Integral action ON/OFF
    def get_intg_action(self, clear=True):
        cmd = "ICTL"
        return self.__get_onoff_withcmd(cmd, clear=clear)

    def set_intg_action(self, status, clear=True):
        cmd = "ICTL"
        self.__set_onoff_withcmd(cmd, status, printstr="Integral Gain Calculator action", clear=clear)

    # DCTL(?) z 3 – 10 Derivative action ON/OFF
    def get_derv_action(self, clear=True):
        cmd = "DCTL"
        return self.__get_onoff_withcmd(cmd, clear=clear)

    def set_derv_action(self, status, clear=True):
        cmd = "DCTL"
        self.__set_onoff_withcmd(cmd, status, printstr="Derivative Gain Calculator action", clear=clear)

    # OCTL(?) z 3 – 10 Offset ON/OFF
    def get_outoffset_action(self, clear=True):
        cmd = "OCTL"
        return self.__get_onoff_withcmd(cmd, clear=clear)

    def set_outoffset_action(self, status, clear=True):
        cmd = "OCTL"
        self.__set_onoff_withcmd(cmd, status, printstr="Output Offset Calculator action", clear=clear)

    # GAIN(?) {f} 3 – 10 Proportional Gain
    def get_prop_gain(self, clear=True):
        cmd = "GAIN"
        return self.__get_num_withcmd(cmd, clear=clear)

    def set_prop_gain(self, num, clear=True):
        cmd = "GAIN"
        num = num if isinstance(num, numbers.Number) else self.__decode_str_to_SIunit(num)
        from math import log10
        self.__set_num_withcmd(
            cmd,
            num,
            printstr="Proportional Gain in V/V",
            low_lim=-self.__prop_gain_max,
            high_lim=self.__prop_gain_max,
            decimal=None if self.__prop_gain_resolution == None else int(-log10(self.__prop_gain_resolution)),
            # resolution=self.__prop_gain_resolution,
            clear=clear)

    # APOL(?) z 3 – 11 Controller Polarity
    # INTG(?) {f} 3 – 11 Integral Gain
    def get_intg_gain(self, clear=True):
        cmd = "INTG"
        return self.__get_num_withcmd(cmd, clear=clear)

    def set_intg_gain(self, num, clear=True):
        cmd = "INTG"
        num = num if isinstance(num, numbers.Number) else self.__decode_str_to_SIunit(num)
        from math import log10
        self.__set_num_withcmd(
            cmd,
            num,
            printstr="Integral Gain in 1/seconds",
            low_lim=self.__intg_gain_min,
            high_lim=self.__intg_gain_max,
            decimal=None if self.__intg_gain_resolution == None else int(-log10(self.__intg_gain_resolution)),
            # resolution=self.__intg_gain_resolution,
            clear=clear)

    # DERV(?) {f} 3 – 11 Derivative Gain
    def get_derv_gain(self, clear=True):
        cmd = "DERV"
        return self.__get_num_withcmd(cmd, clear=clear)

    def set_derv_gain(self, num, clear=True):
        cmd = "DERV"
        num = num if isinstance(num, numbers.Number) else self.__decode_str_to_SIunit(num)
        from math import log10
        self.__set_num_withcmd(
            cmd,
            num,
            printstr="Derivative Gain in seconds",
            low_lim=self.__derv_gain_min,
            high_lim=self.__derv_gain_max,
            decimal=None if self.__derv_gain_resolution == None else int(-log10(self.__derv_gain_resolution)),
            # resolution=self.__derv_gain_resolution,
            clear=clear)

    # OFST(?) {f} 3 – 11 Output Offset
    def get_outoffset(self, clear=True):
        cmd = "OFST"
        return self.__get_num_withcmd(cmd, clear=clear)

    def set_outoffset(self, num, clear=True):
        cmd = "OFST"
        num = num if isinstance(num, numbers.Number) else self.__decode_str_to_SIunit(num)
        from math import log10
        self.__set_num_withcmd(
            cmd,
            num,
            printstr="Output offset in Volts",
            low_lim=self.__outoffset_min,
            high_lim=self.__outoffset_max,
            decimal=None if self.__outoffset_resolution == None else int(-log10(self.__outoffset_resolution)),
            # resolution=self.__outoffset_resolution,
            clear=clear)

    ## ------------------Controller Configuration------------------
    # AMAN(?) z 3 – 12 Output (Manual Output/PID Control)
    def get_output_mode(self, clear=True):
        r = self.query("AMAN?", clear=clear)
        if r == '0':
            return 'MAN'
        elif r == '1':
            return 'PID'
        else:
            raise ValueError(self.devicename + ": Unrecognized output mode " + r + ". Should be '0':manual, '1':PID ")

    def set_output_mode(self, status, clear=True):
        status = str(status).casefold()
        available_status = ['0', '1', 'pid', 'man']
        if status not in available_status:
            raise ValueError(self.devicename + ": Unrecognized output mode " + status + " to set. Should choose from " +
                             str(available_status))
        if status == '1':
            print(self.devicename + ": output mode 1 is understood as PID mode.")
            status = 'pid'
        elif status == '0':
            print(self.devicename + ": output mode 0 is understood as Manual mode.")
            status = 'man'
        if status == 'pid':
            self.write("AMAN1", clear=clear)
            print(self.devicename + ": PID output is turned ON.")
        else:
            self.write("AMAN0", clear=clear)
            print(self.devicename + ": PID output is turned OFF, output mode is turnd to Manual.")

    # INPT(?) z 3 – 12 Input (Internal/External Setpoint)
    def get_setpoint_input_mode(self, clear=True):
        r = self.query("INPT?", clear=clear)
        if r == '0':
            return 'INT'
        elif r == '1':
            return 'EXT'

    def set_setpoint_input_mode(self, status, clear=True):
        status = str(status).casefold()
        available_status = ['0', '1', 'int', 'ext']
        if status not in available_status:
            raise ValueError(self.devicename + ": Unrecognized setpoint input status " + status +
                             " to set. Should choose from " + str(available_status))
        if status == '1':
            status = 'ext'
        elif status == '0':
            status = 'int'
        if status == 'ext':
            self.write("INPT1", clear=clear)
            print(self.devicename + ": Setpoint input is switched to EXTernal.")
        else:
            self.write("INPT0", clear=clear)
            print(self.devicename + ": Setpoint input is switched to INTernal.")

    # SETP(?) {f} 3 – 12 New setpoint
    def get_setpoint(self, clear=True):
        cmd = "SETP"
        return self.__get_num_withcmd(cmd, clear=clear)

    def set_setpoint(self, num, clear=True):
        cmd = "SETP"
        num = num if isinstance(num, numbers.Number) else self.__decode_str_to_SIunit(num)
        from math import log10
        self.__set_num_withcmd(
            cmd,
            num,
            printstr="Locking set point in Volt",
            low_lim=self.__setpoint_min,
            high_lim=self.__setpoint_max,
            decimal=None if self.__setpoint_resolution == None else int(-log10(self.__setpoint_resolution)),
            # resolution=self.__setpoint_resolution,
            clear=clear)

    # RAMP(?) z 3 – 12 Internal setpoint ramping ON/OFF
    def get_spramp_action(self, clear=True):
        cmd = "RAMP"
        return self.__get_onoff_withcmd(cmd, clear=clear)

    def set_spramp_action(self, status, clear=True):
        cmd = "RAMP"
        self.__set_onoff_withcmd(cmd, status, printstr="Output Offset Calculator action", clear=clear)

    # RATE(?) {f} 3 – 12 Setpoint ramping Rate
    def get_spramprate(self, clear=True):
        cmd = "RATE"
        return self.__get_num_withcmd(cmd, clear=clear)

    def set_spramprate(self, num, clear=True):
        cmd = "RATE"
        num = num if isinstance(num, numbers.Number) else self.__decode_str_to_SIunit(num)
        self.__set_num_withcmd(
            cmd,
            num,
            printstr="Setpoint Ramping Rate in V/s",
            low_lim=self.__spramprate_min,
            high_lim=self.__spramprate_max,
            decimal=None if self.__spramprate_resolution == None else int(-log10(self.__spramprate_resolution)),
            # resolution=self.__spramprate_resolution,
            clear=clear)

    # RMPS? 3 – 13 Setpoint ramping status
    def get_spramp_status(self, clear=True):
        cmd = 'RMPS'
        return self.__get_onoff_withcmd(cmd, clear=clear)

    # STRT z 3 – 13 Pause or continue ramping
    def spramp_START(self, clear=True):
        self.write("STRT1", clear=clear)
        print(self.devicename + ": Setpoint ramp STARTed.")

    def spramp_STOP(self, clear=True):
        self.write("STRT0", clear=clear)
        print(self.devicename + ": Setpoint ramp STOPped.")

    # MOUT(?) {f} 3 – 13 Manual Output
    def get_manual_output(self, clear=True):
        cmd = "MOUT"
        return self.__get_num_withcmd(cmd, clear=clear)

    def set_manual_output(self, num, clear=True):
        cmd = "MOUT"
        num = num if isinstance(num, numbers.Number) else self.__decode_str_to_SIunit(num)
        # ---------------
        low_lim = self.__manual_output_min 
        high_lim = self.__manual_output_max
        printstr="Output in Manual Mode in Volt"
        if not low_lim == None:
            low_lim = float(low_lim)
            if num < low_lim:
                raise ValueError(self.devicename + ": Setting " + printstr + " number over low range." +
                                 f"Given number {num} should NOT lower than {low_lim}")
        if not high_lim == None:
            high_lim = float(high_lim)
            if num > high_lim:
                raise ValueError(self.devicename + ": Setting " + printstr + " number over high range." +
                                 f"Given number {num} should NOT higher than {high_lim}")
        # ---------------
        from math import log10
        if self.manual_output_ramp == 0:
            self.__set_num_withcmd(
                cmd,
                num,
                printstr="Output in Manual Mode in Volt",
                low_lim=self.__manual_output_min,
                high_lim=self.__manual_output_max,
                decimal=None if self.__manual_output_resolution == None else
                int(-log10(self.__manual_output_resolution)),
                # resolution=self.__manual_output_resolution,
                clear=clear)
        else:
            volt_start = self.get_manual_output(clear=clear)
            volt_stop = num
            volt_incr = np.abs(self.manual_output_ramp)
            volt_list = np.round(
                np.linspace(volt_start, volt_stop, max(int(np.ceil(np.abs(volt_start - volt_stop) / volt_incr)), 2)) *
                1000) / 1000
            print(self.devicename + ": ....Manual output voltage Ramping.... Disable ranp by set self.manual_output_ramp=0. ")
            decimal=3 if self.__manual_output_resolution == None else int(-log10(self.__manual_output_resolution))
            for vv in volt_list:
                self.write(cmd + "{:.{}f}".format(vv, decimal), clear=clear)
                print(self.devicename+f": Output in Manual Mode in Volt set to "+"{:.{}f}".format(vv, decimal)+".")
                # self.__set_num_withcmd(cmd,
                #                        vv,
                #                        printstr="Output in Manual Mode in Volt",
                #                        low_lim=self.__manual_output_min,
                #                        high_lim=self.__manual_output_max,
                #                        decimal=None if self.__manual_output_resolution == None else
                #                        int(-log10(self.__manual_output_resolution)),
                #                        clear=clear)
            print(self.devicename + ": ....Manual output voltage Ramp Finished. Disable ramp by set self.manual_output_ramp=0. ")
    # ULIM(?) {f} 3 – 13 Upper Output Limit
    def get_output_upperlim(self, clear=True):
        cmd = "ULIM"
        return self.__get_num_withcmd(cmd, clear=clear)

    def set_output_upperlim(self, num, clear=True):
        cmd = "ULIM"
        num = num if isinstance(num, numbers.Number) else self.__decode_str_to_SIunit(num)
        from math import log10
        self.__set_num_withcmd(cmd, 
                               num,
                               decimal=None if self.__output_upperlim_resolution == None else
                               int(-log10(self.__output_upperlim_resolution)),
                               printstr="Output Upper limit in Volt", clear=clear)

    # LLIM(?) {f} 3 – 14 Lower Output Limit
    def get_output_lowerlim(self, clear=True):
        cmd = "LLIM"
        return self.__get_num_withcmd(cmd, clear=clear)

    def set_output_lowerlim(self, num, clear=True):
        cmd = "LLIM"
        num = num if isinstance(num, numbers.Number) else self.__decode_str_to_SIunit(num)
        from math import log10
        self.__set_num_withcmd(cmd, 
                               num, 
                               decimal=None if self.__output_lowerlim_resolution == None else
                                int(-log10(self.__output_lowerlim_resolution)),
                               printstr="Output Lower limit in Volt", clear=clear)

    ## ------------------Monitor------------------
    # SMON? [i] 3 – 14 Setpoint Input Monitor
    def get_setpoint_input(self, clear=True):
        cmd = "SMON"
        return self.__get_num_withcmd(cmd, clear=clear)

    # MMON? [i] 3 – 14 Measure Input Monitor
    def get_measure_input(self, clear=True):
        cmd = "MMON"
        return self.__get_num_withcmd(cmd, clear=clear)

    # EMON? [i] 3 – 15 Amplified Error Monitor
    def get_amplified_error(self, clear=True):
        cmd = "EMON"
        return self.__get_num_withcmd(cmd, clear=clear)

    # OMON? [i] 3 – 15 Output Monitor
    def get_output_voltage(self, clear=True):
        cmd = "OMON"
        return self.__get_num_withcmd(cmd, clear=clear)

    # RFMT(?) {z} 3 – 15 Output Streaming Records Format
    # SOUT [z] 3 – 16 Stop Streaming
    # FPLC(?) {i} 3 – 16 Frequency of Power Line Cycle

    ## ------------------- Set/Get Private Methods ------------------- ##
    def __get_onoff_withcmd(self, cmd, clear=True):
        #example: cmd = "PCTL" give proportional gain status
        cmd = str(cmd).upper()
        result = str(self.query(cmd + "?", clear=clear)).casefold()
        if result in set(['1', 'on']):
            return 'ON'
        elif result in set(['0', 'off']):
            return 'OFF'
        else:
            raise ValueError(self.devicename + ": Unrecognized ON/OFF string [" + result + "] returned.")

    def __set_onoff_withcmd(self, cmd, status, printstr=None, clear=True):
        #example: cmd = "PCTL" sets proportional gain status
        cmd = str(cmd).upper()
        status = str(status).casefold()
        if printstr == None:
            printstr = cmd
        if status in set(['1', 'on']):
            self.write(cmd + "1", clear=clear)
            print(self.devicename + ": " + printstr + " is set to ON.")
        elif status in set(['0', 'off']):
            self.write(cmd + "0")
            print(self.devicename + ": " + printstr + " is set to OFF.")
        else:
            raise ValueError(self.devicename + ": Unrecognized ON/OFF string [" + status +
                             "] given. Should be 0|1|'on'|'off' ")

    def __get_num_withcmd(self, cmd, clear=True):
        cmd = str(cmd).upper()
        result = str(self.query(cmd + "?", clear=clear)).replace(" ", "")
        return float(result)

    def __set_num_withcmd(self,
                          cmd,
                          num,
                          printstr=None,
                          low_lim=None,
                          high_lim=None,
                          decimal=None,
                        #   resolution=None, # TODO: Deprecate this option!
                          clear=True):
        cmd = str(cmd).upper()
        num = float(num)
        if printstr == None:
            printstr = cmd
        if (low_lim != None) and (high_lim != None):
            if float(low_lim) > float(high_lim):
                raise ValueError(self.devicename + ": Setting " + printstr + " number Given invalid range." +
                                 f"Given low_lim {float(low_lim)} should NOT higher than high_lim {float(high_lim)}")
        if not low_lim == None:
            low_lim = float(low_lim)
            if num < low_lim:
                raise ValueError(self.devicename + ": Setting " + printstr + " number over low range." +
                                 f"Given number {num} should NOT lower than {low_lim}")
        if not high_lim == None:
            high_lim = float(high_lim)
            if num > high_lim:
                raise ValueError(self.devicename + ": Setting " + printstr + " number over high range." +
                                 f"Given number {num} should NOT higher than {high_lim}")
        if not decimal == None:  
            decimal = int(decimal)
            new_num = Decimal("{:.{}f}".format(num, decimal))
            if not abs(Decimal(num) -new_num)<0.00001:
                warnings.warn(self.devicename + ": Setting " + printstr + " precision overgiven, " + str(decimal) +
                              " decimal degits required. Given number " + str(num) + " is rounded.")
                num = new_num
        # if not resolution == None:
        #     num = num // resolution * resolution  
        self.write(cmd + str(num), clear=clear)
        print(self.devicename + ": Setting " + printstr + f" to {num}.")

    def __decode_str_to_SIunit(self, encoded_str: str) -> float:
        if encoded_str[-4:].casefold() in ['mv/s', 'mv/v']:
            return float(encoded_str[0:-4]) / 1000
        elif encoded_str[-3:].casefold() in ['v/s', 'v/v']:
            return float(encoded_str[0:-3])
        elif encoded_str[-3:].casefold() in ['/ms', '/mv', '\ms', '\mv']:
            return float(encoded_str[0:-3]) * 1000
        elif encoded_str[-2:].casefold() in ['mv', 'ms']:
            return float(encoded_str[0:-2]) / 1000
        elif encoded_str[-2:].casefold() in ['/s']:
            return float(encoded_str[0:-2])
        elif encoded_str[-1:].casefold() in ['v', 's']:
            return float(encoded_str[0:-1])
        else:
            raise ValueError(self.devicename + ": Unrecognized unit str " + encoded_str + " while converting.")


class SRS_VoltSorc_SIM928(object):

    def __init__(self, mainframe, slot: int, name="SRS Isolated Voltage Source SIM928"):
        # mainframe is an instance of SRS_SIM900
        self.mainframe = mainframe
        self.slot = slot
        self.devicename = name

    def write(self, cmd):
        self.mainframe.write_slot(self.slot, cmd)

    def query(self, cmd):
        return self.mainframe.query_slot(self.slot, cmd)

    def read(self, cmd):
        return self.mainframe.read_slot(self.slot, cmd)


if __name__ == '__main__':
    srs = SRS_SIM900(addr="GPIB0::2::INSTR")
    srs.connect()

    servo1 = SRS_PIDcontrol_SIM960(srs, 5)
    servo1.set_manual_output_max(4)
    servo1.set_manual_output_min(-4)

    servo1.set_output_lowerlim(-4)
    servo1.set_output_upperlim(4)

    msg = servo1.printStatus()
    
    filename = r"Z:\Maodong\Projects\Keck\System Assembly test\RIO Rb locking\20230430\servo.txt"   

    with  open(filename,"w") as f:
        f.write("")
    with  open(filename,"a") as f:
        f.write(msg+'\n')
        f.write("".center(80, "=")+"\n")
        f.write("time\t")
        f.write("measured input\t")
        f.write("output\t")
        f.write("amplified error\t")
        f.write("\n")

    import time
    while True:
        try:
            with open(filename,"a") as f:
                f.write(time.ctime()+"\t")

                print("".center(80, "-"))

                in_v = servo1.measure_input
                f.write(f"{in_v:.5f}\t")
                print(f"Measured input: {in_v:.5f} V")

                out_v = servo1.output_voltage
                f.write(f"{out_v:.5f}\t")
                print(f"Output voltage: {out_v:.5f} V")

                amp_err = servo1.amplified_error
                f.write(f"{amp_err:.5f}\t")
                print(f"Amplified error: {amp_err:.5f} V")

                f.write("\n")
        except Exception as e:
            print(e)
        time.sleep(1)
