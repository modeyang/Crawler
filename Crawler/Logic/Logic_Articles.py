#!/usr/bin/python
#coding=utf-8
import sys, os

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from Crawler.Public.Tables import *

engine = create_engine("sqlite:///logics.db" , echo=True)
Base.metadata.create_all(engine)
DBSession = scoped_session(
	sessionmaker(
		bind=engine,
		autoflush=True,
		autocommit=False
	)
)


if __name__ == '__main__':
	pass