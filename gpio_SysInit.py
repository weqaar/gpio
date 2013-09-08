#!/usr/bin/env python

from ConfigParser import RawConfigParser

class gpio_SysInit (object):
	version = 0.1
	gpio_conf = "gpio.conf"
	'''Parameters from conf file'''
	SERVER_DICT = None
	SERVER_CMD_DICT = None
	SERVER_IP = None
	SERVER_PORT = None
	GPIOFS_PATH = None
	rcp = None
	SUCCESS = 0
	ERROR = 1

        '''Make it a Singleton class'''
        _instance = None

        def __new__(cls, *args, **kwargs):
                if not cls._instance:
                        cls._instance = super(gpio_SysInit, cls).__new__(cls, *args, **kwargs)
                return cls._instance

        def __init__(self):
		self.config_parser()

	def config_parser(self):
		rcp = RawConfigParser()
		if rcp.read(self.gpio_conf) == []:
			return self.ERROR
		
		'''PINMAP Parameters'''
		self.SERVER_DICT = rcp.get("PINMAP","SERVER_LIST").strip("")
		self.SERVER_CMD_DICT = rcp.get("PINMAP","SERVER_CMD_LIST").strip("")
		
		'''NETWORK Parameters'''
		self.SERVER_IP = rcp.get("NET","SERVER").strip("")
		self.SERVER_PORT = rcp.get("NET","PORT").strip("")

		'''OTHER Parameters'''
		self.GPIOFS_PATH = rcp.get("PATHS","GPIOFS").strip("")
		
		return self.SUCCESS


