import multiprocessing

class ruptime_host_queue (object):
   	host_queue = None
	_lock = None

	def __init__ (self):
        	global host_queue
		global _lock
        	host_queue = multiprocessing.Queue() 
		_lock = multiprocessing.Lock()

	def put (self, data):
		'''host_queue.put(data, block=True, timeout=None)'''
		host_queue.put(data)

	def get (self):
		if self.is_empty() is True:
			return False
		else:
			return host_queue.get()

	def get_nowait (self):
		return host_queue.get_nowait()

	def get_lock (self):
		_lock.acquire()
	
	def release_lock (self):
		_lock.release()

	def close_queue (self):
		host_queue.close()

	def is_empty (self):
		if host_queue.empty():
			return True
		else:
			return False

