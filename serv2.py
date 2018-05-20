# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************

import socket
import sys
import os
from contextlib import contextmanager
import traceback
import subprocess as sp

# Custom module
import commands
import utils
import mySocket as ms


@contextmanager
def create_data_port(addr):
    e_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    e_socket.bind(('',0))
    # port = e_socket.getsockname()[1]
    # yield port
    print 'created an ep sock {}'.format(e_socket.getsockname()[1])
    yield e_socket
    e_socket.close()

def listen_for_command(client):

    # Accept connections forever
    while True:
        print "wating for command from ", client
    	# The buffer to all data received from the
    	# the client.
    	file_data = ""

    	# The temporary buffer to store the received
    	# data.
    	recv_buff = ""

    	# The buffer containing the file size
    	cmd_header = ""

    	# Receive the first 10 bytes indicating the
    	# size of the file
    	cmd_header = utils.get_all(client[1], HEADER_MSG_SIZE)

        cmd, size = cmd_header.split()

        with create_data_port(client[0]) as ep_sock:
            send_header(client[1], '', ep_sock.getsockname()[1])
            if(cmd == 'put'):
                data = commands.do_get(ep_sock, int(size))
                print 'received', data


        # # Get the file size
    	# file_size = int(file_sizeBuff)
        #
    	# print "The file size is ", file_size
        #
    	# # Get the file data
    	# file_data = get_all(client_sock, file_size)
        #
    	# print "The file data is: "
    	# print conn_data

	# Close our side
	client[1].close()




def listen_for_connection(sock):
    print "Waiting for connections..."

    # Accept connections
    client_sock, addr = sock.accept()


    print "Accepted connection from client: {0}:{1}"\
        .format(addr[0], addr[1])
    print ""

    while True:

    	conn_header = sock.recv_header(sock=client_sock)
        ep_socket = ms.MySocket(port=0)
        ep_socket.listen()

        print "connection header:", conn_header
        sock.send_header('prt', ep_socket.sock.getsockname()[1], sock=client_sock)
        ep_sock, ep_addr = ep_socket.accept()

        if conn_header[0] == 'put':
            data = ep_socket.recv(int(conn_header[1]), sock=ep_sock)
            print "this is the data", data
            data_spl = data.split('|')
            file = open('serv' + data_spl[0], "w")
            file.write(data_spl[1])
            file.close()
            ep_socket.close()

        elif conn_header[0] == 'get':
            filename = ep_socket.recv(int(conn_header[1]), sock=ep_sock)
            print "this is the filename", filename
            size = os.path.getsize(filename)
            ep_socket.send_header('rgt', size, sock=ep_sock)

            file = open(filename, 'r')
            data = file.read()
            file.close()

            ep_socket.send(data, sock=ep_sock)
            ep_socket.close()

        elif conn_header[0] == 'lls':
            data = sp.check_output('ls')
            ep_socket.send_header('rls', len(data), sock=ep_sock)

            ep_socket.send(data, sock=ep_sock)
            ep_socket.close()


def main():

    # Command line checks
    if len(sys.argv) != 2 :
    	print "USAGE: python {} <PORT NUMBER>".format(sys.argv[0])
        return

    # TODO check valid and non reserved port number

    # The port on which to listen
    listen_port = int(sys.argv[1])

    server_socket = ms.MySocket(port=listen_port)

    server_socket.listen()
    server_socket.accept_connections(listen_for_connection)
    server_socket.close()
    # listen_for_connection(server_socket)

if __name__ == '__main__':
    main()
