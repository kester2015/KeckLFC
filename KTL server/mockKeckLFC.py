import time, threading
import xml.etree.ElementTree as ET

VERBOSE = False

def parse_xml(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()

    keyword_names = []
    keyword_types = []

    for keyword in root.findall('keyword'):
        name = keyword.find('name').text
        keyword_type = keyword.find('type').text
        capability_type = keyword.find('capability').get('type')

        print('Parsed keyword: name=%s\ttype=%s\tcapability=%s' % (name, keyword_type, capability_type))
        keyword_names.append(name)
        keyword_types.append(keyword_type)

    return keyword_names, keyword_types


def test_clock(stop, mkl):
    while True:
        mkl.keywords['ICECLK'] = time.strftime('%H:%M:%S')
        time.sleep(1)
        if stop(): 
            mkl.clock = None
            break
            
class mockKeckLFC(object):

    def __init__(self):

        keyword_names, keyword_types = parse_xml('LFC.xml.sin')
        
        self.keywords = {keyword: None for keyword in keyword_names}
        self.types = {keyword: keyword_type for keyword, keyword_type in zip(keyword_names, keyword_types)}

        func_dict = {}
        for keyword in self.keywords:
            method_name = f'{keyword}'
            method = getattr(self, method_name)
            func_dict[keyword] = method
        
        self.funcs = func_dict

        for key in keyword_names:
            print('parsed Keyword ', key, self.types[key], self.funcs[key])

    def __getitem__(self, key):
        '''Read keywords. 
        Calls the associated function, stores the returned value. 
        This is called periodically.'''
        val = self.funcs[key](value=None)
        if val != None: val = self.convert_type(self.types[key], val)

        self.keywords[key] = val
        
        return val
    
    def __setitem__(self, key, val):
        '''Write keywords.
        When keyword values are changed by KTL user, stores the value.'''
        if val != None: val = self.convert_type(self.types[key], val)
        
        status = self.funcs[key](value = val)
        if status == 0: self.keywords[key] = val
    
    @staticmethod
    def convert_type(typ, val):
        
        if typ == 'integer': return int(val)
        elif typ == 'double': return float(val)
        elif typ == 'enumerated': return int(val)
        elif typ == 'string': return str(val)
        elif typ == 'boolean': 
            if val in ['True', '1', 1, True] : return True
            else: return False
        else:
            print('Unrecognized type')
            raise Exception

    ########## Test keywords and functions ############
    def ICECLK_ONOFF(self, value=None):
        '''Turn on / off the clock '''
        if VERBOSE: print('ICECLK_ONOFF func called')
        if value == None: return self.keywords['ICECLK_ONOFF']
        
        else:
            print('ICECLK value: ', value)
            print('Writing value', value, 'to ICECLK_ONOFF')
            if value == True: self.start_clock()
            elif value == False: self.stop_clock()
            else: 
                print('something wrong with ICECLK_ONOFF')
                return 1
            return 0
    
    def ICECLK(self, value=None):
        ''' shows current time returned by ice'''
        if VERBOSE: print('ICECLK func called')
        if value == None: return self.keywords['ICECLK']
        
        else:
            print('Writing value', value, 'to ICECLK')
            return 0

    def ICESTA(self, value=None):
        ''' shows status of the ICE connection'''
        if VERBOSE: print('icesta func called')
        if value == None: return self.keywords['ICESTA']
        else:
            print('Writing value', value, 'to icesta')
            if value == 2: print('ICE - KTL disconnected!')
            return 0             
        
    def start_clock(self):
        self._stop_clock = False
        self.clock = threading.Thread(target = test_clock, args = (lambda: self._stop_clock, self))
        print('\t\t\tstart clock')
        self.clock.start()
    
    def stop_clock(self):
        print('\t\t\tstop clock')
        self._stop_clock = True
        self.clock.join()
        
    ########## LFC Keywords Implementation ############
    def LFC_RIO_T(self, value=None):
        '''RIO pump laser temperature. float?'''
        if value == None: return self.keywords['LFC_RIO_T']
        else:
            print('Writing value', value, 'to LFC_RIO_T')
            return 0

    def LFC_RIO_I(self, value=None):
        '''RIO pump laser current. float?'''
        if value == None: return self.keywords['LFC_RIO_I']
        else:
            print('Writing value', value, 'to LFC_RIO_I')
            return 0

    def LFC_EDFA27_P(self, value=None):
        '''Small  EDFA (500 mW) 1 output power. float?'''
        if value == None: return self.keywords['LFC_EDFA27_P']
        else:
            print('Writing value', value, 'to LFC_EDFA27_P')
            return 0
    
    def LFC_EDFA27_ONOFF(self, value=None):
        '''Small EDFA (500 mW) 1 emission on/off. boolean'''
        if value == None: return self.keywords['LFC_EDFA27_ONOFF']
        else:
            print('Writing value', value, 'to LFC_EDFA27_ONOFF')
            return 0

    def LFC_EDFA13_P(self, value=None):
        '''Small EDFA (20 mW) 2 output power. float?'''
        if value == None: return self.keywords['LFC_EDFA13_P']
        else:
            print('Writing value', value, 'to LFC_EDFA13_P')
            return 0
    
    def LFC_EDFA13_ONOFF(self, value=None):
        '''Small EDFA (20 mW) 2 emission on/off. boolean'''
        if value == None: return self.keywords['LFC_EDFA13_ONOFF']
        else:
            print('Writing value', value, 'to LFC_EDFA13_ONOFF')
            return 0

    def LFC_EDFA23_P(self, value=None):
        '''Small EDFA (200 mW) 3 output power. float'''
        if value == None: return self.keywords['LFC_EDFA23_P']
        else:
            print('Writing value', value, 'to LFC_EDFA23_P')
            return 0

    def LFC_EDFA23_ONOFF(self, value=None):
        '''Small EDFA (200 mW) 3 emission on/off. boolean'''
        if value == None: return self.keywords['LFC_EDFA23_ONOFF']
        else:
            print('Writing value', value, 'to LFC_EDFA23_ONOFF')
            return 0

    def LFC_RFAMP_I(self, value=None):
        '''RF Amp current. float?'''
        return #return value. this keyword is read-only
    
    def LFC_RFAMP_V(self, value=None):
        '''RF Amp voltage. float?'''
        if value is not None:
            pass
        return
    
    def LFC_RFOSCI_I(self, value=None):
        '''RF Oscillator input current. float'''
        return #return value. this keyword is read-only
    
    def LFC_RFOSCI_V(self, value=None):
        '''RF Oscillator input voltage. float?'''
        if value is not None:
            pass
        return
    
    def LFC_IM_BIAS(self, value=None):
        '''Mini-comb amplitude lock offset bias. float'''
        if value is not None:
            pass
        return
    
    def LFC_IM_RF_ATT(self, value=None):
        '''Mini-comb RF voltage controlled variable attenuation setting'''
        if value is not None:
            pass
        return
    
    def LFC_WSP_PHASE(self, value=None):
        '''Waveshaper Dispersion Compensation. float array (2,N)'''
        if value is not None:
            pass
        return

    def LFC_WSP_ATTEN(self, value=None):
        if value is not None:
            pass
        return

    def LFC_PTAMP_PRE_P(self, value=None):
        '''High-power EDFA pre-amp output power'''
        return

    def LFC_PTAMP_OUT(self, value=None):
        '''High-power EDFA output power'''
        return

    def LFC_PTAMP_I(self, value=None):
        '''High-power EDFA pump current'''
        if value is not None:
            pass
        return

    def LFC_PTAMP_ONOFF(self, value=None):
        '''High-power EDFA emission on/standby. boolean'''
        if value is not None:
            pass
        return
    
    def LFC_PTAMP_LATCH(self, value=None):
        '''RESET preamp and pwramp latching circuits'''
        if value is not None:
            pass
        return

    def LFC_WGD_T(self, value=None):
        '''Waveguide TEC control. float'''
        if value is not None:
            pass
        return

    def LFC_PPLN_T(self, value=None):
        '''PPLN TEC control. float'''
        if value is not None:
            pass
        return      
    
