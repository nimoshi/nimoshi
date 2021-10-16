# -------------------------------------------------------------------------------------------
# 라이브러리 선언
from datetime import datetime, timedelta
from pytz import timezone, utc
import pprint
import time
from influxdb import InfluxDBClient
from copy import deepcopy
import serial

# -------------------------------------------------------------------------------------------

device = 'COM3'

# -------------------------------------------------------------------------------------------
# influxdb 클라이언트 생성 함수
def get_ifdb(db, host='180.70.53.4', port=11334, user='root', passwd='root'):
    # client 객체 생성, 해당 객체는 influxdb에 연결하기 위한 정보를 포함함
    client = InfluxDBClient(host, port, user, passwd, db)

    try:
        # db 기반의 클라이언트 생성
        client.create_database(db)
        print('success')
    except:
        print('failed')
        pass
    return client


# -------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------
# 아두이노에서 받은 데이터를 influxdb 클라이언트에 저장
def my_test(ifdb, tA, tO, h):
    # json_body라는 세이브포인트(리스트) 생성
    json_body = []
    tablename = 'TempHumi'
    #fieldname = 'my_field'
    temp_A = tA
    temp_O = tO
    humi = h
    # point라는 이름의 딕셔너리(key와 value 쌍을 가지는 자료형) 생성
    # KST = timezone('Asia/Seoul')
    # # date = datetime.now()
    # now = datetime.utcnow()
    # dt = KST.localize(now)

    point = {
        "measurement": tablename,
        "tags": {
            #이부분에 값이 아니라 id
            "arduino_id": "moniter"
        },
        "fields": {
            # 데이터 0으로 초기화
            #fieldname: 0,
            "temp_A": temp_A,
            "temp_O": temp_O,
            "humi": humi,
        },
        "time": None,
    }


    # UTC 기준을 한국 표준시로 변경
    dt = datetime.utcnow() + timedelta(hours=9)
    date = dt.strftime("%Y-%m-%d %H:%M:%S")

    # 깊은 복사로 객체 복사
    np = deepcopy(point)
    np['time'] = date
    # 추가값이 저장된 np를 json에 스택 저장
    json_body.append(np)

    time.sleep(1)

    # for문에서 완성된 json_body를 influxdb에 저장함
    ifdb.write_points(json_body)

    # influxdb데이터를 불러와 result에 저장 및
    result = ifdb.query('select * from %s' % tablename)
    # 출력
    #pprint.pprint(result.raw)


# -------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------
# 메인(?) 함수
def do_test():
    arduino = serial.Serial(device, 9600)
    # mydb라는 이름을 가진 클라이언트 생성
    mydb = get_ifdb(db='env_moniter')
    # 해당 클라이언트로 작업(my_test) 수행
    while True:
        time.sleep(1)
        data = arduino.readline()
        # tA = float(data[0:4].decode())
        # tO = float(data[6:10].decode())
        # h = float(data[12:16].decode())

        tA = data[0:4].decode()
        tO = data[6:10].decode()
        h = data[12:16].decode()
        # if tA == "NaN" or tA.length < 0 or tA == 0 :
        #     a = 0


        pprint.pprint(f'현재 주변온도 {tA}°C , 접촉온도 {tO}°C , 습도 {h}% 입니다')
        # if t > 35:
        #     pprint.pprint(f'현재 온, 습도는 {t}°C, {h}% 이며 너무 덥습니다. 에어컨 ON')
        #     arduino.write(b'1\n')
        # elif 27 < t < 35:
        #     pprint.pprint(f'현재 온, 습도는 {t}°C, {h}% 이며 적당합니다. 에어컨 OFF')
        #     arduino.write(b'2\n')
        # elif t > 47:
        #     pprint.pprint(f'화재발생')
        #     arduino.write(b'0\n')
        # if h > 70:
        #     pprint.pprint(f'현재 온, 습도는 {t}°C, {h}% 이며 너무 습합니다. 팬 ON')
        #     arduino.write(b'3\n')
        # elif 40 < h < 70:
        #     pprint.pprint(f'현재 온, 습도는 {t}°C, {h}% 이며 적당합니다. 팬 OFF')
        #     arduino.write(b'4\n')
        # elif h < 40:
        #     pprint.pprint(f'현재 온, 습도는 {t}°C, {h}% 이며 너무 건조합니다. 물을 뿌립니다.')
        my_test(mydb, tA, tO, h)


# -------------------------------------------------------------------------------------------

# 메인함수 실행
if __name__ == '__main__':
    do_test()