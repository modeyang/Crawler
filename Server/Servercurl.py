#!/usr/bin/python
#coding=utf-8

import sys, os
project_path = os.path.dirname(__file__)
project_path = os.path.join(project_path, '..')
sys.path.append(project_path)

import pycurl
import StringIO
import socket
import random
import urllib

user_agents = [
	'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
]

class ServerCurl(object):
	"""docstring for ServerCurl"""

	def __init__(self, url, data=None):
		self.url = url
		self.data = data
		self.curl = pycurl.Curl()
		socket.setdefaulttimeout(10.0)

	def fetchurl(self, callback=None):
		b = StringIO.StringIO()
		self.curl.setopt(pycurl.WRITEFUNCTION, b.write)
		self.curl.setopt(pycurl.FOLLOWLOCATION, 1)
		self.curl.setopt(pycurl.MAXREDIRS, 5)
		self.curl.setopt(pycurl.USERAGENT, random.choice(user_agents))

		if self.data is not None:
			self.setopt(crl.POSTFIELDS,  urllib.urlencode(self.data))

		# self.curl.setopt(pycurl.COOKIEFILE, "cookie_file_name")
		self.curl.setopt(pycurl.URL, self.url.encode('utf-8'))
		self.curl.setopt(pycurl.TIMEOUT, 300)
		self.curl.perform()
		if callback:
			callback(b.getvalue())
		return b.getvalue()


if __name__ == "__main__":
	pass