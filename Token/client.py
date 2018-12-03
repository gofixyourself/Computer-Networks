import socket
import time

host = "127.0.0.1"
port = 22822
MESSAGE = "tcp_client: Enter message / Enter exit:"

tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_client.connect((host, port))

while MESSAGE != 'exit':
    time.sleep(0.5)
    tcp_client.send(input().encode())

tcp_client.close()
