#!/usr/bin/env python

import sys, os

project_path = os.path.dirname(__file__)
project_path = os.path.join(project_path, '..')
sys.path.append(project_path)

import urllib2, urllib, cookielib
import socket, random
import gzip

try:
	from cStringIO import StringIO
except Exception, e:
	from StringIO import StringIO

class urllibUtil(object):
	
	def __init__(self):
		socket.setdefaulttimeout(10)
	
	def openUrl(self, url, data=None):
		cookie_support = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
		self.opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler, urllib2.HTTPRedirectHandler)
		urllib2.install_opener(self.opener)

		# proxy_support = urllib2.ProxyHandler({'http', 'http://XX.XX.XX.XX:XXXX'})
		# opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
		# urllib2.install_opener(opener)
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
		
		agent = random.choice(user_agents)
		self.opener.addheaders = [('User-agent', agent),("Accept","*/*"),('Referer',url)]
		try:
			handler = self.opener.open(url)
		except Exception, e:
			return None
		return handler

	def getHtmls(self, url):
		try:
			handler = self.openUrl(url)
			if handler.headers.has_key('content-encoding'):
				if 'gzip' in handler.headers['content-encoding']:
					fileobj = StringIO()
					fileobj.write(handler.read())
					fileobj.seek(0)
					gzip_file = gzip.GzipFile(fileobj = fileobj)
					return gzip_file.read()
				else:
					return handler.read()

		except Exception, e:
			return handler.read()
		return ''

	
	@staticmethod
	def retrievefile(url, storage=None, callback=None):
		def cbk(a, b, c):
			per = 100.0 * a * b /c 
			if per > 100:
				per = 100
			print '%.2f%%' % per 
		if callback is None:
			callback = cbk
		if storage is None:
			storage = url.split('/')[-1]
		urllib.urlretrieve(url, storage, callback)
	
	@staticmethod
	def testescape():
		# url escape
		data = 'name=dasf'
		data1 = urllib.quote(data)
		print data1
		print urllib.unquote(data1)
		
		# json file 
		data3 = urllib.urlencode({ 'name': 'dark-bull', 'age': 200 })  
		print data3
		
		data4 = urllib.pathname2url(r'd:/a/b/c/23.php')  
		print data4 # result: ///D|/a/b/c/23.php  
		print urllib.url2pathname(data4)    # result: D:/a/b/c/23.php 
		
if __name__ == '__main__':
	data = {'email': '523720676@qq.com', 'password':'123456ygs'}
	print urllib.urlencode(data)
	url = 'https://github.com/login'
	auth_handler = urllib2.HTTPBasicAuthHandler()
	auth_handler.add_password(
							realm='PDQ Application',
							uri='https://github.com/login',
							user='523720676@qq.com',
							passwd='123456ygs')

	opener = urllib2.build_opener(auth_handler)
	urllib2.install_opener(opener)

	handler = urllibUtil().openUrl(url, data)
	print handler.getcode()
	print handler.info()
	print handler.geturl()
	
	
