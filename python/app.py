# this is app entry 

import time
import random
import json
import re
import os.path
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup

class AnalysisFundComment():
    def __init__(self, id='', date='', page = 1):
        self.id = id
        self.page = page
        self.date = date
        self.div = None

    def setConfig(self, id, date, page=1):
        """
        id: int 基金id
        date: string 日期
        page: int 页数
        """
        self.id = id
        self.date = date
        self.page = page

    def sendRequest(self):
        id = self.id
        if (self.id==''):
            print('please set fund id first')
            exit(1)
        page = self.page
        if (page == 1):
            self.url = "http://guba.eastmoney.com/list,of{0}.html".format(id)
        else:
            self.url = "http://guba.eastmoney.com/list,of{0}_{1}.html".format(id, page)
        self.content = urlopen(self.url)
        self.soup = BeautifulSoup(self.content, 'lxml')
        self.div = self.soup.select("div[class=articleh]")

    def countComment(self,  date = ''):
        if (self.div == None):
            self.sendRequest()
        if (date == ''):
            date = self.date
        compareDate = time.strptime(date, '%Y-%m-%d')
        compareTs = time.mktime(compareDate)
        count = 0
        for comment in self.div:
            commentDate = comment.contents[6].string[:5]
            try:
                tsGroup = time.strptime('2017-'+commentDate, '%Y-%m-%d')
                ts = time.mktime(tsGroup)
            except Exception :
                ts = compareTs - 1000
                print('date error, skip  :' + commentDate)
            if (ts == compareTs):
                count+=1
        if (ts >= compareTs) :
            self.getNextPage()
            print(commentDate)
            print('id = '+repr(self.id)+'get next page = ' + repr(self.page))
            if (self.page >=100):
                return count
            count += self.countComment()
        return count

    def getCommentTitle(self):
        commentStr = []
        for comment in self.div:
            commentDate = '2017-'+comment.contents[6].string[:5]
            child = comment.a.string
            commentStr.append({'date':commentDate, 'title': child})
        return commentStr

    def getNextPage(self):
        self.page += 1
        self.sendRequest()

class AnalysisFundId():
    def __init__(self):
        self.path = os.path.abspath('./funddata/ranklist_'+time.strftime('%Y-%m-%d')+'.json')
        
    def getIdList(self):
        content = []
        ids = []
        if (os.path.isfile(self.path)):
            fp = open(self.path,'r')
            content = json.load(fp)
        else:
            content = self.getRankList()
        return list(content.keys())

    def getRankList(self):
        # param
        '''
        #http://fundapi.eastmoney.com/fundtradenew.aspx?ft=zs&sc=3y&st=desc&pi=1&pn=100&cp=&ct=&cd=&ms=&fr=&plevel=&fst=&ftype=&fr1=&fl=0&isab=
        #http://fund.eastmoney.com/trade/zs.html
        ft:zs zs-指数基金 hh-混合基金
        sc:3y 3y-三个月; y-一个月; z-一周;
        st:desc
        pi:1 页数
        pn:100 每页条数
        cp: 
        ct: 
        cd: 
        ms: 
        fr: 
        plevel: 
        fst: 
        ftype: 
        fr1: 
        fl:0
        isab:  
        # 'sd': time.strftime('%Y-%m-%d', time.localtime(time.time()-365*24*3600)),
        # 'ed': time.strftime('%Y-%m-%d'),
        #'v': random.random()
        '''
        if (os.path.isfile(self.path)):
            fp = open(self.path,'r')
            content = json.load(fp)
            return content
        url = 'http://fundapi.eastmoney.com/fundtradenew.aspx?ft={ft}&sc={sc}&st=desc&pi={pi}&pn={pn}&cp=&ct=&cd=&ms=&fr=&plevel=&fst=&ftype=&fr1=&fl=0&isab='
        params = [
            {
                'ft': 'zs',
                'sc': '3y',
                'pi': 1,
                'pn': 100
            },
            {
                'ft': 'zs',
                'sc': 'y',
                'pi': 1,
                'pn': 100
            },
            {
                'ft': 'zs',
                'sc': 'z',
                'pi': 1,
                'pn': 100
            },
            {
                'ft': 'hh',
                'sc': '3y',
                'pi': 1,
                'pn': 100
            },
            {
                'ft': 'hh',
                'sc': 'y',
                'pi': 1,
                'pn': 100
            },
            {
                'ft': 'hh',
                'sc': 'z',
                'pi': 1,
                'pn': 100
            }
        ]
        dictObj = {}
        for param in params:
            # 设置参数
            urlFormat = url.format(**param)
            content = urlopen(urlFormat).read()
            match = re.search('\[(.*)\]', str(content,'utf-8'))
            fundInfo = eval(match.group(0))
            for fund in fundInfo:
                item = fund.split('|')
                dictObj[item[0]] = item[1]+'|'+item[2]+'|'+param['ft']
            time.sleep(1)
        fp = open(self.path, 'w+')
        fp.write(json.dumps(dictObj))
        fp.close()
        return dictObj
        
# fundID = 160222
# page = 1
# date = '2017-11-28'

# comment = AnalysisFundComment(fundID, date, page)
# print(comment.getCommentTitle())

# comment.getNextPage()
# print(comment.getCommentTitle())


idHandler = AnalysisFundId()
# 暂存list
ids = idHandler.getIdList()
print(len(ids))

page = 1
date = time.strftime('%Y-%m-%d')
fundID = 160222
# comment = AnalysisFundComment(fundID, date, page)
# print(comment.countComment())

comment = AnalysisFundComment()
idMap = []
for id in ids:
    # time.sleep(1)
    comment.setConfig(id, date)
    comment.sendRequest()
    count = comment.countComment()
    idMap.append({'id':id,'count':count})
    print('count fund id='+ repr(id) + ' value='+repr(count))

path = os.path.abspath('./funddata/fundcount_'+date+'-ts_'+time.strftime('%Y-%m-%d_%H:%M:%S')+'.json')
fp = open(path,'w+')
fp.write(json.dumps(idMap))
fp.close()

print('complete')