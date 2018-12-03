import socket
from threading import Thread
import random
import string

LEN = 40
TIMEOUT = 60


class TokenQueue:
    def __init__(self, quantity):
        self.queue = []
        self.n = quantity
        self.freen = quantity

    def gen_tokens(self):
        while len(self.queue) < self.n:
            self.queue.append(''.join(random.choices(string.hexdigits, k=10)))

    def take_token(self):
        if self.freen > 0:
            self.freen -= 1
            return self.queue.pop(random.randint(0, len(self.queue)-1))
        else:
            return None

    def return_token(self, token):
        if self.freen < self.n:
            self.queue.append(token)
            self.freen += 1


class ClientThread(Thread):
    def __init__(self, ip, port, token, tokens):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.token = token
        self.tokens = tokens
        print("[+] New server socket thread started for " + ip + ":" + str(port) + " " + self.token)

    def run(self):
        while True:
            try:
                data = connection.recv(2048)
                if data != b'':
                    print("Server received data: ", data)
            except socket.timeout:
                tokens.return_token(self.token)
                connection.close()
                print(f"Disconnected {self.token}")
                return 0
            except OSError:
                pass


TCP_IP = '0.0.0.0'
TCP_PORT = 22822

tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_server.bind((TCP_IP, TCP_PORT))
threads = []

tokens = TokenQueue(LEN)
tokens.gen_tokens()

while True:
    tcp_server.listen(LEN)
    (connection, (ip, port)) = tcp_server.accept()
    connection.settimeout(TIMEOUT)
    token = tokens.take_token()
    if token != None:
        new_thread = ClientThread(ip, port, token, tokens)
        new_thread.start()
        threads.append(new_thread)
