# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************

import socket
import sys
from contextlib import contextmanager

# Custom module
import commands
import utils

# The size of the message
HEADER_MSG_SIZE = 10

# Availabble commands
COMMANDS = {
    "get" : commands.do_put,
    "put" : commands.do_get,
    "ls"  : commands.do_ls
}

def authenticate(usr, pwd):

    # TODO authenticate user
    print "authenticated"
    return True

@contextmanager
def create_data_port():
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

        print "command header", cmd_header

        cmd, size = cmd_header.split()

        with create_data_port as ep_sock:
            if(cmd == 'put'):
                data = commands.do_get(ep_sock, size)
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

    # Accept connections forever
    while True:

        print "Waiting for connections..."

    	# Accept connections
    	client_sock, addr = sock.accept()


    	print "Accepted connection from client: {0} {1}"\
            .format(addr[0], addr[1])
    	print "\n"

    	# The buffer to all data received from the
    	# the client.
    	conn_data = ""

    	# The temporary buffer to store the received
    	# data.
    	recv_buff = ""

    	# The buffer containing the file size
    	conn_header = ""

    	# Receive the first 10 bytes indicating the
    	# size of the file
    	conn_header = utils.get_all(client_sock, HEADER_MSG_SIZE)

        print "connection header: ",conn_header

        usr, pwd = conn_header.split()

        if not authenticate(usr, pwd):
            return

        listen_for_command((addr, client_sock))

        # # Get the file size
    	# data_size = int(data_sizeBuff)
        #
    	# print "The file size is ", data_size
        #
    	# # Get the file data
    	# conn_data = get_all(client_sock, data_size)
        #
    	# print "The file data is: "
    	# print conn_data

    	# Close our side
    	client_sock.close()

def main():

    # Command line checks
    if len(sys.argv) != 2 :
    	print "USAGE: python {} <PORT NUMBER>".format(sys.argv[0])
        return

    # TODO check valid and non reserved port number

    # The port on which to listen
    listen_port = int(sys.argv[1])

    # Create a server socket.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Bind the socket to the port
        server_socket.bind(('', listen_port))
    except Exception as e:
        print e
        server_socket.close()

    # Start listening on the socket
    server_socket.listen(1)
    print "Listening on port {}".format(listen_port)

    # try:
    #     listen_for_connection(server_socket)
    # except Exception as e:
    #     print e
    #     server_socket.close()

    listen_for_connection(server_socket)

if __name__ == '__main__':
    main()
