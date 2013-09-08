#!/usr/bin/env python

import threading
import multiprocessing
import sys
import time
import smtplib
from ruptime_SysInit import *
from ruptime_host_queue import *
from ruptime_host_stats_queue import *
from ruptime_sharedvars import *
from subprocess import *

'''Global Vars'''
_ruptime_init = None
_host_list = None
_host_queue = None
_host_stats_queue = None
tlock = None

'''Class Definitions'''
class Thread_Conf(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		global _ruptime_init, _host_list, _host_queue, _host_stats_queue, tlock
		tlock = ruptime_sharedvars()
		'''Initialize Queues'''
		_host_queue = ruptime_host_queue()
		_host_stats_queue = ruptime_host_stats_queue()
		'''Initialize System'''
		_ruptime_init = ruptime_SysInit()
		_ruptime_init.config_parser()
		_host_list = _ruptime_init.read_file()

	def run(self):
		pass

class Thread_Host_Init(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		tlock.acquire_lock()	
		while _host_list is None:
			pass
		for i in range(len(_host_list)):
			_host_queue.put(_host_list[i].strip('\n'))
		'''Must release lock for other threads waiting to acquire()'''
		tlock.release_lock()	

class Thread_SSH(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		tlock.acquire_lock()
		_threads = []

		for i in range(int(_ruptime_init._max_threads)):
        		_t = Thread_exec_uptime()
			_threads += [_t] 
        		_t.start()
		
		'''_host_queue.close_queue()'''
		for x in _threads: 
    			x.join()

		'''Must Release the lock and close the queue otherwise QueueFeederThread Exception is thrown'''
		tlock.release_lock()

		_t1 = Thread_uptime_stats()
		_t1.start()	
		

class Thread_exec_uptime(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)

        def run(self):
		while _host_queue.is_empty() == False:
			_hname = _host_queue.get()
			if _hname is False:
				sys.exit()
			result = Popen([_ruptime_init._ssh_binary, _ruptime_init._ssh_quiet, _ruptime_init._ssh_args, \
					_ruptime_init._ssh_login + "@" + \
			      		_hname, _ruptime_init._ssh_remote_cmd], stdout=PIPE)
			'''communicate() returns a Tuple (output, error)'''
			out, err = result.communicate()

			if out == '':
				sys.exit()

			'''Populate the _host_stats_queue, that queue holds output from [uptime]'''
			if _ruptime_init.__DEBUG__ == 'True':
				print "blahhh" + str(self.parse_uptime_output(out, _hname))

			if (':' not in [s.strip() for s in out.strip('\n').replace(',', ' ').split(' ')][1]):
				print "Unknown Host: " + _hname + "\n"
				sys.exit()

			_host_stats_queue.put(self.parse_uptime_output(out.strip('\n'), _hname))

	'''Parse UPTIME output, returns Dictionary {}'''
	def parse_uptime_output(self, output, _host):
		_output_str = output.split(' ', 30)
		'''Better to use the Lambda function inside _host_node structure for [running_time]'''
		if _output_str[4].split(',')[0] == ('day' or 'days'):
			_running_time = _output_str[3].split(',')[0] + _output_str[4].split(',')[0] + ' ' + _output_str[6].split(',')[0]
		else:
			_running_time = _output_str[6].split(',')[0]
		_host_node = { 'host' : _host,
                               'current_timestamp' : _output_str[1],
                               'running_time' : _running_time,
                               'users_loggedin' : _output_str[8].split(',')[0],
                               'load_avg' : {  '5Min' : _output_str[13].split(',')[0],
                                               '10Min' : _output_str[14].split(',')[0],
                                               '15Min' : _output_str[15].split(',')[0].strip('\n'),
                                            }
                             }
		return _host_node


class Thread_uptime_stats(threading.Thread):
	
        def __init__(self):
                threading.Thread.__init__(self)

        def run(self):
		tlock.acquire_lock()
		
		if _ruptime_init.__DEBUG__ == 'True':
			print "inside Thread_uptime_stats\n"

		while _host_stats_queue.is_empty() == False:
			_node_struct = _host_stats_queue.get()
			if _node_struct is not False:
				self._print_stdout(_node_struct)
			else:
				sys.exit()


	def _print_stdout(self, _node_dict):
		_marker = '-------------------------------------------'
		_n = '\n'
		print _marker
		print "Hostname:\t\t" + _node_dict['host'] + _n
		print "Current Timestamp:\t" + _node_dict['current_timestamp'] + _n
		print "Running Time:\t\t" + _node_dict['running_time'] + _n
		print "Users Loggedin:\t\t" + _node_dict['users_loggedin'] + _n
		print "Load Average:" + _n
		print "\t\t5 Minutes:\t" + _node_dict['load_avg']['5Min'] + _n
		print "\t\t10 Minutes:\t" + _node_dict['load_avg']['10Min'] + _n
		print "\t\t15 Minutes:\t" + _node_dict['load_avg']['15Min'] + _n


class Thread_mail(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)

        def run(self):
		pass		
	
	def _send_email(self, _mesg):
		_smtp = smtplib.SMTP(_ruptime_init._mail_server)
		_smtp.sendmail(_ruptime_init._mail_from + _ruptime_init._mail_domain, _ruptime_init._mail_to, _ruptime_init._mail_subject + "\n" + _mesg)
		_smtp.quit()
	

