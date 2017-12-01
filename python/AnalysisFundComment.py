import time
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
        self.content = urlopen(self.url)
        self.soup = BeautifulSoup(self.content, 'lxml')
        self.div = self.soup.select("div[class=articleh]")

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
            if (comment.find_all('em', class_='settop')) : #跳过置顶的评论
                continue
            commentDate = comment.contents[6].string[:5]
            reading = comment.contents[1].string
            try:
                tsGroup = time.strptime('2017-'+commentDate, '%Y-%m-%d')
                ts = time.mktime(tsGroup)
            except Exception :
                ts = compareTs - 1000
                print('date error, skip  :' + commentDate)
            if (ts == compareTs):
                count+=1
                readingCount+=int(reading)
        if (ts >= compareTs) :
            self.getNextPage()
            print(commentDate+' id = '+repr(self.id)+' get next page = ' + repr(self.page))
            if (self.page >=50):
                return {'ccount':count,'reading':readingCount}
            dictCount = self.countComment()
            count += dictCount['ccount']
            readingCount += dictCount['reading']
        return {'ccount':count,'reading':readingCount}

    def getCommentTitle(self):
        commentStr = []
        for comment in self.div:
            commentDate = '2017-'+comment.contents[6].string[:5]
            child = comment.a.string
            commentStr.append({'date':commentDate, 'title': child})
        return commentStr

    def getNextPage(self):
        '''
        获取下一页数据
        '''
        self.page += 1
        self.sendRequest()
