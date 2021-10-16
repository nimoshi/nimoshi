
# 모듈 불러오기
from influxdb import InfluxDBClient
from pandas import json_normalize
from matplotlib import pyplot
from fbprophet import Prophet
import re

# 필요한 DB 생성
client = InfluxDBClient(host='180.70.53.4', port=11334, username='root', password='root' , database='moniter2')
tablename = 'tempAOhumi'

#
rs = client.query('select * from %s order by time desc' %tablename)
# display(rs)

result = list(rs.get_points('tempAOhumi'))
# display(result)



df = json_normalize(result)
df


df.plot()
pyplot.show()


df['ds1'] = df['time'].apply(lambda x: re.sub(r'T', ' ', str(x)))
df['ds'] = df['ds1'].apply(lambda x: re.sub(r'Z', ' ', str(x)))

df=df.rename(columns={"temp_O":"y"})
df=df.drop(columns=df.columns.difference(['ds','y']))
df=df[['ds','y']]



m = Prophet()
m.fit(df)
future = m.make_future_dataframe(periods=1, freq='1min')
