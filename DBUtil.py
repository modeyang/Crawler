#!/usr/bin/python
#coding=utf-8
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from Life_Sqlite import Base, Theme, Article

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
	session = LifeDBUtils().session
	print session.query(Theme).all()
	# session.commit()