# 출처 : https://dining-developer.tistory.com/25

# --------------모듈 불러오기 --------------------------------------------------
from fbprophet import Prophet
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import mean_absolute_error
# ---------------------------------------------------------------------------


# -------------- csv 데이터 불러오기 -------------------------------------------
df = pd.read_csv('./monthly-car-sales.csv', header=0)
# ---------------------------------------------------------------------------


# -------------- 데이터 확인 --------------------------------------------------
# 데이터 읽어오기
print(df.shape)
print(df.head())

print(df.info())

# 데이터 시각화
df.plot()
plt.show()
# ---------------------------------------------------------------------------


# -------------- prophet 모델 학습시키기 ---------------------------------------
# 컬럼명 변경 (month -> ds, Sales -> y)
df.columns = ['ds', 'y']
# 데이터 타입 변경(to_datetime() : 데이터 타입을 변환하는 함수로 int64 형태를 datetime64로 변환)
df['ds'] = pd.to_datetime(df['ds'])
# 모델 생성
model = Prophet()
# 모델 학습
model.fit(df)
# ---------------------------------------------------------------------------


# -------------- In-Sample Forecast(표본을 통한 사전예측) -----------------------
# 마지막 1년('68)의 월별 리스트 생성
last_1year = list()
for i in range(1,13):
    last_1year.append(['1968-%02d' % i])
last_1year = pd.DataFrame(last_1year, columns = ['ds'])
last_1year['ds'] = pd.to_datetime(last_1year['ds'])
# 예측
forecast = model.predict(last_1year)
# ---------------------------------------------------------------------------


# -------------- 사전 예측 데이터 출력  ----------------------------------------
# 예측 데이터 forecast의 칼럼 yhat, yhat_lower, yhat_upper 확인
print(forecast[['ds','yhat','yhat_lower','yhat_upper']].head())
# 플롯 확인
model.plot(forecast)
plt.show()
# ---------------------------------------------------------------------------


# -------------- Out-of-Sample Forecast(표본을 통한 사후예측) -------------------
# 향후 1년('69)의 월별 리스트 생성
over_1year = list()
for i in range(1,13):
    over_1year.append(['1969-%02d' % i])
over_1year = pd.DataFrame(over_1year, columns = ['ds'])
over_1year['ds'] = pd.to_datetime(over_1year['ds'])
# 예측
forecast = model.predict(over_1year)
# ---------------------------------------------------------------------------


# -------------- 사후 예측 데이터 그래프 출력 ------------------------------------
model.plot(forecast)
plt.show()
# ---------------------------------------------------------------------------


# -------------- 모델 평가하기 ------------------------------------------------
# 마지막 12개월('68) 제외시키기
train = df.drop(df.index[-12:])
y_true = df['y'][-12:].values
# 모델 생성 후 학습
model = Prophet()
model.fit(train)
# train set 마지막 1년 날짜 생성
model_1year = list()
for i in range(1,13):
    model_1year.append(['1968-%02d' % i])
model_1year = pd.DataFrame(model_1year, columns = ['ds'])
model_1year['ds'] = pd.to_datetime(model_1year['ds'])
# 예측 데이터인 MAE 확인
forecast= model.predict(model_1year)
y_pred = forecast['yhat'].values
MAE = mean_absolute_error(y_true, y_pred)
print('MAE : %.3f' % MAE)
# 실제 데이터와 예측 데이터를 그래프를 통해 비교
plt.plot(y_true, label = 'Actual')
plt.plot(y_pred, label = 'Predicted')
plt.legend()
plt.show()
# ---------------------------------------------------------------------------
