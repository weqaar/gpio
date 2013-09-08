import SocketServer
import os
import multiprocessing
from ruptime_host_queue import *

class _UDPHandler(SocketServer.BaseRequestHandler):

	def handle(self):
	        data = self.request[0].strip()
		socket = self.request[1]
		udp_queue.get_lock()
		udp_queue.put(data)
		udp_queue.release_lock()
		print 'Received: ' + data


def start_server(server_ip, server_port):
	global udp_queue
        udp_queue = ruptime_host_queue()
    	HOST, PORT = server_ip, int(server_port)
	server = SocketServer.UDPServer((HOST, PORT), _UDPHandler)
        server.serve_forever()

