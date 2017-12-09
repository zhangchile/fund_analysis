# this is app entry 

import time
import json
import re
import os.path
import random
from AnalysisFundComment import *
from AnalysisFundId import *

# 判断时间 0点到9点不访问
hour = int(time.strftime('%H'))
if hour < 10:
    print('hour = ' + str(hour) + ' < 10, system exit')
    exit(0)

#当前文件路径,并切换
dir = os.path.dirname(__file__)
if dir != '':
    os.chdir(dir)

idHandler = AnalysisFundId()
# 暂存list
ids = idHandler.getIdList()
rankdict = idHandler.getRankList()
print(len(ids))

page = 1
date = time.strftime('%Y-%m-%d')
# fundID = 160222
countPath = '../public/funddata/fundcount_'+date+'.json'
# comment = AnalysisFundComment(fundID, date, page)
# print(comment.countComment())
if(os.path.isfile(countPath)==''):
    cf = open(countPath)
    idMap = json.load(cf)
else:
    comment = AnalysisFundComment()
    idMap = []
    # ids = ['161725']#['161725']
    for id in ids:

        print(id, date)
        comment.setConfig(id, date)
        comment.sendRequest()
        count = comment.countComment()
        if (count['ccount'] > 30):
            idMap.append({'id':id, 'name':rankdict[id], 'count':count['ccount'],'reading':count['reading']})
            #分析评论
            comment.divideWord()
        print(time.strftime('%Y-%m-%d %H:%M:%S') + ' count fund name= '+rankdict[id]+' value='+repr(count))
        comment.clearComment()

        rtime = random.random() * 6
        time.sleep(rtime)

    path = os.path.abspath('../public/funddata/fundcount_'+date+'.json')
    fp = open(path,'w+')
    fp.write(json.dumps(idMap))
    fp.close()

    print('complete')

