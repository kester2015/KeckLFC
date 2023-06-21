from .Device import Device

## Following code is adapted from 
# https://github.com/ograsdijk/Agiltron-SelfAlign/blob/main/agiltron_selfalign/module.py


from typing import Optional

import pyvisa
from pyvisa.constants import Parity


def check_port(fiber_port: int, number_of_ports: int) -> bool:
    """
    Check if given fiber port is an integer and in the range of valid fiber ports.

    Args:
        port (int): fiber port to switch to
        number_of_ports (int): total number of fiber ports on the switch

    Raises:
        TypeError: unsupported type for the fiber port
        ValueError: fiber port out of range

    Returns:
        bool: returns True if the fiber port is valid, False otherwise
    """
    if not isinstance(fiber_port, int):
        raise TypeError(f"unsupported type for fiber port: {type(fiber_port)}")
    v = (fiber_port > 0) & (fiber_port <= number_of_ports)
    if not v:
        raise ValueError(f"fiber port {fiber_port} out of range")
    else:
        return v


class AgiltronSelfAlign(Device):
    def __init__(self, addr='COM49', name='Agiltron 1 by 6 switch'):
        # resource_name: str, timeout: int = 2, number_of_ports: int = 16,):
        super().__init__(addr=addr, name=name, isVISA=False)

        self.rm = pyvisa.ResourceManager()
        self.instrument = self.rm.open_resource(
            resource_name=self.addr,
            timeout=2,
            parity=Parity.none,
            data_bits=8,
            baud_rate=9600,
            write_termination="\r\n",
            read_termination="\r\n",
        )
        self.number_of_ports: int = 6
        self.fiber_port: Optional[int] = None

        self.isVISA = True
        self.inst = self.instrument # for compatibility with Device class

    def set_fiber_port(self, fiber_port: int) -> None:
        """
        Switch fiber switch to port `fiber_port`.

        Args:
            fiber_port (int): fiber port to switch to
        """
        check_port(fiber_port, self.number_of_ports)
        if fiber_port != self.fiber_port:
            cmd = b"\x01\x35\x00" + bytes([fiber_port - 1])
            self.instrument.write_raw(cmd)
            ret = self.instrument.read_bytes(4)
            assert (
                ret == b"\x01\x35\xff\xff"
            ), f"invalid return message, fiber port not set to {fiber_port}"
            self.fiber_port = fiber_port

    def home(self) -> None:
        """
        Home the fiber switch, i.e. move to port 1.
        """
        self.instrument.write(b"\x01\x30\x00\x00")