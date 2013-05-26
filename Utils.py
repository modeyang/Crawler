#!/usr/bin/py
#coding=utf-8

import sys, os

# reload(sys)
# sys.setdefaultencoding('utf-8')

project_path = os.path.dirname(__file__)
project_path = os.path.join(project_path, '..')
sys.path.append(project_path)

from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
from lxml.html.clean import Cleaner
from Servercurl import ServerCurl
from urllibtest import urllibUtil
from urlparse import urljoin

def getBaseUrl(url):
	urls = url.split(r'/')
	return '/'.join(urls[0:3])

def cleanUrl(url):
	'''clean ../../faa/fda.html to faa/fda.html'''
	if url is None:
		return ''

	url = url.strip('/')
	while url.startswith('..'):
	 	url = url[2:]
	 	url = url.strip('/')
	return url

def getHtmlSoup(url):
	try:
		cleaner = Cleaner(page_structure=False, links=False, meta=False, safe_attrs_only=False)
		# htmls = cleaner.clean_html(urllibUtil().getHtmls(url))
		htmls = cleaner.clean_html(ServerCurl().fetchurl(url))
		return BeautifulSoup(htmls, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
	except Exception, e:
		pass
	return None


if __name__ == '__main__':
	pass
	# pass

	# import re
	# content = '''<!--
	# 		<script type="text/javascript">
	# 		var webownerId = 24975;
	# 		var childid = '10000';
	# 		var code_id = '10131406049032465780';
	# 		</script>
	# 		<script type="text/javascript" src="http://code.aizhuanlove.cn/code/10131406049032465780.js"></script>
	# 		-->'''
	# html = re.sub("^<!--.*-->", "", content,  flags=re.S)
	# print html 

	# print type('准备'), u'准备'
	# print hashmd5((u'准备').encode('utf8'))
