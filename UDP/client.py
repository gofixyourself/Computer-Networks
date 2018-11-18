import socket
import argparse

our_socket = socket.socket()
host = '127.0.0.1'
port = 12345

parser = argparse.ArgumentParser(description='Send files over TCP')
parser.add_argument('filename', metavar='filename', type=str,
                    help='a file to send')

our_socket.connect((host, port))
args = parser.parse_args()
with open(args.filename, 'rb') as input_file:
    line = 1
    while line:
        line = input_file.read(1024)
        print('Sending...')
        our_socket.send(line)
    input_file.close()
    our_socket.close()
exit()