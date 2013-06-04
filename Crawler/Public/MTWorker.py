#!/usr/bin/python
#coding=utf-8
import sys, os
import time
project_path = os.path.dirname(__file__)
project_path = os.path.join(project_path, '..')
sys.path.append(project_path)

import threading
from Queue import Queue, Empty as QueueEmpty

class MTWorker(threading.Thread):
	"""
	MTWorker 
	"""
	def __init__(self, queue, processor=None):
		threading.Thread.__init__(self)
		self.task_queue = queue
		self.processor = processor

	def run(self):
		while True:
			try:
				data = self.task_queue.get(block=False)
				if self.processor is not None:
					self.processor(data)
					
				self.task_queue.task_done()

			except QueueEmpty:
				time.sleep(1)
			