import socket

import utils

HEADER_MSG_SIZE = 10

class MySocket:

    def __init__(self, sock=None, port=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.port = port
        else:
            self.sock = sock

        print "Created socket"

    def __del__(self):
        pass

    def listen(self, port=None):
        if port is None:
            self.sock.bind(('', self.port))
            self.sock.listen(1)
        else:
            self.port = port
            self.sock.bind(('', port))

        print "Listening on port {}".format(self.port)

    def connect(self, host, port=None):
        if port is None:
            self.sock.connect((host, self.port))
        else:
            self.port = port
            self.sock.connect((host, port))

        print "Connnecting to {} on port {}".format(host, self.port)

    def close(self):
        print "Closing socket"
        self.sock.close()

    def accept(self):
        return self.sock.accept()

    def accept_connections(self, func):
        func(self)


    def send_header(self, code, data, sock):
        msg = str(code) + '|' + str(data)
    	while len(msg) < HEADER_MSG_SIZE:
    		msg = msg + '|'

        print "Sending a header with data: {}".format(msg)
    	self.send(msg, sock=sock)

    def recv_header(self, sock):
        data = self.recv(HEADER_MSG_SIZE, sock=sock)
        data_spl = data.split('|')

        print "Received a header with data: {}".format(data)
        return (data_spl[0], data_spl[1])

    def send(self, data, sock=None):
        if sock is None:
            print "Sending data: {}".format(data)
            utils.send_all(self.sock, data)
        else:
            print "Sending data: {}".format(data)
            utils.send_all(sock, data)

    def recv(self, num_bytes, sock=None):
        print "Waiting to receive", num_bytes, "bytes"
        if sock is None:
            data = utils.get_all(self.sock, num_bytes)
            print "Received data: {}".format(data)
            return data
        else:
            data = utils.get_all(sock, num_bytes)
            print "Received data: {}".format(data)
            return data
