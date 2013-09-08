#!/usr/bin/env python

import sys
import threading
import UDP_Server
import multiprocessing
from ruptime_host_queue import *
from gpio_SysInit import *
from gpiolib import *
from cStringIO import StringIO

class Thread_UDPServer(threading.Thread):

        def __init__(self):
                threading.Thread.__init__(self)

        def run(self):
                UDP_Server.start_server(conf_params.SERVER_IP, conf_params.SERVER_PORT)


class Thread_GPIO(threading.Thread):

        def __init__(self):
                threading.Thread.__init__(self)

        def run(self):
		
		while True:
			while gpio_queue.is_empty() == False:
				data = gpio_queue.get()
				_server = data.split()[0]
				_cmd = data.split()[1]
				print "server: " + data.split()[0] + "\n"
				print "cmd: " + data.split()[1] + "\n"
				if self.gpio_action(_server, _cmd) is True:
					print "OPERATION SUCCESSFUL: " + _server + " : " + _cmd + "\n"
				else:
					print "OPERATION FAILED: " + _server + " : " + _cmd + "\n"
					

	def gpio_action(self, _server, _cmd):
		if _server in gpio_dict:
			if _cmd in gpio_cmd_dict:
				gpio_handler = GPIO(gpio_dict[_server])
				gpio_handler.set_value(gpio_cmd_dict[_cmd])
				return True
			else:	
				return False
		else:
			return False


def main():
	global gpio_queue
	global conf_params
	global gpio_dict
	global gpio_cmd_dict

	gpio_queue = ruptime_host_queue()
	conf_params = gpio_SysInit()

	#Convert String to Dictionary
	gpio_dict = {}
	strdict = conf_params.SERVER_DICT.strip("{").strip("}")
	for item in strdict.split(','):
		key,value = item.split(':')
		if gpio_dict.get( key ):
			gpio_dict[ key ] += int( value )
		else:
			gpio_dict[ key ] = int( value )

	print "GPIO for mysql is: " + str(gpio_dict['mysql'])

	gpio_cmd_dict = {}
	strdict_cmd = conf_params.SERVER_CMD_DICT.strip("{").strip("}")
	for item in strdict_cmd.split(','):
		key,value = item.split(':')
		if gpio_cmd_dict.get( key ):
			gpio_cmd_dict[ key ] += int( value )
		else:
			gpio_cmd_dict[ key ] = int( value )

	t0 = Thread_UDPServer()
	t0.start()

	t1 = Thread_GPIO()
	t1.start()

if __name__ == '__main__':
        main()

