import pymongo
from pprint import *
import re

client = pymongo.MongoClient()
db = client.opendata

'''
查詢各縣市觀測站 AQI 指數，由大排到小，並僅輸出特定欄位
'''

# projection：除了 _id 欄位外，其他欄位的 1 與 0 為互斥
# sort：反向排序 -1
# The use of "**" operator to unpack the values.

Projection = {'county':1, 'sitename':1, 'aqi':1, '_id':0}
for doc in db.AQI.find({}, projection = Projection).sort('aqi', -1):
    print('---------------')
    print('{county}{sitename}: {aqi}'.format(**doc))  
    
    
'''
查詢彰、雲、嘉地區觀測站 pm2.5 指數，利用包含運算子 $in 和 模糊查詢 $regex
'''

# $in：包含運算子，查詢在陣列中的資料
# $regex：正規表示法進行模糊查詢

Projection = {'county':1, 'sitename':1, 'pm2_5':1, '_id':0}

cursor = db.AQI.find({'county':{'$in':[re.compile('彰化'), re.compile('雲林'), re.compile('嘉義')]}}, projection = Projection)

pprint(list(cursor)) 


'''
查詢 AQI 值大於 50 小於 100 的資料
'''

# where()中的語法是 JavaScript

Projection = {'county':1, 'sitename':1, 'aqi':1, '_id':0}

cursor = db.AQI.find({}, projection = Projection).where('parseInt(this.aqi) >= 50 && parseInt(this.aqi) < 100')

pprint(list(cursor)) 


'''
若沒加上可選參數 upsert，即使沒有與 query 相符的 sitename，也不會新增資料
'''

# upsert 為布林值，預設為 False

db.AQI.update_one({'sitename':'榕樹下'},{'$set':{'aqi':'100'}})
db.AQI.update_one({'sitename':'橋頭邊'},{'$set':{'aqi':'0'}},upsert=True)
cursor = db.AQI.find({'sitename':{'$in':['榕樹下','橋頭邊']}})

for document in cursor:
    pprint(document)


'''
刪除最新一筆資料
'''

no1 = db.AQI.find({}).sort('_id',-1)
_id = no1[0]['_id']


query = {'_id':_id}
result = db.AQI.delete_one(query) 
cursor = db.AQI.find({'sitename':'橋頭邊'})

if result.acknowledged:
    print(list(cursor))
    print('delete {} documents'.format(result.deleted_count))
    