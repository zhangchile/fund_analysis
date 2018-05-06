# coding=utf-8
import time
import json
import re
import os.path
from bs4 import BeautifulSoup
from urllib.request import urlopen

class AnalysisFundId():
    '''
    获取基金id及排行列表
    '''
    def __init__(self, date = ''):
        if (date!=''):
            self.date = date
        else:
            self.date = time.strftime('%Y-%m-%d')
        self.path = os.path.abspath('../public/funddata/ranklist_'+self.date+'.json')
        
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
            },
            {
                'ft': 'gp',
                'sc': '3y',
                'pi': 1,
                'pn': 100
            },
            {
                'ft': 'gp',
                'sc': 'y',
                'pi': 1,
                'pn': 100
            },
            {
                'ft': 'gp',
                'sc': 'z',
                'pi': 1,
                'pn': 100
            },
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
        with open(self.path, 'w+') as fp:
            fp.write(json.dumps(dictObj))

        return dictObj
        