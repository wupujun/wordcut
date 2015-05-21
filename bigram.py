# -*- coding: utf-8 -*-
#!/usr/bin/env python
import loadResult
import json
from xml.etree import ElementTree
import hashlib


wordList=[]
bigramList=[]
bigramDic={}
sentenceDic={}

def processSentence(s):
	

	sentence=s.get(u'sentence').decode()
	sentence=sentence.replace(u'【研究报告内容摘要】','')
	md5=hashlib.md5(sentence).hexdigest()
	

	#md5=hashlib.md5(sentence.encode(‘utf-8′)).hexdigest()
	sentenceDic[md5]=sentence


	wordList=s[u'words']
	words=[]
	for w in wordList:
		words.append(w.get(u'word'))

	for dw in bigramList:
		
		if dw[0] in words and dw[1] in words:
			
			bikey=u'%s-%s' %(dw[0],dw[1])
			
			print bikey.encode('gb18030')
			print sentence.encode('gb18030')

			if bikey in bigramDic:
				v=bigramDic[bikey]
				if md5 not in v[u'MD5List']:
					v[u'MD5List'].append(md5)
				v['count']+=1
				bigramDic[bikey]=v
			else:	
				v={u'MD5List':[md5],u'count':1}			
				bigramDic[bikey]= v


#loadResult.processDir('test/*.out',processSentence, None)
def bigramBuild(path):

	fp=open('wordfreq.txt','r')
	wordList=json.load(fp,encoding='utf-8') 
	fp.close()

	topWordlist=wordList[:50]



	for w1 in topWordlist:
		for w2 in topWordlist:
			if w1[0]==w2[0]:
				continue
			else:
				if (w1[0],w2[0]) not in bigramList and (w2[0],w1[0]) not in bigramList :
					bigramList.append((w1[0],w2[0]))


	loadResult.processDir(path+'/*.out',processSentence, None)

	#bigramList= sorted(bigramDic.items(),key=lambda x: x[1]['count'], reverse=True)


	fp=open('sentenceList.txt','w')
	json.dump(sentenceDic,fp,ensure_ascii=False)
	fp.close()

	fp=open('bigram.txt','w')
	json.dump(bigramDic, fp, ensure_ascii=False)
	fp.close()

