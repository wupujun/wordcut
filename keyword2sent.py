# -*- coding: utf-8 -*-
#!/usr/bin/env python
import loadResult
import json
from xml.etree import ElementTree
import hashlib
import logging
import os
import shutil
import glob
import codecs
import tfidf

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='app.log',
                filemode='w')

def getArticles():
	
	
	fp=codecs.open('urllist.txt','r','utf-8')
	urllist=json.load(fp,encoding='utf-8')
	fp.close()

	return urllist

def getArticleContent(path):
	#fpath=u"C:\\Apps\\NLP\\WordCut\\" + path
	fpath=path.replace('\\','/')
	fp=codecs.open(fpath,'r','utf-8')
	content=fp.readlines()	
	fp.close()
	text=''
	for l in content:
		text+= l
	#tfidf.getTFIDF()
	dic=getDocTFIDF(path)

	return text,dic

def getDocTFIDF(path):

	i=getSeqOfFile(path)

	aAr=weight[i]
	wordlist=words[i].split(',')

	outdic={}
	j=0
	for w in wordlist:
		outdic[w]=aAr[j]
		j=j+1
	return outdic

def getSeqOfFile(path):
	
	return 1

def getEmotionalWrods():
	return loadResult.loadDic('dic/emotionalword.txt')
	

def getNegativeWrods():
	
	return loadResult.loadDic('dic/negativeword.txt')

def getUnigramWords():
	return unigramList

def getBigramWords():
	bigramwords=[]
	for w in bigramList:
		bigramwords.append( (w[0],w[1].get('count') ) )
	return bigramwords

def getSentences():
	return sentDic.values()

def getStopwordList():
	return loadResult.loadDic('dic/stopword.txt')

def getSentencesByWord(key):
	print key
	v1=bigramDic[key]
	md5List=v1[u'MD5List']
	
	result=[]
	for s in sentDic:
		if s in md5List:
			result.append(sentDic[s])

	return result

def loadJsonFromFile(fname):
	fp=open(fname,'r')
	dic=json.load(fp,encoding='utf-8')
	fp.close()
	return dic


def removeNegativeWord(key):
	removeLineFromFile(key,'dic/negativeword.txt')
def addNegativeWord(key):
	appendLineToFile(key,'dic/negativeword.txt')


def removeEmotionalWord(key):
	removeLineFromFile(key,'dic/emotionalword.txt')
def addEmotionalWord(key):
	appendLineToFile(key,'dic/emotionalword.txt')


def removeStopword(key):
	removeLineFromFile(key,'dic/stopword.txt')
def addStopword(key):
	appendLineToFile(key,'dic/stopword.txt')


def removeLineFromFile(key,fname):
	stopwordList=loadResult.loadDic(fname)
	if key in stopwordList:
		stopwordList.remove(key)
	shutil.copyfile(fname, fname+'.bak')
	fp=open(fname,'w')
	stopwordList=[line+'\n' for line in stopwordList]
	fp.writelines(stopwordList)
	fp.close()
	logging.info('keyword: %s was added into %s.' %(key,fname) )

def appendLineToFile(key,fname):	
	fp=open(fname,'a')
	fp.writelines(key+'\n')
	fp.close()
	logging.info('keyword: %s was added into %s.' %(key,fname) )


#global variables
sentDic=loadJsonFromFile('sentenceList.txt')
bigramDic= loadJsonFromFile('bigram.txt')
unigramList=loadJsonFromFile('wordfreq.txt')
bigramList= sorted(bigramDic.items(),key=lambda x: x[1]['count'], reverse=True)
words,weight=tfidf.loadTFIDF('')

def main():
	top10=bigramList[:10]

	i=0
	for w in top10:
		print i,':',w[0].encode('gb18030')
		i+=1

	#index=raw_input('Select one index:')
	index=1


	if index in range(0,10):
		print 'index:', index
		key=top10[index][0]
		print key.encode('gb18030')
		sents=getSentencesByWord(key)
		for s in sents:
			print s.encode('gb18030')


if __name__=='__main__':
	main()
