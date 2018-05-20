# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param num_bytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
def get_all(sock, num_bytes):

	# The buffer
	recv_buff = ""

	# The temporary buffer
	tmp_buff = ""

	# Keep receiving till all is received
	while len(recv_buff) < num_bytes:

		# Attempt to receive bytes
		tmp_buff =  sock.recv(num_bytes)

		# The other side has closed the socket
		if not tmp_buff:
			break

		# Add the received bytes to the buffer
		recv_buff += tmp_buff

	print "received data:", recv_buff
	return recv_buff

def send_all(sock, data):
	print sock.getsockname()[1]
	print 'sending data', data

	# The number of bytes sent
	numSent = 0

	# The number of bytes sent
	numSent = 0

	# Send the data!
	while len(data) > numSent:
		numSent += sock.send(data[numSent:])

	print 'data sent successfully'
