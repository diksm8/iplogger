#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ipify
from ipify.exceptions import ConnectionError, ServiceError
import logging
import atexit
from apscheduler.schedulers.blocking import BlockingScheduler
logging.basicConfig(level=logging.INFO,
	format='%(asctime)s %(message)s',
	datefmt='[%m/%d/%Y %H:%M:%S]',
	filename='iplog.log',
	filemode='a+')
logging.getLogger('apscheduler').setLevel(logging.WARNING)

def new_ip():
	try:
		return ipify.get_ip()
	except ConnectionError as e:
		logging.error(str(e))
	except ServiceError as e:
		logging.error(str(e))
	except Exception as e:
		logging.error(str(e))

def loop():
	global current_ip
	global new_ip
	try:
		new_ip = new_ip()
		if new_ip != current_ip:
			logging.info('New IP is %s' % new_ip)
			current_ip = new_ip
	except Exception as e:
		logging.exception('Exception:')


current_ip = new_ip()
logging.info('Start IP is %s' % current_ip)
scheduler = BlockingScheduler()
scheduler.add_job(loop, 'interval', minutes=1)
scheduler.start()