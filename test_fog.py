import threading
import time
import datetime
import sys
import zmq
import time

class TestThread(threading.Thread):

    """docstring for TestThread"""

    def __init__(self, n, t):
        super(TestThread, self).__init__()
        self.n = n
        self.t = t

    # - 送信するやつ - 
    def run(self):
        context = zmq.Context()
        socket_send = context.socket(zmq.PUB)
        socket_send.connect("tcp://192.168.2.171:5557")
        i=0
        while True:
            i += 1
            for ch in range(1,3):
                number = str(ch * i)
                socket_send.send_string("{0} {1}".format(ch,number))
                print("CH {0} <- {1} sent".format(ch,number))            
            time.sleep(3)

# 受信を書く
if __name__ == '__main__':
    ch = "1"
    context = zmq.Context()    

    # サブスレッド稼働
    th_cl = TestThread(5, 5)
    th_cl.start()

    time.sleep(1)

    print (" === start main thread (main) === ")

    socket_receive = context.socket(zmq.SUB)
    socket_receive.bind("tcp://*:5556")
    socket_receive.setsockopt_string(zmq.SUBSCRIBE,ch)
    while True:
        string = socket_receive.recv_string()
        data = string.split()
        print("RECEIVE!!! Ch {0} -> {1}received".format(ch,data))

        
