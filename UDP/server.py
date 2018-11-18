import socket

our_socket = socket.socket()
host = '0.0.0.0'
port = 12345
our_socket.bind((host, port))
save_received_data = open('received.bin', 'wb')
our_socket.listen(5)
while True:
    data, address = our_socket.accept()
    print('Got connection from', address)
    total_length = data.recv(1024)
    while (total_length):
        print("Receiving...")
        save_received_data.write(total_length)
        total_length = data.recv(1024)
    save_received_data.close()
    print("Done Receiving")
    data.close()
    exit()
