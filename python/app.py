# this is app entry 

import time
import json
import re
import os.path
from AnalysisFundComment import *
from AnalysisFundId import *

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
rankdict = idHandler.getRankList()
print(len(ids))

page = 1
date = '2017-11-30' #time.strftime('%Y-%m-%d')
fundID = 160222
countPath = '../public/funddata/fundcount_'+date+'.json'
# comment = AnalysisFundComment(fundID, date, page)
# print(comment.countComment())
if(os.path.isfile(countPath)):
    cf = open(countPath)
    idMap = json.load(cf)
else:
    comment = AnalysisFundComment()
    idMap = []
    # ids = [160222]
    for id in ids:
        # time.sleep(1)
        comment.setConfig(id, date)
        comment.sendRequest()
        count = comment.countComment()
        if (count['ccount'] > 30):
            idMap.append({'id':id, 'name':rankdict[id], 'count':count['ccount'],'reading':count['reading']})
        print('count fund name= '+rankdict[id]+' id='+ repr(id) + ' value='+repr(count))

    path = os.path.abspath('../public/funddata/fundcount_'+date+'.json')
    fp = open(path,'w+')
    fp.write(json.dumps(idMap))
    fp.close()

    print('complete')

# 排序 dict
for i in idMap:
    print(i)
    pass