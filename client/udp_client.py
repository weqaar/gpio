import socket
import sys

HOST, PORT = "192.168.66.10", 9999
data = " ".join(sys.argv[1:])
server_list = ['mysql', 'queue', 'video', 'webservice']
signal_list = ['off', 'on']

if (len(sys.argv) != 3):
	sys.stderr.write("usage: " + sys.argv[0] + " <SERVER NAME> <OFF|ON>" + "\n")
	sys.exit(1)

if sys.argv[1] not in server_list:
	print "Server: " + sys.argv[1] + " is invalid. Valid list of servers: " + "\n"
	for i in server_list:
		print "* " + i
	print "\n".strip("\n")
	sys.exit(1)

if sys.argv[2] not in signal_list:
	print "Signal: " + sys.argv[2] + " is invalid. Valid list of signals: " + "\n"
	for i in signal_list:
		print "* " + i
	print "\n".strip("\n")
	sys.exit(1)


#print "usage: udp_client <SERVER NAME> <OFF|ON> \n"

# Create a socket (SOCK_DGRAM means a UDP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # Connect to server and send data
    #sock.connect((HOST, PORT))
    sock.sendto(data, (HOST, PORT))

    # Receive data from the server and shut down
    #received = sock.recv(1024)
finally:
    sock.close()

#print "Sent:     {}".format(data)
#print "Received: {}".format(received)
