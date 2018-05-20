# *******************************************************************
# This file illustrates how to send a file using an
# application-level protocol where the first 10 bytes
# of the message from client to server contain the file
# size and the rest contain the file data.
# *******************************************************************
import socket
import os
import sys
from contextlib import contextmanager
import traceback

import mySocket as ms
import commands
import utils

@contextmanager
def create_data_port(addr, port):
	e_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	e_socket.connect((addr,port))
	yield e_socket
	e_socket.close()

def send_header(sock, cmd, size):
	msg = cmd + '|' + str(size)
	while len(msg) < 10:
		msg = msg + '|'
	print "Sending header:", msg, "to", sock.getsockname()[1]
	utils.send_all(sock, msg)

def receive_header(sock):
	data = utils.get_all(sock, 10)
	data_spl = data.split('|')
	return (data_spl[0], data_spl[1])

def main():

	# Command line checks
	if len(sys.argv) < 3:
		print "USAGE: python {} <server machine> <server port>".format(sys.argv[0])
		# print "USAGE python " + sys.argv[0] + " <FILE NAME>"
		return

	# Server address
	server_addr = sys.argv[1] # "localhost"
	server_addr__real = socket.gethostbyname(server_addr)

	# Server port
	server_port = int(sys.argv[2]) # 1234

	cli_sock = ms.MySocket()
	cli_sock.connect(server_addr__real, server_port)

	while 1:
		input = raw_input("ftp> ")
		input_arr = input.split()

		if(input_arr[0] == 'quit'):
			print "Closing connection"
			cli_sock.close()
			return
		elif(input_arr[0] == 'get'):
			cli_sock.send_header('get', len(input_arr[1]), sock=cli_sock.sock)
			port_header = cli_sock.recv_header(cli_sock)
			print 'Header receieved', port_header
			ep_port = -1
			if (port_header[0] == 'prt'):
				ep_port = int(port_header[1])

			ep_sock = ms.MySocket()
			ep_sock.connect(server_addr__real, ep_port)
			ep_sock.send(input_arr[1], sock=ep_sock.sock)
			data_header = cli_sock.recv_header(sock=ep_sock.sock)
			print 'Header receieved', data_header
			data = ep_sock.recv(int(data_header[1]), sock=ep_sock.sock)
			file = open('cli' + input_arr[1], "w")
			file.write(data)
			file.close()
			ep_sock.close()

		elif(input_arr[0] == 'put'):
			if(len(input_arr) == 1):
				print 'Invalid command. Type \'help\' for a list of commandts'
				continue

			size = os.path.getsize(input_arr[1])

			cli_sock.send_header('put', len(input_arr[1]) + size + 1, sock=cli_sock.sock)
			data = cli_sock.recv_header(cli_sock)
			print 'Header receieved', data
			ep_port = -1
			if (data[0] == 'prt'):
				ep_port = int(data[1])

			ep_sock = ms.MySocket()
			ep_sock.connect(server_addr__real, ep_port)
			file = open(input_arr[1], "r")
			data = file.read()
			file.close()
			ep_sock.send(input_arr[1] + '|' + data, sock=ep_sock.sock)
			# commands.do_put(ep_sock.sock, input_arr[1])
			ep_sock.close()

		elif(input_arr[0] == 'ls'):
			commands.do_ls()
		elif(input_arr[0] == 'lls'):
			cli_sock.send_header('lls', -1, sock=cli_sock.sock)
			port_header = cli_sock.recv_header(cli_sock)
			print 'Header receieved', port_header
			ep_port = -1
			if (port_header[0] == 'prt'):
				ep_port = int(port_header[1])

			ep_sock = ms.MySocket()
			ep_sock.connect(server_addr__real, ep_port)
			data_header = cli_sock.recv_header(sock=ep_sock.sock)
			print 'Header receieved', data_header
			data = ep_sock.recv(int(data_header[1]), sock=ep_sock.sock)
			print data
			ep_sock.close()
		elif(input_arr[0] == 'help'):
			commands.do_help()

	conn_sock.close()



if __name__ == '__main__':
	main()
