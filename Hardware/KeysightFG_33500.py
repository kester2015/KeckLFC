from .Device import Device
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
    
    
    def sin(self, freq, amp, offset, phase=0):
        self.write(f"APPL:SIN {freq}, {amp}, {offset}, {phase}")

    def square(self, freq, amp, offset, phase=0, duty=50):
        self.write(f"APPL:SQU {freq}, {amp}, {offset}, {phase}, {duty}")

    def ramp(self, freq, amp, offset, phase=0, sym=50):
        self.write(f"APPL:RAMP {freq}, {amp}, {offset}, {phase}, {sym}")
    
    def arbitary(self, func_array, sample_rate, amp, offset, phase=0):
        self.write(f"APPL:USER {sample_rate}, {amp}, {offset}, {phase}")
        self.write(f"DATA:VOL:CLE")
        self.write(f"DATA:VOL:DATA {func_array}")
        self.write(f"FUNC:USER")

    def dc_voltage(self, volt):
        self.write(f"APPL:DC DEF, DEF, {volt}")
    
    def dc_current(self, current):
        self.write(f"APPL:DC DEF, DEF, DEF, {current}")

    


    #set output channel impedance
    def set_channel_impedance(self, channel, impedance):
        self.write(f"OUTP{channel}:IMP {impedance}")
    #set output channel amplitude
    def set_channel_amplitude(self, channel, amp):
        self.write(f"VOLT{channel} {amp}")
    #set output channel offset
    def set_channel_offset(self, channel, offset):
        self.write(f"VOLT:OFFS{channel} {offset}")
    #set output channel phase
    def set_channel_phase(self, channel, phase):
        self.write(f"PHAS{channel} {phase}")
    #set output channel frequency
    def set_channel_frequency(self, channel, freq):
        self.write(f"FREQ{channel} {freq}")
    #set output channel duty cycle
    def set_channel_duty_cycle(self, channel, duty):
        self.write(f"DUTY{channel} {duty}")
    #set output channel symmetry
    def set_channel_symmetry(self, channel, sym):
        self.write(f"SYMM{channel} {sym}")
    #set output channel state
    def set_channel_state(self, channel, state):
        self.write(f"OUTP{channel} {state}")




    #get output channel amplitude
    def get_channel_amplitude(self, channel):
        return self.query(f"VOLT{channel}?")
    #get output channel offset
    def get_channel_offset(self, channel):
        return self.query(f"VOLT:OFFS{channel}?")
    #get output channel phase
    def get_channel_phase(self, channel):
        return self.query(f"PHAS{channel}?")
    #get output channel frequency
    def get_channel_frequency(self, channel):
        return self.query(f"FREQ{channel}?")
    #get output channel duty cycle
    def get_channel_duty_cycle(self, channel):
        return self.query(f"DUTY{channel}?")
    #get output channel symmetry
    def get_channel_symmetry(self, channel):
        return self.query(f"SYMM{channel}?")
    #get output channel impedance
    def get_channel_impedance(self, channel):
        return self.query(f"OUTP{channel}:IMP?")
    #get output channel state
    def get_channel_state(self, channel):
        return self.query(f"OUTP{channel}?")
    
    #get channel parameters
    def get_channel_parameters(self, channel):
        print(f"Channel {channel} parameters:")
        print(f"Amplitude: {self.get_channel_amplitude(channel)}")
        print(f"Offset: {self.get_channel_offset(channel)}")
        print(f"Phase: {self.get_channel_phase(channel)}")
        print(f"Frequency: {self.get_channel_frequency(channel)}")
        print(f"Duty Cycle: {self.get_channel_duty_cycle(channel)}")
        print(f"Symmetry: {self.get_channel_symmetry(channel)}")
        print(f"Impedance: {self.get_channel_impedance(channel)}")
        print(f"State: {self.get_channel_state(channel)}")
    

    #apply wave function with parameters to output channel
    def channel_apply(self, channel, function, freq, amp, offset, phase=0, duty=50, sym=50):
        if function == "sin":
            self.sin(freq, amp, offset, phase)
        elif function == "square":
            self.square(freq, amp, offset, duty)
        elif function == "ramp":
            self.ramp(freq, amp, offset, sym)
        elif function == "dc":
            self.dc_voltage(amp)
        else:
            print("Function not supported")
        
        self.get_channel_parameters(channel)
        self.set_channel_state(channel, "ON")

    
if __name__ == "__main__":
    fg = KeysightFG_33500()
    fg.connect()
    print(fg.IDN)
    fg.disconnect()