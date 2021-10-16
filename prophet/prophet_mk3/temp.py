from fbprophet import Prophet
import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('./temp.csv', header = 0)


df = df.drop(['week'], axis = 'columns')
# print(df.head())
df.plot()
plt.show()

df.columns = ['ds', 'y']
df['ds'] = pd.to_datetime(df['ds'])


# ------------------------------- 3월 달 사전 예측 비교 --------------------------------------------
train = df.drop(df.index[-31:])
y_true = df['y'][-31:].values
model = Prophet()
model.fit(train)

model_1month = list()
for i in range(1,32):
    model_1month.append(['2021-03-%02d' % i])
model_1month = pd.DataFrame(model_1month, columns = ['ds'])
model_1month['ds'] = pd.to_datetime(model_1month['ds'])

forecast = model.predict(model_1month)
y_pred= forecast['yhat'].values

plt.plot(y_true, label = 'Actual')
plt.plot(y_pred, label = 'Predicted')
plt.legend()
plt.show()
# -----------------------------------------------------------------------------------------------


# -------------- In-Sample Forecast(표본을 통한 사전예측) -----------------------
# 마지막 1년('68)의 월별 리스트 생성
last_1year = list()
for i in range(1,32):
    last_1year.append(['2021-03-%02d' % i])
last_1year = pd.DataFrame(last_1year, columns = ['ds'])
last_1year['ds'] = pd.to_datetime(last_1year['ds'])
# 예측
forecast = model.predict(last_1year)
model.plot(forecast)
df.plot()
plt.show()
# ---------------------------------------------------------------------------



