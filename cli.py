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

import commands
import utils

@contextmanager
def create_data_port(port):
    e_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    e_socket.bind(('',port))
    yield e_socket
    e_socket.close()

def send_header(sock, cmd, size):
	msg = cmd + str(size)
	while len(msg) < 10:
		msg = msg + ' '

	utils.send_all(sock, msg)

def receive_header(sock):
	return int(utils.get_all(sock, 10))

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

	# Create a TCP socket
	conn_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		# Connect to the server
		conn_sock.connect((server_addr__real, server_port))
	except Exception as e:
		print "Connection refused, the server may be down. Try again later."
		return

	msg = 'user pass1'
	utils.send_all(conn_sock, msg)


	while 1:
		input = raw_input("ftp> ")
		input_arr = input.split()

		if(input_arr[0] == 'quit'):
			print "Closing connection"
			conn_sock.close()
			return
		elif(input_arr[0] == 'get'):


			commands.do_get(conn_sock, 10)
		elif(input_arr[0] == 'put'):
			if(len(input_arr) == 1):
				print 'Invalid command. Type \'help\' for a list of commandts'
				continue
			try:
				size = os.path.getsize(input_arr[1])

				send_header(conn_sock, 'put', str(size))
				ep_port = receive_header(conn_sock)

				with create_data_port(ep_port) as ep_sock:
					commands.do_put(ep_sock, input_arr[1])

			except Exception as e:
				print e
				print 'Invalid file'
		elif(input_arr[0] == 'ls'):
			commands.do_ls()
		elif(input_arr[0] == 'lls'):
			commands.do_lls()
		elif(input_arr[0] == 'help'):
			commands.do_help()

	conn_sock.close()

	# # The number of bytes sent
	# numSent = 0
	#
	# # The file data
	# fileData = None
	#
	# # Keep sending until all is sent
	# while True:
	#
	# 	# Read 65536 bytes of data
	# 	fileData = fileObj.read(65536)
	#
	# 	# Make sure we did not hit EOF
	# 	if fileData:
	#
	#
	# 		# Get the size of the data read
	# 		# and convert it to string
	# 		dataSizeStr = str(len(fileData))
	#
	# 		# Prepend 0's to the size string
	# 		# until the size is 10 bytes
	# 		while len(dataSizeStr) < 10:
	# 			dataSizeStr = "0" + dataSizeStr
	#
	#
	# 		# Prepend the size of the data to the
	# 		# file data.
	# 		fileData = dataSizeStr + fileData
	#
	# 		# The number of bytes sent
	# 		numSent = 0
	#
	# 		# Send the data!
	# 		while len(fileData) > numSent:
	# 			numSent += connSock.send(fileData[numSent:])
	#
	# 	# The file has been read. We are done
	# 	else:
	# 		break
	#
	#
	# print "Sent ", numSent, " bytes."
	#
	# # Close the socket and the file
	# connSock.close()
	# fileObj.close()

if __name__ == '__main__':
    main()
