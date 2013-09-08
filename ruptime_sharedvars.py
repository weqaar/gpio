#!/usr/bin/env python

import threading

'''Global Vars'''
_thread_lock = None

'''Class Definitions'''
class ruptime_sharedvars(threading.Thread):
	'''Make it a Singleton class'''
	_instance = None
    	
	def __new__(cls, *args, **kwargs):
        	if not cls._instance:
            		cls._instance = super(ruptime_sharedvars, cls).__new__(cls, *args, **kwargs)
        	return cls._instance

	def __init__(self):
		threading.Thread.__init__(self)
		global _thread_lock
		'''A reentrant lock must be released by the thread that acquired it'''
		_thread_lock = threading.RLock()

	def run(self):
		pass

	def acquire_lock(self):
		_thread_lock.acquire(blocking=True)

	def release_lock(self):
		_thread_lock.release()
	'''
	def notify_lock(self):
		_thread_lock.notify()

	def wait_lock(self):
		_thread_lock.wait()
	'''

