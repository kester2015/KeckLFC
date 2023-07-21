# Reconfigure logger
import os, sys, warnings, inspect

# ------------ Logger start ------------
from loguru import logger

def get_call_kwargs(level=1):
    frame = inspect.currentframe().f_back
    for _ in range(level):  # get the level-th frame
        frame = frame.f_back
    code_obj = frame.f_code
    return dict(
        function_module=os.path.basename(code_obj.co_filename),
        function_name=code_obj.co_name,
        function_line=frame.f_lineno,
    )

def send_log_file_via_email(fname):
    import win32com.client
    ol = win32com.client.Dispatch('Outlook.Application')
    # size of the new email
    olmailitem = 0x0
    newmail = ol.CreateItem(olmailitem)
    newmail.Subject = '[Regular] Keck LFC log file ' + fname
    newmail.To = 'maodonggao@gmail.com; maodonggao@outlook.com'
    # newmail.CC='maodonggao@outlook.com'
    newmail.Body = 'Hello, \n Attached are the rotated data logging file at Keck. \n\n Best, \n Maodong'

    newmail.Attachments.Add(fname)
    newmail.Send()
    print(f'Log file {fname} sent')

fname = os.path.expanduser(r'~\Desktop\Keck\Logs\test.log')
logger.remove()  # remove logger with default format
logger_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{extra[devicename]}</cyan> | "
    "<cyan>{extra[function_module]}</cyan>:<cyan>{extra[function_name]}</cyan>:<cyan>{extra[function_line]}</cyan>\n"
    "<level>{message}</level>")
logger.add(sys.stderr, format=logger_format, level="INFO")  # recover console print
logger.add(fname, format=logger_format, level="INFO", rotation="1 MB", retention=5,
           compression=send_log_file_via_email)  # 1MB per file, 5 files max
logger.bind(devicename="Device").info('logger initialized', **get_call_kwargs(level=0))

# ------------ Logger end ------------


# Base class for devices
class Device:
    import pyvisa
    rm = pyvisa.ResourceManager()

    def __init__(self, addr, name='', isVISA=True):
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
                self.info(self.devicename + " connected")
                return 1
            except Exception as e:
                self.error(f"Error:{e}")
                return -1
        return 0

    def disconnect(self):
        if self.connected:
            if self.isVISA:
                self.inst.close()
            self.connected = False
            self.info(self.devicename + " disconnected")
            return 1
        return 0

    def write(self, cmd):
        self.inst.write(cmd)

    def read(self):
        return self.inst.read()

    def query(self, cmd):
        return self.inst.query(cmd)

    # logging
    logger = logger
    
    def debug(self, x, name='', level=1):
        logger.debug(x, devicename=name or self.devicename, **get_call_kwargs(level))
        # print(x)

    def info(self, x, name='', level=1):
        logger.info(x, devicename=name or self.devicename, **get_call_kwargs(level))
        # print(x)

    def warning(self, x, name='', level=1):
        logger.warning(x, devicename=name or self.devicename, **get_call_kwargs(level))
        warnings.warn(x)

    def error(self, x, name='', level=1):
        logger.error(x, devicename=name or self.devicename, **get_call_kwargs(level))
        # raise Exception(x)