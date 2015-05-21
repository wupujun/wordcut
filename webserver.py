# -*- coding: utf-8 -*-
#!/usr/bin/env python
import keyword2sent
import json
import logging
import web
import os

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='web.log',
                filemode='w')

urls = (
    '/img/(.*)', 'images', #this is where the image folder is located....
    '/(.*)','index'
    ) 

app= web.application(urls,globals())


render_globals = {}
render = web.template.render('web/', cache=False, globals = render_globals)
render_globals['render'] = render

#render = web.template.render('web/')

class images:
    def GET(self,name):
        ext = name.split(".")[-1] # Gather extension

        cType = {
            "png":"images/png",
            "jpg":"images/jpeg",
            "gif":"images/gif",
            "ico":"images/x-icon"
             }

        if name in os.listdir('web/img'):  # Security
            web.header("Content-Type", cType[ext]) # Set the Header
            return open('web/img/%s'%name,"rb").read() # Notice 'rb' for reading images
        else:
            raise web.notfound()

class index:

    def GET(self, name):

        i = web.input(name=None)
        if name=='unigram':
            unigramWords=keyword2sent.getUnigramWords()
            return render.unigram(name,unigramWords)
        elif name=='bigram':
            bigramWords=keyword2sent.getBigramWords()
            return render.bigram(name,bigramWords)

        elif name=='article':
            articles=keyword2sent.getArticles()
            return render.article(name,articles)

        elif name=='sentences':
            sentences=keyword2sent.getSentences()
            return render.sentences(name,sentences)
        elif name=='keyword2sent':
            sentences=keyword2sent.getSentencesByWord(i.key)
            return render.sentences(name,sentences)
        elif name=='stopword':
            stopwordList=keyword2sent.getStopwordList()
            return render.stopword(name,stopwordList)
        elif name=='emotional':
            elist=keyword2sent.getEmotionalWrods()
            return render.emotional(name,elist)
        elif name=='negative':
            nlist=keyword2sent.getNegativeWrods()
            return render.negative(name,nlist)
        
        elif name=='sharepage':
            return render.sharepage()
        else:
            sentences=keyword2sent.getSentences()
            return render.index(name,sentences)
        return 

    def POST(self,name):
        i=web.input(name=None)
        key= i.key

        if name=='getArticle':
            text,dic= keyword2sent.getArticleContent(key)
            value={'text':text,'dic':dic}

            return json.dumps(value)

        if name=='getSents':
            sents= keyword2sent.getSentencesByWord(key)            
            return json.dumps(sents)
        elif name=='addStopword':
            logging.info('add stopword:' + key)
            keyword2sent.addStopword(key)
        elif name=='removeStopword':
            logging.info('remove stopword:'+key)
            keyword2sent.removeStopword(key)
        elif name=='addNegativeWord':
            logging.info('add negative word:'+key)
            keyword2sent.addNegativeWord(key)
        elif name=='removeNegativeWord':
            logging.info('remove Negative word:'+key)
            keyword2sent.removeNegativeWord(key)
        elif name=='addEmotionalWord':
            logging.info('add emotional word:'+key)
            keyword2sent.addEmotionalWord(key)
        elif name=='removeEmotionalWord':
            logging.info('remove Emotional word:'+key)
            keyword2sent.removeEmotionalWord(key)    

        else:
            return json.dumps({'msg':'invalid request %s' %name})



if __name__== "__main__": 
    app.run()