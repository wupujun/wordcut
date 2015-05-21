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
import string
import caculateTFIDF
import numpy
import codecs
import scipy as sp


def processSentence (s, stopDic, callPerSentence,callPerWord) :
        

        sWords=[]

        words=s[u'words']
        for word in words:
            
            #print word.get('cont').encode('utf-8')
            tword=word[u'word']
            if  not (tword in stopDic) and not(re.match(r'[0-9].*',tword)) :
                #callPerWord(word,text)
                #if (tword in unigramList):
                sWords.append(tword)
        return sWords

def processFile (f,stopDic,callPerSentence,callPerWord,texts):
    
 
    fp=open(f,'r')
    sentenceList=json.load(fp,encoding='utf-8')
    fp.close()

    ftext=u''

    for s in sentenceList:
        #print 'line='+s['original'].encode('gb18030')
        sWords=processSentence(s,stopDic,callPerSentence,callPerWord)
        ftext+=string.join(sWords,',')

    #print 'get Fiels:'+ ftext.encode('gb18030')
    texts.append(ftext)

def loadDic(file) :
    lines=open(file,'r').readlines()
    keys=[]
    for line in lines:
        keys.append(line.strip())
    return keys

def processDir(path,callPerSentence,callPerWord,texts):

    stopDic=loadDic('dic/stopword.txt')

    flist=glob.glob(path)
    
    n=len(flist)
    i=0
    for f in flist:
        i+=1
        print 'processing file: %s (%d/%d)' %(f,i,n)
        processFile (f,stopDic,callPerSentence,callPerWord,texts)


def defaultS(s):
    #print s.encode('gb18030')
    pass

def defaultW(w):
    #print w.get('cont').encode('gb18030')
    pass



def loadTFIDF(path):

    weight=sp.load('tfidf_weight.npy')
    fp=codecs.open('tfidf_words.txt','r','utf-8')
    words=json.load(fp)
    fp.close()    
    return words,weight

    
def getFileFromPath(path,i):
    flist=glob.glob(patt)
    if i>=0 and i<len(flist):
        return flist[i]


def getTFIDF(path):
    texts=[]
    processDir(path,defaultS,defaultW,texts) 

    word,weight=caculateTFIDF.caculateTFIDF(texts)


    fp=codecs.open('tfidf_words.txt','w','utf-8')
    json.dump(texts,fp)
    fp.close()    
    sp.save('tfidf_weight.npy',weight)

    return word,weight
'''
    for i in range(len(weight)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
        print u"-------这里输出第".encode('gbk'),i,u"类文本的词语tf-idf权重------".encode('gbk')
        for j in range(len(word)):
            if weight[i][j] > 0:
                print word[j].encode('gbk'),weight[i][j]  
'''
#global varable
fp=codecs.open('wordfreq.txt','r','utf-8')
unigramList=json.load(fp,encoding='utf-8')
fp.close()


if len(unigramList) > 1000:
    unigramList=unigramList[:1000]

if __name__=='__main__':
    if len(sys.argv)>1:
        path=sys.argv[1]+'/*.out'
    else:
        path= 'test/*.out'

    print len(unigramList)
        
    getTFIDF(path)
    
    

