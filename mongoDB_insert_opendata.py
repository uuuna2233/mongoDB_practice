import urllib.request as urllib
import json
import pymongo


# 以 api 金鑰取得資料權限

api_key = 'e8dd42e6-9b8b-43f8-991e-b3dee723a52d'
url = 'https://data.epa.gov.tw/api/v2/aqx_p_432?api_key=' + api_key + '&limit=1000&sort=ImportDate%20desc&format=json'

# 以 urlopen 函數處理 url 響應的對象
# requests.get(url).text 也能夠解析出漂亮的 json 文檔

response = urllib.urlopen(url)
text = response.read().decode('utf-8') # 將二進位制型別 bytes 編碼為 utf-8

text = text.replace('pm2.5', 'pm2_5').replace('pm2.5_avg', 'pm2_5_avg')  # field name 不能有 dot

jsonObj = json.loads(text) # 將以編碼的 JSON 字符串解碼為 Python 對象


# 將資料存進 opendata 資料庫中的 AQI 資料表

client = pymongo.MongoClient()
db = client.opendata
db.AQI.insert_many(jsonObj['records'])



