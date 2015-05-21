# -*- coding: utf-8 -*-
#!/usr/bin/env python
import loadResult
import json
from xml.etree import ElementTree

stopwords=loadResult.loadDic('dic/stopword.txt')

def processWord(w):
		word= w.get(u'word')
		cword= word.encode('gb18030')
		no= w.get(u'no')
		head=w.get(u'head')
		deprels=w.get(u'deprels')

		#print no,cword,head, deprels
		if word in stopwords:
			return
		if word in wordDic:
			wordDic[word]+=1
		else:
			wordDic[word] = 1


def processSentence(s):
	
	print s.get(u'sentence').encode('gb18030')

#	root=ElementTree.fromstring(xml)
#	sents=root.findall('doc/para/sent')

		
	for w in s[u'words']:
		word= w.get(u'word')
		cword= word.encode('gb18030')
		no= w.get(u'no')
		head=w.get(u'head')
		deprels=w.get(u'deprels')

		print no,cword,head, deprels
		
		#print ' %d %s %s %d' %(no,cword,deprels,head)
	
def wordcount(path):


	#loadResult.processDir('test/*.out',processSentence, None)
	loadResult.processDir(path+'/*.out',None, processWord)

	wordList= sorted(wordDic.items(),key=lambda x: x[1], reverse=True)

	noW=0
	totalW=0
	for w in wordList:
		totalW+= w[1]
		noW+=1

	print 'Total word: %d ,total no.: %d' %(noW,totalW)

	fp=open('wordfreq.txt','w')
	json.dump(wordList,fp,ensure_ascii=False) 
	fp.close()

wordDic={}

if __name__=='__main__':
	wordcount('out')