# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************

import socket
import sys
import os
import subprocess as sp

# Custom module
import commands
import utils
import mySocket as ms

def handle_connection(sock, client_sock, addr):
	print "handling connection"
	while True:

		try:
			conn_header = sock.recv_header(sock=client_sock)
		except Exception as e:
			print e
			print "connection closed"
			break
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


def listen_for_connection(sock):
	client_id = 0
	while True:
		print "Waiting for connections..."

		# Accept connections
		client_sock, addr = sock.accept()


		print "Accepted connection from client {2}: {0}:{1}"\
			.format(addr[0], addr[1], client_id)
		print ""

		# handle_connection(sock, client_sock, addr)

		child_pid = os.fork()
		if child_pid == 0:
			print("Forking client {} now".format(client_id))
			handle_connection(sock, client_sock, addr)
			break
		else:
			client_id += 1


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
