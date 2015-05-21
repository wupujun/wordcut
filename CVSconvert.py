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
import csv


def toCSV(infname,outfname):
    fp=open(infname,'r')
    urllist=json.load(fp,encoding='utf-8')
    fp.close()
   
    FIELDS = ['url', 'file', 'title', 'result']  
  
    # DictWriter  
    csv_file = codecs.open(outfname, 'wb','utf-8')  
    writer = csv.DictWriter(csv_file, fieldnames=FIELDS ) 
    # write header  
    writer.writerow(dict(zip(FIELDS, FIELDS)))  
     
    writer.writerows(urllist)  
    csv_file.close()  

    return len(urllist)

def fromCSV(fname):
   
    reader= csv.DictReader(open(fname, 'rb') )
    aList=[]
    for line in reader:
        aList.append(line)

    return aList 


noRec= toCSV('urllist.txt','result.csv')
print noRec

aList=fromCSV('result.csv')
print type(aList)
print len(aList)

for i in range(0,10):
    print aList[i].get('title').encode('gb18030')
