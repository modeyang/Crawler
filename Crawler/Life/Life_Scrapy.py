#!/usr/bin/python
#coding=utf-8
import sys, os
project_path = os.path.dirname(__file__)
project_path = os.path.join(project_path, '..')
sys.path.append(project_path)

import re
import time
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup
from Public.Tables import Article, Theme
from DBUtil import LifeDBUtils

from Life_Articles import ArticleCrawler
from urlparse import urljoin
from Public.Utils import *
from sqlalchemy import and_, or_


class  LiftCrawler(object):
	"""docstring for  LiftCrawler"""
	def __init__(self, url):
		self.baseUrl = url
		self.themeUrls = {}
		self.DBUtil = LifeDBUtils()


	def isArticalUrl(self, url):
		return url.endswith('.shtm')

	def get_all_theme(self):
		soup = getHtmlSoup(self.baseUrl)
		for trSoup in soup.findAll('tr', attrs={'valign': 'top'}):
			try:
				tmSoup = trSoup.find('div', attrs={'class': 'tm'})
				navStr = tmSoup.find('span').text
				if navStr == "内容分类导航":
					mmSoup = trSoup.find('div', attrs={'class': 'mm'})
					for aSoup in mmSoup.findAll('a'):
						theme = aSoup.text
						url = aSoup['href']
						try:
							category = aSoup['class']
						except Exception:
							category = 'Child'
						self.DBUtil.addTheme(Theme(theme, urljoin(self.baseUrl, url.strip('/')), category))
			except Exception:
				pass
		self.DBUtil.commit()

	def get_theme_articleInfo(self, name, url):
		soup = getHtmlSoup(url)
		totals = soup.find('li', attrs={'class' : 'p_total'}).text
		totals = int(totals.split('/')[1])
		nextPages = [url + '/' +'indexp' + str(i) + '.shtm' for i in range(totals + 1) if i > 1]
		nextPages.insert(0, url)
		for pageUrl in nextPages:
			try:
				pageSoup = getHtmlSoup(pageUrl)
				newsSoup = pageSoup.find('span', attrs={'id': 'dlNews'})
				for aSoup in newsSoup.findAll('a'):
					url = aSoup['href']
					theme = Theme(name, urljoin(self.baseUrl, cleanUrl(url)), 'article')
					print theme
					self.DBUtil.addTheme(theme)
			except Exception, e:
				pass

		self.DBUtil.commit()


	def run(self):
		self.get_all_theme()
		session = self.DBUtil.getSession()

		# get all article of theme
		themes = session.query(Theme).filter(Theme.category == 'Child').all()
		for th in themes:
			self.get_theme_articleInfo(th.name, th.url)
		
		# query child url
		themes = session.query(Theme).filter(\
			and_(Theme.category == 'article', Theme.isloaded==0)).all()

		for theme in themes:
			crawler = ArticleCrawler(theme.url)
			if crawler.startScrapy():
				session.query(Theme).filter_by(id=theme.id).update({'isloaded' : 1}, synchronize_session=False)
				session.commit()
		self.DBUtil.close()

if __name__ == '__main__':
	starturl = 'http://love.heima.com'
	# starturl = 'http://love.heima.com/html/c37/49262.shtm'
	# starturl = 'http://love.heima.com/html/c47/54155.shtm'
	# LiftCrawler(starturl).CrapyOnTheme('', starturl)
	LiftCrawler(starturl).run()
	# ArticleCrawler(starturl).startScrapy()
	# print ArticleCrawler(starturl).getNextUrl()
