import signal, sys, time, Ice

Ice.loadSlice('KtlIce.ice')
import Demo

sys.path.append('../')

use_mock = True

#import random, threading
if not use_mock:
    from KeckLFC import *
else:
    from mockKeckLFC import *


class LfcI(Demo.Lfc):

    def __init__(self):

        #== List of the KTL keywords that should be monitored
        #self.keyword_names = ['ICEINT','ICEBOOL','ICEENUM','ICESTRING', 'ICESTA']
        keyword_names, keyword_types = parse_xml('LFC.xml.sin')
        self.keyword_names = keyword_names

        #== Define mockKeckLFC class object as mkl
        if use_mock:
            self.mkl = mockKeckLFC()
        else:
            self.mkl = KeckLFC()

        print('ICE server starts ...\n')

        #self.ncalls = 0

    def modifiedkeyword(self, name, value, current):
        ''' This function is used by the dispatcher. 
        KTL dispatcher communicates with ICE when keyword value is changed. '''

        self.mkl[name] = value
        #self.mkl.__setitem__(name, value) # = value
        print(' Keyword <%s> changed to %s' % (name, value))

    def receive(self, name, current):
        ''' This function is used by the dispatcher.
        Sends the keyword values stored in KeckLFC class to the dispatcher'''

        val = self.mkl[name]
        return str(val)  #self.mkl.__getitem__(name) #str(self.mkl.keywords[name]) #self.ncalls

    def keylist(self, current):
        ''' This function is used by the dispatcher '''
        return self.keyword_names

    def shutdown(self, current):
        self.mkl.stop_clock()
        current.adapter.getCommunicator().shutdown()


with Ice.initialize(sys.argv, 'config.server') as communicator:
    signal.signal(signal.SIGINT, lambda signum, frame: communicator.shutdown())

    #
    # The communicator initialization removes all Ice-related arguments from argv
    #
    if len(sys.argv) > 1:
        print(sys.argv[0] + ": too many arguments")
        sys.exit(1)

    adapter = communicator.createObjectAdapter("Lfc")
    adapter.add(LfcI(), Ice.stringToIdentity("lfc"))
    adapter.activate()
    communicator.waitForShutdown()
