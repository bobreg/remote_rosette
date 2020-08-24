import socket
import threading
import re
import time


# r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$' - определение правильной формы ip адреса
# ^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$ - выделение всех сегментов цифр ip адреса


class udp:
    def __init__(self):
        self.my_ip = socket.gethostbyname(socket.gethostname())
        self.udp_s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.port = 8888
        self.udp_s.bind(('', self.port))
        self.ip = '192.168.0.1'
        self.flag_thread = True
        self.data = b''
        self.listen_thread = threading.Thread(target=self.listen_socket)
        self.listen_thread.start()

    def send_comm(self, comm):
        self.udp_s.sendto(comm.encode('utf-8'), (self.ip, self.port))
        # print(comm)

    def listen_socket(self):
        # нельзя создать два сокета на один порт
        # print('start thread')
        while self.flag_thread is True:
            try:
                self.data = self.udp_s.recv(1024)
                # print(self.data.decode('utf-8'))
            except OSError:
                pass
        # print('bye')

    def find_rosette(self, ip):
        with open('adress.txt', 'w') as ip_file:
            ip_file.write(ip + '\n')
        pattern = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'
        matches = re.findall(pattern, ip)
        print(matches[0])
        segment_ip_1 = matches[0][0]
        segment_ip_2 = matches[0][1]
        segment_ip_3 = matches[0][2]
        for i in range(1, 255):
            ip = segment_ip_1 + '.' + segment_ip_2 + '.' + segment_ip_3 + '.' + str(i)
            self.udp_s.sendto(b'ping', (ip, self.port))
            time.sleep(0.05)
            print(ip)
            if self.data == b'ping!':
                self.data = b''
                print(ip)
                self.ip = segment_ip_1 + '.' + segment_ip_2 + '.' + segment_ip_3 + '.' + str(i)
                return True





