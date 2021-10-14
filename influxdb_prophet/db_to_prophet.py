# -------------------------------------------------------------------------------------------
# 라이브러리 선언
import pprint
from influxdb import InfluxDBClient
import pandas as pd
from pandas import json_normalize
from matplotlib import pyplot as plt
import re
from fbprophet import Prophet
# -------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------
# influxdb 클라이언트 생성 함수
def get_ifdb( host='180.70.53.4', port=11334, user='root', passwd='root'):
    # client 객체 생성, 해당 객체는 influxdb에 연결하기 위한 정보를 포함함
    client = InfluxDBClient(host, port, user, passwd, database='test1')

    return client
# -------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------
# 아두이노에서 받은 데이터를 influxdb 클라이언트에 저장
def get_data(ifdb):
    tablename = 'my_table'
    # influxdb데이터를 불러와 터미널에 출력
    result = ifdb.query('select * from %s order by time desc' % tablename)

    return result
# -------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------
# 메인 함수
def do_test():
    mydb = get_ifdb()
    df = get_data(mydb)
    # 해당 클라이언트로 작업(my_test) 수행

    result = list(df.get_points('my_table'))
    # display(result)
    df = json_normalize(result)

    df['ds1'] = df['time'].apply(lambda x: re.sub(r'T', ' ', str(x)))
    df['ds'] = df['ds1'].apply(lambda x: re.sub(r'Z', ' ', str(x)))

    df = df.rename(columns={"temp":"y"})
    df = df.drop(columns=df.columns.difference(['ds','y']))

    print(df.head())

    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=1, freq='1min')

# -------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------
# 시작함수
if __name__ == '__main__':
    do_test()
# -------------------------------------------------------------------------------------------
