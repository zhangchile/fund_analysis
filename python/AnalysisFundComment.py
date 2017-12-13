import time
import jieba
import os
import json
import random
import urllib.request
from bs4 import BeautifulSoup
from urllib.request import urlopen

class AnalysisFundComment():
    ''' 基金评论模块
    @id string 基金id
    @date 默认为当前日期
    @page 页数
    '''
    def __init__(self, id='', date='', page = 1):
        self.id = id
        self.page = page
        if (date == ''):
            self.date = time.strftime('%Y-%m-%d')
        self.div = None
        self.commentList = []
        self.wordDict = {}

    def _getHeader(self):
        return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
        }

    def setConfig(self, id, date, page=1):
        """
        id: int 基金id
        date: string 日期
        page: int 页数
        """
        self.id = id
        self.date = date
        self.page = page

    def initCookie(self):
        host = 'http://guba.eastmoney.com/'
        headerDict = self._getHeader()
        rq = urlopen(host, headers=headerDict)

    def sendRequest(self):
        '''
        发起请求，需要设置 基金id 分页可选page
        获取的数据会放到self.div
        '''
        id = self.id
        if (self.id==''):
            print('please set fund id first')
            exit(1)
        page = self.page
        if (page == 1):
            self.url = "http://guba.eastmoney.com/list,of{0}.html".format(id)
        else:
            self.url = "http://guba.eastmoney.com/list,of{0}_{1}.html".format(id, page)
        try:
            headerDict = self._getHeader()
            rqObj = urllib.request.Request(self.url, headers=headerDict)
            self.content = urlopen(rqObj)
            self.soup = BeautifulSoup(self.content, 'lxml')
            self.div = self.soup.select("div[class=articleh]")
            rt = random.random() * 3
            time.sleep(rt)

        except Exception as err:
            self.div = None
            print('can\'t get content, request fail : code=' + repr(err))

    def countComment(self,  date = ''):
        '''
        统计评论数和阅读量的数据
        '''
        if (self.div == None):
            self.sendRequest()
        if (date == ''):
            date = self.date
        compareDate = time.strptime(date, '%Y-%m-%d')
        compareTs = time.mktime(compareDate)
        count = 0
        readingCount = 0
        ts = 0
        for comment in self.div:
            if comment.find_all('em', class_='settop') : #跳过置顶的评论
                continue
            elif comment.find_all('em', class_='hinfo') : #跳过公告
                continue
            try:
                commentDate = comment.contents[6].string[:5]
                reading = comment.contents[1].string
                commentTitle = comment.contents[3].string
                if (commentTitle!=None):
                    self.commentList.append(commentTitle)
                year = time.strftime('%Y')
                tsGroup = time.strptime(year+'-'+commentDate, '%Y-%m-%d')
                ts = time.mktime(tsGroup)
            except Exception as err:
                ts = compareTs - 1000
                print('parse error, skip !!!' )
            if (ts == compareTs):
                count+=1
                readingCount+=int(reading)
        if (ts >= compareTs) :
            self.getNextPage()
            print(commentDate+' id = '+repr(self.id)+' get next page = ' + repr(self.page))
            if (self.page >= 50):
                return {'ccount':count,'reading':readingCount}
            dictCount = self.countComment()
            count += dictCount['ccount']
            readingCount += dictCount['reading']
        return {'ccount':count,'reading':readingCount}

    def getCommentTitle(self):
        commentStr = []
        for comment in self.div:
            year = time.strftime('%Y')
            commentDate = year+'-'+comment.contents[6].string[:5]
            child = comment.a.string
            commentStr.append({'date':commentDate, 'title': child})
        return commentStr

    def getNextPage(self):
        '''
        获取下一页数据
        '''
        self.page += 1
        self.sendRequest()

    def clearComment(self):
        '''
        清除评论数据
        '''
        self.commentList = []
        self.wordDict = {}

    def divideWord(self):
        '''
        分词统计
        '''
        print('analysis word')
        for c in self.commentList:
            clist = jieba.lcut(c, cut_all=False)
            # print(c +' => '+repr(clist))
            for w in clist:
                if w in self.wordDict:
                    self.wordDict[w] += 1
                else:
                    self.wordDict[w] = 1
        formatList = self.formatWord()
        # save to file
        basePath = os.path.abspath('../public/funddata/tagcloud/'+self.date)
        if os.path.isdir(basePath) != True:
            os.mkdir(basePath)
        savePath = os.path.abspath(basePath+'/'+self.id+'.json')
        with open(savePath, 'w+') as fp:
            fp.write(json.dumps(formatList))
        return formatList

    def formatWord(self):
        '''
        格式化分词dict到合适的前端格式
        return List
        '''
        formatList = []
        ignoreWord = [
            "你","我","他","的","是","你们","我们","他们","大家","人",
            "，","了","?","？","。","!","！",",","、",",",
            "不","啊","呢","么","吗","吧"," "
        ]
        for w in self.wordDict:
            if w in ignoreWord:
                continue
            elif self.wordDict[w] <= 1: #过滤低频字词
                continue
            formatList.append({"text": w, "weight": self.wordDict[w]})
        
        return formatList