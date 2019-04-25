import select
import socket
import threading
import sys
from time import sleep


class fileServer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        # 소켓생성
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 바인드
        self.server.bind(('0.0.0.0', 0))
        # 리슨, 여기까지는 기본적인 서버 소켓 세팅
        self.server.listen()
        # select 함수에서 관찰될 소켓 리스트 설정
        self.input_list = [self.server]
        self.connectionList = []
        self.stopFlag = False
        print(self.server.getsockname())

    def getPort(self):
        return self.server.getsockname()[1]

    def stop(self):
        for ir in self.input_list:
            if ir != self.server:
                ir.close()
        self.server.close()
        self.stopFlag = True

    def run(self):
        while not self.stopFlag:
            # select 함수는 관찰될 read, write, except 리스트가 인수로 들어가며
            # 응답받은 read, write, except 리스트가 반환된다.
            # input_list 내에 있는 소켓들에 데이터가 들어오는지 감시한다.
            # 다르게 말하면 input_list 내에 읽을 준비가 된 소켓이 있는지 감시한다.
            input_ready, __, _ = select.select(
                self.input_list, [], [])

            # 응답받은 read 리스트 처리
            for ir in input_ready:
                # 클라이언트가 접속했으면 처리함
                if ir == self.server:
                    client, address = self.server.accept()
                    index = 0
                    if any(address in s for s in self.connectionList):
                        index = self.connectionList.index(address)
                    else:
                        index = len(self.connectionList)
                        self.connectionList.append(address)
                    print("[INFO] PEER " + str(index) + " Connected")

                    # input_list에 추가함으로써 데이터가 들어오는 것을 감시함
                    self.input_list.append(client)

                # 클라이언트소켓에 데이터가 들어왔으면
                else:
                    data = ir.recv(1024)
                    if data:
                        print(''.join(map(str, ir.getpeername())) + 'SEND :' + str(data), flush=True)
                        ir.send(data)
                    # 데이터가 없는경우, 즉 클라이언트에서 소켓을 close 한경우
                    else:
                        print(''.join(map(str, ir.getpeername())) + 'CLOSE', flush=True)
                        ir.close()
                        # 리스트에서 제거
                        self.input_list.remove(ir)
        self.server.close()

# 참고 :  https: //scienceofdata.tistory.com/entry/Python-select-함수를-이용한-간단한-에코-서버클라이언트-예제
