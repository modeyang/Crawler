#!/usr/bin/python
#coding = utf-8

import sys, os
project_path = os.path.dirname(__file__)
project_path = os.path.join(project_path, '..')
sys.path.append(project_path)

import md5
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Article(Base):
	"""docstring for Article"""

	__tablename__ = 'article'
	id = Column(Integer, primary_key=True)
	title = Column(String)
	keywords = Column(String)
	category = Column(String, index=True)
	description = Column(String)
	url = Column(String)
	content = Column(String)
	md5value = Column(String, index=True)

	def __init__(self, url,  title, content, keywords="", category="", desc=""):
		self.title = title
		self.keywords = keywords
		self.category = category
		self.description = desc
		self.url = url
		self.content = content
		self.md5value = md5.md5(content).hexdigest()

	def __repr__(self):
		return "<Article('%s', '%s')>" % (self.title, self.category)

class Theme(Base):
	"""docstring for Theme"""

	__tablename__ = 'theme'
	id = Column(Integer, primary_key=True)
	name = Column(String, index=True)
	url = Column(String)
	category = Column(String, index=True)
	isloaded = Column(Integer, default=0)

	def __init__(self, name, url, category):
		self.name = name
		self.url = url
		self.category = category
		self.isloaded = 0
		self.md5value = md5.md5(name).hexdigest()

	def __str__(self):
		return "%s %s %s " % (self.name, self.url, self.category)
	
__all__ = ['Base', 'Article', 'Theme']

		
		
