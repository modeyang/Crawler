#!/usr/bin/py
#coding = utf8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import md5
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


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
		
engine = create_engine("sqlite:///articles.db" , echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

class  LifeDBUtils(object):
	
	def __init__(self, name='articles'):
		self.session = Session()
		self.conn  = engine.connect()

	def addArticle(self, articles, commit=False):
		if isinstance(articles, (tuple, list)):
			self.session.add_all(articles)
		else:
			self.session.add(articles)

		if commit:
			self.session.commit()

	def ExecuteRawSQL(sql):
		try:
			result = LifeDBUtils.conn.execute(sql)
		except Exception, e:
			return None

	def addTheme(self, theme, commit=False):
		if theme:
			self.session.add(theme)

			if commit:
				self.session.commit()

	def getSession(self):
		return self.session or None

	def commit(self):
		self.session.commit()


if __name__ == '__main__':
    # pass
	session = LifeDBUtils().session
	session.query(Theme).filter_by(id=70).update({'isloaded' : 1})
	session.commit()
		
