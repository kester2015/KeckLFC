import time, threading
import xml.etree.ElementTree as ET

VERBOSE = False

def parse_xml(xmlfile):
    '''Parse KTL xml file'''
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
    ''' just a test function '''
    while True:
        mkl.keywords['ICESTRING'] = time.strftime('%H:%M:%S')
        time.sleep(1)
        if stop(): 
            mkl.clock = None
            break
            
class mockKeckLFC(object):

    def __init__(self):

        keyword_names, keyword_types = parse_xml('/kroot/src/kss/nirspec/nsmine/ktlxml/ICEkeywords.xml.sin')
        
        self.keywords = {keyword: None for keyword in keyword_names}
        self.types = {keyword: keyword_type for keyword, keyword_type in zip(keyword_names, keyword_types)}

        func_dict = {}
        for keyword in self.keywords:
            method_name = f'{keyword}'
            method = getattr(self, method_name)
            func_dict[keyword] = method
        
        self.funcs = func_dict

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
        elif typ == 'enumerated': return int(val)
        elif typ == 'string': return str(val)
        elif typ == 'boolean': 
            if val in ['True', '1', 1, True] : return True
            else: return False
        else:
            print('Unrecognized type')
            raise Exception
    
    def ICEINT(self, value=None):
        
        if VERBOSE: print('iceint func called')
        if value is None: return self.keywords['ICEINT']
        else:
            print('Writing value', value, 'to iceint')
            return 0
    
    def ICEENUM(self, value=None):
        
        if VERBOSE: print('iceenum func called')
        if value == None: return self.keywords['ICEENUM']
        else:
            print('Writing value', value, 'to iceenum')
            return 0
            
    def ICEBOOL(self, value=None):
        
        if VERBOSE: print('icebool func called')
        if value == None: return self.keywords['ICEBOOL']
        
        else:
            print('ICEBOOL value: ', value)
            print('Writing value', value, 'to icebool')
            if value == True: self.start_clock()
            elif value == False: self.stop_clock()
            else: 
                print('something wrong with icebool')
                return 1
            return 0
    
    def ICESTRING(self, value=None):
        
        if VERBOSE: print('icestring func called')
        if value == None: return self.keywords['ICESTRING']
        
        else:
            print('Writing value', value, 'to icestring')
            return 0

    def ICESTA(self, value=None):
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
        
    
        
    
