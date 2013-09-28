#!/usr/bin/python
#coding=utf-8

import sys, os
import re
from Crawler.Public.Tables import Article, Theme
from DBUtil import LifeDBUtils
from urlparse import urljoin
from Crawler.Public.Utils import *


class  ArticleCrawler(object):
	def __init__(self, url):
		self.url = url
		self.baseUrl = getBaseUrl(url)
		self.soup = getHtmlSoup(url)
		self.DBUtils = LifeDBUtils()

	def isArticalUrl(self, url):
		return url.endswith('.shtm')
		
	def get_title_category(self):
		try:
			title_category = self.soup.title.string
			pos = title_category.rfind('_')
			title = title_category[0:pos]
			category = title_category[pos + 1:]
		except Exception, e:
			title, category = '', ''

		return title, category

	def get_desc(self):
		try:
			return self.soup.find('meta', attrs={'name':'description'})['content']
		except Exception, e:
			return ''

	def get_keywords(self):
		try:
			return self.soup.find('meta', attrs={'name':'keywords'})['content']
		except Exception, e:
			return ''

	def getNextUrl(self):
		try:
			urlSoup = self.soup.find('div' , attrs={'class' : 'prevNews'} )
			url = urlSoup.find('a')['href']
			return urljoin(self.baseUrl, cleanUrl(url))
		except Exception, e:
			pass
		return None

	def getPrevUrl(self):
		try:
			urlSoup = self.soup.find('div' , attrs={'class' : 'nextNews'} )
			url = urlSoup.find('a')['href']
			return urljoin(self.baseUrl, cleanUrl(url))
		except Exception, e:
			pass
		return None

	def get_content(self):
		try:
			conSoup = self.soup.find('div', attrs={'id' : 'content'})
			pConts = conSoup.findAll('p')
			contents = ''
			if len(pConts) == 0:
				for node in conSoup.contents:
					attr = getattr(node, 'name', None)
					if attr == 'br' or attr == 'a':
						atext = node.text or ''
						art = node.nextSibling
						if getattr(art, 'name', None) in ['div', 'span', 'script']:
							continue
						else:
							if getattr(art, 'string'):
								contents += atext + art.string + os.linesep
				return contents

			else:
				for p in pConts:
					if len(p.text) > 0:
						contents += p.text + os.linesep
				return contents
		except Exception, e:
			return ''

	def startScrapy(self):
		print self.url
		title, category = self.get_title_category()
		desc = self.get_desc()
		keywords = self.get_keywords()
		content = self.get_content()
		print title, category
		if len(content) > 0:
			article = Article(self.url, title, content, keywords, category, desc)
			self.DBUtils.addArticle(article, commit=True)
			self.DBUtils.close()
			return True
		return False

if __name__ == '__main__':
	url = 'http://love.heima.com/HunLiChouBei/54498.shtm'
	# ArticleCrawler(url).startScrapy()