#!/usr/bin/python
#coding=utf-8
import sys, os
project_path = os.path.dirname(__file__)
project_path = os.path.join(project_path, '..')
sys.path.append(project_path)

from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from Public.Tables import *

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