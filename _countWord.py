# -*- coding: utf-8 -*-
#!/usr/bin/env python
import loadResult
import json

def processSentence(s, xml):
	#print 'line='+s.encode('gb18030')
	return

def processWord(w):
	#print w.get('cont').encode('gb18030')
	word=w.get('cont')
	if word in wordDic:
		wordDic[word]+=1
	else:
		wordDic[word]=1

wordDic={}

loadResult.processDir('data/*.out',None, processWord)

wordList= sorted(wordDic.items(),key=lambda x: x[1])

fp=open('wordfreq.txt','w')
json.dump(wordList,fp,ensure_ascii=False) 
fp.close()
'''
for k in wordDic:
	print '%s=%d' %(k.encode('gb18030'),wordDic[k])
'''