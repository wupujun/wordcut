# -*- coding: utf-8 -*-
#!/usr/bin/env python
import urllib, urllib2
from xml.etree import ElementTree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import glob
import re
import json
import traceback



def processSentence (s, stopDic, callPerSentence,callPerWord) :
		
		if callPerSentence is not None:
			callPerSentence (s)

		if callPerWord is None:
			return 

		words=s[u'words']
		for word in words:
			
			#print word.get('cont').encode('utf-8')
			text=word[u'word']
			if not (text in stopDic) and not(re.match(r'[0-9].*',text)):
				callPerWord(word)


def processFile (f,stopDic,callPerSentence,callPerWord):
	fp=open(f,'r')
	sentenceList=json.load(fp,encoding='utf-8')
	fp.close()

	for s in sentenceList:
		#print 'line='+s['original'].encode('gb18030')
		processSentence(s,stopDic,callPerSentence,callPerWord)


def loadDic(file) :
	lines=open(file,'r').readlines()
	keys=[]
	for line in lines:
		keys.append(line.strip())
	return keys

def processDir(path,callPerSentence,callPerWord):

	stopDic=loadDic('dic/stopword.txt')

	flist=glob.glob(path)
	
	for f in flist:
		#print 'processing file: %s' %f
		processFile (f,stopDic,callPerSentence,callPerWord)


def defaultS(s,xml):
	print s.encode('gb18030')

def defaultW(w):
	print w.get('cont').encode('gb18030')

if __name__=='__main__':
	if len(sys.argv)>1:
		path=sys.argv[1]+'/*.out'
	else:
		path= 'data/*.out'
	processDir(path,defaultS,defaultW)