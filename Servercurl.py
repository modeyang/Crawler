#!/bin/env python

import pycurl
import StringIO

class ServerCurl(object):
	"""docstring for ServerCurl"""

	def __init__(self):
		super(ServerCurl, self).__init__()
		self.curl = pycurl.Curl()

	def fetchurl(self, url, callback=None):
		self.curl.setopt(pycurl.URL, url.encode('utf-8'))
		b = StringIO.StringIO()
		self.curl.setopt(pycurl.WRITEFUNCTION, b.write)
		self.curl.setopt(pycurl.FOLLOWLOCATION, 1)
		self.curl.setopt(pycurl.MAXREDIRS, 5)
		self.curl.perform()
		if callback:
			callback(b.getvalue())
		return b.getvalue()

		