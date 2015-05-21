# -*- coding: utf-8 -*-
#!/usr/bin/env python
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from ctypes import *

libc=cdll.LoadLibrary("LTPWrapper.dll")
'''
text=u'你好 world!'
key=u'主键'
fname='my.json'

buf=create_string_buffer(1024)
nChar=libc.writeJson(fname,key.encode('gb18030'), text.encode('gb18030'),buf)
print nChar

dic= json.loads(buf.raw[:nChar],encoding='gb18030')
v=dic[0][key] + u',我用python'
print v.encode('gb18030')

fp=open(fname,'r')
jsonObj=json.load(fp,encoding='gb18030')

print jsonObj
print jsonObj[0][key].encode('gb18030')

fp.close()
'''

outBuf=create_string_buffer(64*1024)

#msg=u'这个问题画了不少时间，贴出来供大家参考'
msg=open('in.txt').readline();



msg=msg.decode('utf-8')

print msg.encode('gb18030')

libc.loadConfig('C:\Apps\NLP\ltp_data')

nChar=libc.convert(msg.encode('gb18030'),outBuf)

libc.unLoadConfig()

print 'return %d char' %nChar
outString=outBuf.raw[:nChar]

fp=open('out.txt','w')
fp.write(outString)

fp.close()


ss=json.loads(outString,encoding='gb18030')

i=0
for s in ss:
	#print u"第%d句".encode('gb18030') %i
	i+=1 
	print s['sentence'].encode('gb18030')
#for w in dic:
#	print '%d %s %s %s' %(w['no'], w['word'].encode('gb18030'), w['tag'].encode('gb18030'),w['deprels'].encode('gb18030') )

