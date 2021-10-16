# ----- 탬플릿 ---------------------------------------------------------

# --------------------------------------------------------------------------

# ----- 모듈 불러오기 ---------------------------------------------------------
import pandas as pd
from fbprophet import Prophet
from matplotlib import pyplot as plt
# --------------------------------------------------------------------------

# ----- csv 불러오기 ---------------------------------------------------------
df = pd.read_csv('./코로나바이러스감염증-19_확진환자_발생현황_210930.csv', encoding = 'UTF-8', header = 0)
# --------------------------------------------------------------------------

# ----- csv 데이터 수정 ------------------------------------------------------
df = df.drop([0])
df = df.drop(['국내발생(명)', '해외유입(명)', '사망(명)'], axis = 1)
df = df.replace('(.*),(.*)', r'\1\2', regex=True)
df = df.astype({'계(명)': int})
# --------------------------------------------------------------------------

# ----- csv 정보 확인 -------------------------------------------------------
print(df.columns)
print(df.head())
print(df.info())
# --------------------------------------------------------------------------

# ----- csv 플롯 출력 ---------------------------------------------------------
df.plot()
plt.show()
# --------------------------------------------------------------------------

# ----- prophet 모델 학습 ---------------------------------------------------------
df.columns = ['ds','y']
df['ds'] = pd.to_datetime(df['ds'])
model = Prophet()
model.fit(df)
# --------------------------------------------------------------------------

# ----- ISF 문 ---------------------------------------------------------
last_1month = list()
for i in range(1,31):
    last_1month.append(['2021-09-%02d' % i])
last_1month = pd.DataFrame(last_1month, columns = ['ds'])
last_1month['ds'] = pd.to_datetime(last_1month['ds'])
forecast = model.predict(last_1month)

model.plot(forecast)
plt.show()
# --------------------------------------------------------------------------

# ----- 모델 평가하기 --------------------------------------------------------------
train = df.drop(df.index[-30:])
y_ture = df['y'][-30:].values

model= Prophet()
model.fit(train)

model_1month = list()
for i in range(1, 31):
    model_1month.append(['2021-09-%02d' % i])
model_1month = pd.DataFrame(model_1month, columns=['ds'])
model_1month['ds'] = pd.to_datetime(model_1month['ds'])

forecast = model.predict(model_1month)
y_pred = forecast['yhat'].values

plt.plot(y_ture, label = 'Actual')
plt.plot(y_pred, label = 'Predicted')
plt.legend()
plt.show()
# --------------------------------------------------------------------------
