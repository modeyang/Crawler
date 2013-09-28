#!/usr/bin/python
#coding=utf-8

import sys, os
import re
import collections
# from Crawler.Public.Tables import Article, Theme
# from DBUtil import LifeDBUtils
from urlparse import urljoin
from Crawler.Public.Utils import *
from Crawler.Server.Servercurl import ServerCurl
from JuSqlite3 import sqliteDB

class  ArticleCrawler(object):
    def __init__(self, aUrl='', qUrl='', sels=[], style='', packName=''):
        self.aUrl = aUrl
        self.qUrl = qUrl
        self.QADcit = {}
        self.QuestionDict = {}
        self.sels = sels
        self.StyleName = style
        self.PackName = packName

    def getSeq(self, seq):
        seq = seq.strip()
        index = 0
        for i in seq[:]:
            try:
                int(i)
            except Exception, e:
                break
            index += 1
        seq = seq[:index]
        return int(seq)


    def getAnswear(self):
        soup = getHtmlSoup(self.aUrl)
        # soup = BeautifulSoup(open('ju.html', 'r').read(), convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
        contentSoup = soup.find('div', attrs={'id' : 'content_l_nr_content1'})
        contentSoup = contentSoup.find('div', attrs={'class' : 'Section0'})
        answerSeq = {'A' : 1 , 'B' : 2, 'C' : 3, 'D' : 4}

        seqPattern = re.compile(r'\d+.+')
        choosePattern = re.compile('(A|B|C|D).+')
        seq = None
        for p in contentSoup.findAll('p'):
            match = seqPattern.match(p.text[:3])
            if match:
                seq = self.getSeq(match.group())

            if 'underline' in str(p):
                match = choosePattern.match(p.text)
                if match:
                    right = match.group(1)
                    right = answerSeq[right]
                    try:
                        self.QADcit[seq].append(right)
                    except Exception, e:
                        self.QADcit[seq] = [right]    


    def getQuestion(self):
        soup = getHtmlSoup(self.qUrl)
        # soup = BeautifulSoup(open('ju_Q.html', 'r').read(), convertEntities=BeautifulStoneSoup.HTML_ENTITIES)
        contentSoup = soup.find('div', attrs={'id' : 'content_l_nr_content1'})
        contentSoup = contentSoup.find('div', attrs={'class' : 'Section0'})

        others = []
        seqPattern = re.compile(r'\d+.+')
        choosePattern = re.compile('(A|B|C|D).+')
        seq = None
        for p in contentSoup.findAll('p'):
            if len(p.text.strip()) == 0:
                continue

            match = seqPattern.match(p.text[:3])
            if match:
                seq = self.getSeq(match.group())
                self.QuestionDict[seq] = {
                    'question' : p.text[len(str(seq)) + 1:],
                } 
                continue  

            match = choosePattern.match(p.text)
            if match:
                try:
                    self.QuestionDict[seq]['options'].append(p.text[2:])
                except Exception, e:
                    self.QuestionDict[seq].update({'options' : [p.text[2:]]})
                continue

            others.append(p.text)

        return others

    def getSelType(self, index):
        for i in range(len(self.sels)):
            if index < self.sels[i]:
                return i+1
        return 0

    def runScrapy(self, TestType=1003):
        others = self.getQuestion()
        self.getAnswear()

        f = open('%s.txt' % TestType, 'w')
        for line in others:
            f.write(line.encode('utf8') + '\n')
        f.close()

        pos = []
        for key in self.QuestionDict.keys():
            print key
            dictQA = self.QuestionDict[key]
            try:
                dictQA.update({'answer' : map(str, self.QADcit[key])})
                pos.append(key)
            except Exception, e:
                print e
                continue

            # print dictQA

            dataDict = {}
            dataDict['TestType'] = TestType
            dataDict['QuesText'] = dictQA['question'].encode('utf8')
            dataDict['AnswerText'] = ('++'.join(dictQA['options'])).encode('utf8')
            dataDict['Answer'] = '++'.join(dictQA['answer'])
            dataDict['SelectionType'] = self.getSelType(key)
            dataDict['StyleName'] = self.StyleName
            dataDict['PackName'] = self.PackName
            dataDict['Handle'] = key

            # print dataDict

            dbUtil = sqliteDB()
            dbUtil.insert('Selection', dataDict)
            # print dbUtil.fetchall('select * from Selection where TestType=1004')
        print pos
        print 'end: ', len(pos)



if __name__ == '__main__':
    QAList = [
        {
            'qUrl' : 'http://www.cnsikao.com/html/20130916/137931417515288.html',
            'aUrl' : 'http://www.cnsikao.com/html/20130922/137982931215294.html',
            'sels' : [51, 86],
            'style' : '卷一',
            'pack' : '2013 卷一'
        },
        {
            'qUrl' : 'http://www.cnsikao.com/html/20130916/137931424415289.html',
            'aUrl' : 'http://www.cnsikao.com/html/20130922/137982946615295.html',
            'sels' : [51, 86],
            'style' : '卷二',
            'pack' : '2013 卷二'
        },
        {
            'qUrl' : 'http://www.cnsikao.com/html/20130916/137931429415290.html',
            'aUrl' : 'http://www.cnsikao.com/html/20130922/137982975315296.html',
            'sels' : [51, 86],
            'style' : '卷三',
            'pack' : '2013 卷三'
        },
        # {
        #     'qUrl' : 'http://www.cnsikao.com/html/20121121/13534845481212.html',
        #     'aUrl' : 'http://www.cnsikao.com/html/20121121/13534911781531.html',
        #     'sels' : [51, 100],
        #     'style' : '卷一',
        #     'pack' : '2012 卷一'
        # },
        # {
        #     'qUrl' : 'http://www.cnsikao.com/html/20121121/13534846291213.html',
        #     'aUrl' : 'http://www.cnsikao.com/html/20121121/13534912241532.html',
        #     'sels' : [51, 100],
        #     'style' : '卷二',
        #     'pack' : '2012 卷二'
        # },
        # {
        #     'qUrl' : 'http://www.cnsikao.com/html/20121121/13534864831214.html',
        #     'aUrl' : 'http://www.cnsikao.com/html/20121121/13534912541533.html',
        #     'sels' : [51, 100],
        #     'style' : '卷三',
        #     'pack' : '2012 卷三'
        # },
    ]

    startPos = 1004
    for item in QAList:
        aUrl = item['aUrl']
        qUrl = item['qUrl']
        sels = item['sels']
        style = item['style']
        pack = item['pack']
        ArticleCrawler(aUrl=aUrl, qUrl=qUrl, sels=sels, style=style, packName=pack).runScrapy(TestType=startPos)
        startPos += 1
        # break
