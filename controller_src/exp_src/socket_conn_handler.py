#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

from threading import Thread


class ConnListener(Thread):
    def __init__(self, name: str, conn):
        Thread.__init__(self)
        self.name = name
        self.conn = conn

    def run(self):
        print('Connected', self.name)
        while True:
            data = self.conn.recv(4096)
            if data:
                self.process_data(data)
            else:
                break
        self.conn.close()

    def process_data(self, data):
        print('Need a child function to process data')
        return


class ConnSender(Thread):
    def __init__(self, name: str, conn):
        Thread.__init__(self)
        self.name = name
        self.conn = conn

    def run(self):
        print('Connected', self.name)
        self.do_sending()

    def do_sending(self):
        print('Need a child function to send data')
        return

    def send(self, str_of_ANY_msg: str):
        ret = self.conn.send(str_of_ANY_msg)
        if (not ret):
            print('connection erro', self.conn)
            self.conn.close()
        return ret
