import socketserver
from numpy import base_repr


class Converter:
    def __init__(self, filename):
        self.ip_list = open(filename, 'r').read()
        self.ip_list = self.ip_list.split("\n")

    def present(self, id):
        return self.ip_list[id]

    @staticmethod
    def convert(ip):
        ip = ip.split(".")
        binary = f"{base_repr(int(ip[0]), 2)}.{base_repr(int(ip[1]), 2)}" \
                 f".{base_repr(int(ip[2]), 2)}.{base_repr(int(ip[3]), 2)}"

        hexadecimal = f"{base_repr(int(ip[0]), 16)}.{base_repr(int(ip[1]), 16)}" \
                 f".{base_repr(int(ip[2]), 16)}.{base_repr(int(ip[3]), 16)}"

        octadecimal = f"{base_repr(int(ip[0]), 8)}.{base_repr(int(ip[1]), 8)}" \
                 f".{base_repr(int(ip[2]), 8)}.{base_repr(int(ip[3]), 8)}"
        return {
            "bin": binary,
            "hex": hexadecimal,
            "oct": octadecimal
        }


host = '0.0.0.0'
port = 8800
address = (host, port)
ip_converter = Converter("ip.list")


class MyTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        self.data = self.request.recv(512)
        print('client send: ' + str(self.data))
        ip = ip_converter.present(int(self.data))
        response = ip_converter.convert(ip)

        message = f"{response['bin']}\n{response['hex']}\n{response['oct']}".encode("ascii")
        self.request.sendall(message)


if __name__ == "__main__":
    server = socketserver.TCPServer(address, MyTCPHandler)

    print('Starting server...')
    server.serve_forever()
