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
import os
import chardet
import codecs
from ctypes import *

import wordcount
import bigram


libc=cdll.LoadLibrary("LTPWrapper.dll")
libc.loadConfig('C:\Apps\NLP\ltp_data')
outBuf=create_string_buffer(640*1024)

#global constants
URL_BASE = "http://10.220.2.20:12345/ltp"
SEPERATORS = (u'。',u'；',u':',u'：',u',',u';',u'，',u',')

#uri_base = "http://192.168.199.222:12345/ltp"

#split article as multiple sentences
def tsplit(string, delimiters):

    delimiters = tuple(delimiters)
    stack = [string,]

    for delimiter in delimiters:
        for i, substring in enumerate(stack):
            substack = substring.split(delimiter)
            stack.pop(i)
            for j, _substring in enumerate(substack):
                stack.insert(i+j, _substring)

    return stack

def processSentenceLocal(line, wordDic,stopDic,sentencesList) :
	'''
	---don't do filtering---
	reasonString='主要原因' 
	if reasonString in line:
		pos= line.find(reasonString) + len(reasonString)
		line= line[pos:]
	
	preString='三、'
	if line.startswith(preString):
		line=line.replace(preString,'')
	'''
	#print chardet.detect(line)
	#print line
	print line.encode('gb18030')
	if len(line)<=0: 
		return 
	
	nChar=libc.convert(line.encode('gb18030'),outBuf)
	jsonStr=outBuf[:nChar]
	sList=json.loads(jsonStr,encoding='gb18030')
	
	for s in sList:
		sentencesList.append(s)

#process sentence
def processSentence(line, wordDic,stopDic,sentencesList) :
	#print line
	if len(line)<=0: 
		return 
	try: 
		data = {
		    's': line,
		    'x': 'n',
		    't': 'all'}

		request = urllib2.Request(URL_BASE)
		params = urllib.urlencode(data)
		response = urllib2.urlopen(request, params)
		content = response.read().strip()

		root=ElementTree.fromstring(content)
		words=root.findall('doc/para/sent/word')
		for word in words:
			#print word.get('cont').encode('utf-8')
			text=word.get('cont')
			if not (text in stopDic) and not(re.match(r'[0-9].*',text)):

				if not (text in wordDic):
					wordDic[text]=1
				else:
					wordDic[text]+=1
				#newWord={'text':text,'pos':word.get('pos'),'ne':word.get('ne'),'parent':word.get('parent'),'relate':word.get('relate')}	
		sentencesList.append({'original':line,'result':content})	

	except:
		print 'excpetion captured, badline='
		print line.encode('gb18030')
		print traceback.print_exc() 

#filter out sentence Out of Interest
def isNOISentence(s):
	return False	
	#print chardet.detect(s) 
'''
	try:
		uS= s.decode('utf-8')	
		startWord=u'三、'

		if startWord not in uS:
			return True
	except:
		print 'error in isNotSentence, s= %s' %s 		
	return False
'''

#pre-process to remove return
def preProcessLine(line):
	
	#preString=u'三、'
	#if line.startswith(preString):
	#	line=line[:len(preString)]


	newLine=line.strip().replace('\n','')

	return newLine

def processFile (file, wordDic, stopDic):

	print 'processing file', file

	try: 

		outfile= file+'.out'

		lines= codecs.open(file,'r','utf-8').readlines()
		text=''

		for line in lines:	
			text+=preProcessLine(line)

		sentencesList=[]
		sentences=tsplit(text,SEPERATORS)
		
		for sentence in sentences:
			#print sentence
			if isNOISentence(sentence):
				continue

			if len(sentence)>4000:
				print 'long sentence'
				subSentences=tsplit(sentence,('；',';'))
				for s in subSentences:
					processSentenceLocal (s.strip(), wordDic, stopDic,sentencesList)
			else:
				processSentenceLocal (sentence.strip(), wordDic, stopDic,sentencesList)
		
		outf=open(outfile,'w')
		json.dump(sentencesList,outf, ensure_ascii=False)		
		outf.close()
		
	except:
		print 'Error when processing ' + file
		print traceback.print_exc() 

		
	return




def loadDic(file) :
	lines=open(file,'r').readlines()
	keys=[]
	for line in lines:
		keys.append(line.strip())
	return keys

#entry of main

def processDir(path):


	wordDic={}
	stopDic=loadDic('dic/stopword.txt')

	flist=glob.glob(path)

	i=0
	for f in flist:
		i+=1
		print 'processing file %s (%d/%d)' %(f,i,len(flist))
		if os.path.exists(f+'.out'):
			print 'Skip %s, it had been processed.' %(f)
		else:
			processFile (f,wordDic,stopDic)
				


	total=0
	

	fresult=open('output.txt','w')
	json.dump(wordDic,fresult,ensure_ascii=False)
	fresult.close()
	libc.unLoadConfig()

def main():
	if len(sys.argv)>1:
		path=sys.argv[1]
	else:
		path= 'out'

	flist=path+'/*.txt'
	processDir(flist)
	wordcount.wordcount(path)
	bigram.bigramBuild(path)

if __name__=='__main__':
	main()
