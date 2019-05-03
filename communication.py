import socket
import threading

class Communcation(threading.Thread):
    def __init__(self, sck : socket.socket, debug = False):
        threading.Thread.__init__(self)
        self.socket = sck
        self.debug = debug
        
    def __recvall(self, count : int) -> bytearray:
        buf = b''
        while count:
            newbuf = self.socket.recv(count)
            if not newbuf: 
                return None
            buf += newbuf
            count -= len(newbuf)
        return buf
    
    def recv_json(self) -> bytearray:
        while True:
            lenght = int(self.__recvall(128))
            if lenght > 0 :
                data = self.__recvall(lenght)
                if self.debug:
                    print("[RECV] LENGTH : " + str(lenght))
                #print("[RECV] DATA : " + data)
                return data
    
    def send_json(self, txt : bytearray):
        lengthTxt = '{:0128d}'.format(len(txt))
        if self.debug:
            print("[SEND] LENGTH : " + str(len(txt)))
            print("[SEND] LENGTH HEADER : " + lengthTxt)
            print("[SEND] TXT : " + txt)
        
        self.socket.sendall(bytearray(lengthTxt))
        self.socket.sendall(txt)
        
    def close(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()
        
    def run(self):
        pass