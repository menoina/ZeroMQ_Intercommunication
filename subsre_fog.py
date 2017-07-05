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

    # - 受信するやつ - 
    def run(self):
        ch = "1"
        socket_receive = context.socket(zmq.SUB)
        socket_receive.bind("tcp://*:5556")
        # ch 1 で受信
        socket_receive.setsockopt_string(zmq.SUBSCRIBE,ch)
        while True:
            string = socket_receive.recv_string()
            ch,data = string.split()
            print("Ch {0} -> {1} reveived".format(ch,data))


if __name__ == '__main__':

    context = zmq.Context()    

    # サブスレッド稼働
    th_cl = TestThread(5, 5)
    th_cl.start()

    time.sleep(1)

    print (" === start main thread (main) === ")

    socket_send = context.socket(zmq.PUB)
    socket_send.connect("tcp://192.168.2.171:5557")
    i = 0
    while True:
        i += 1 
        for ch in range(1,3):
            number = ch * i
            socket_send.send_string("{0} {1}".format(ch,number))
            print("Ch {0} <- {1} sent".format(ch,number))
        time.sleep(1)

        
