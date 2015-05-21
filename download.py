# -*- coding:utf-8 -*-
import urllib 
import urllib2 
import os

def tsplit(string, delimiters):
    """Behaves str.split but supports multiple delimiters."""

    delimiters = tuple(delimiters)
    stack = [string,]

    for delimiter in delimiters:
        for i, substring in enumerate(stack):
            substack = substring.split(delimiter)
            stack.pop(i)
            for j, _substring in enumerate(substack):
                stack.insert(i+j, _substring)

    return stack

#os.mkdir("F:\\NLP\\abstract\\pdf")
urllist="pdf_urllist.txt";
fh = open(urllist)
for line in fh.readlines():
    line=line.strip('\n')
    
    tags=tsplit(line,('\t','?'))
    url=tags[1]
    
    
    fnameList=url.split('/')
    
    outName=fnameList[len(fnameList)-1]
    if (os.path.exists('pdf/'+outName)):
        print outName+' exists, skip it'
    else:
        print "Downloading " + url + "..."
        urllib.urlretrieve(url,"pdf/"+outName)
        

fh.close()
