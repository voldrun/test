import socket, threading, string

debug = True

_connector = None
_running = True

_host = '0.0.0.0'
_port = 2222
_maxClient = 10
_recvBuffer = 2000

def printd (aString):
    if debug:
        print aString

class talkToClient (threading.Thread):
    def __init__(self, clientSock, addr):
        self.clientSock = clientSock
        self.addr = addr
        threading.Thread.__init__(self)
    def run (self):
        while True:
            recvData = self.clientSock.recv (_recvBuffer)
            if not recvData:
                self.clientSock.send ('bye')
                break
            printd('Client ' + str (self.addr) + ' say "' + str (recvData) + '"')
            self.clientSock.send (recvData)
            if recvData == "exit":
                break
        self.clientSock.close ()

_connector = socket.socket (socket.AF_INET, socket.SOCK_STREAM)
_connector.bind ((str(_host), int(_port)))
_connector.listen (int(_maxClient))

while _running:
    printd ('Running on ' + _host + ':' + str (_port) + '.')
    channel, details = _connector.accept ()
    printd ('Connect on : ' + str (details))
    talkToClient (channel, details).start ()
