# this is app entry 

import time
import random
import json
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

class AnalysisFundComment():
    def __init__(self, id, date, page = 1):
        self.id = id
        self.page = page
        self.date = date
        self.url = "http://guba.eastmoney.com/list,of{0}_{1}.html".format(id, page)
        self.content = urlopen(self.url)
        self.soup = BeautifulSoup(self.content, 'lxml')
        self.div = self.soup.select("div[class=articleh]")

    def countComment(self, date = ''):
        if (date == ''):
            date = self.date
        compareDate = time.strptime(date, '%Y-%m-%d')
        compareTs = time.mktime(compareDate)
        count = 0
        for comment in self.div:
            commentDate = comment.contents[6].string[:5]
            tsGroup = time.strptime('2017-'+commentDate, '%Y-%m-%d')
            ts = time.mktime(tsGroup)
            if (ts >= compareTs):
                count+=1
        return count

    def getCommentTitle(self):
        commentStr = []
        for comment in self.div:
            commentDate = '2017-'+comment.contents[6].string[:5]
            child = comment.a.string
            commentStr.append({'date':commentDate, 'content': child})
        return commentStr

    def getNextPage(self):
        nextPage = self.page + 1
        self.url = "http://guba.eastmoney.com/list,of{0}_{1}.html".format(self.id, nextPage)
        self.content = urlopen(self.url)
        self.soup = BeautifulSoup(self.content, 'lxml')
        self.div = self.soup.select("div[class=articleh]")

class InitFundId():
    def __init__(self):
        pass
    def getIdList(self):
        pass

    def getRankList(self):
        # param
        '''
        http://fundapi.eastmoney.com/fundtradenew.aspx?ft=zs&sc=3y&st=desc&pi=1&pn=100&cp=&ct=&cd=&ms=&fr=&plevel=&fst=&ftype=&fr1=&fl=0&isab=
        http://fund.eastmoney.com/trade/zs.html
        指数基金前50（3个月）
        op:ph
        dt:kf
        ft:gp
        rs:
        gs:0
        sc:3yzf 3-三个月排序 1-一个月排序
        st:desc
        sd:2016-11-28
        ed:2017-11-28
        qdii:
        tabSubtype:,,,,,
        pi:1 分页
        pn:50 每页条数
        dx:1
        v:0.5573508264089899
        '''
        url = 'http://fund.eastmoney.com/data/rankhandler.aspx?op=ph&dt=kf&ft=all&rs=&gs=0&sc={sc}&st=desc&sd={sd}&ed={ed}&qdii=&tabSubtype=,,,,,&pi={pi}&pn={pn}&dx=1&v={v}'
        # 设置参数
        url = url.format(**{
            'sc': '3yzf',
            'sd': time.strftime('%Y-%m-%d', time.localtime(time.time()-365*24*3600)),
            'ed': time.strftime('%Y-%m-%d'),
            'pi': 1,
            'pn': 50,
            'v': random.random()
        })
        content = urlopen(url).read()
        match = re.search('\[(.*)\]', content)
        print(match.group(1))
        # print(json.loads(repr(content[14:-1])))
        

# fundID = 160222
# page = 1
# date = '2017-11-28'

# comment = AnalysisFundComment(fundID, date, page)
# print(comment.getCommentTitle())

# comment.getNextPage()
# print(comment.getCommentTitle())


id = InitFundId()
id.getRankList()