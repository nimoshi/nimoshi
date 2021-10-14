from fbprophet import Prophet
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import mean_absolute_error

df = pd.read_csv('./electric_margin.csv', encoding='utf-8', header = 0)
df = df.drop(['주택용','교육용','산업용','농사용','일반용','가로등','심야'], axis='columns')

# df.columns = ['year','margin']
# print(df.head())
# df.plot()
# plt.show()

df.columns = ['ds','y']
df['ds'] = pd.to_datetime(df['ds'])

model=Prophet()
model.fit(df)

# --------------------- in sample forecast ----------------------------------
last_5year = list()
for i in range(2016,2021):
    last_5year.append(['%04d' % i + '-01-01'])
last_5year = pd.DataFrame(last_5year, columns=['ds'])
last_5year['ds']= pd.to_datetime(last_5year['ds'])
forecast = model.predict(last_5year)

model.plot(forecast)
plt.title('in-sample-forecast')
plt.show()
# ----------------------------------------------------------------------------


# --------------------- out of sample forecast -------------------------------
over_5year = list()
for i in range(2021,2026):
    over_5year.append(['%04d' % i + '-01-01'])
over_5year = pd.DataFrame(over_5year, columns=['ds'])
over_5year['ds']= pd.to_datetime(over_5year['ds'])
forecast = model.predict(over_5year)

model.plot(forecast)
plt.title('out-of-sample-forecast')
plt.show()
# ----------------------------------------------------------------------------


# --------------------- model comparision ------------------------------------
train = df.drop(df.index[-5:])
y_true = df['y'][-5:].values
model = Prophet()
model.fit(train)
model_5year = list()
for i in range(2016,2021):
    model_5year.append(['%04d' % i + '-01-01'])
model_5year = pd.DataFrame(model_5year, columns = ['ds'])
model_5year['ds'] = pd.to_datetime(model_5year['ds'])
forecast= model.predict(model_5year)
y_pred = forecast['yhat'].values
MAE = mean_absolute_error(y_true, y_pred)
print('MAE : %.3f' % MAE)
# 실제 데이터와 예측 데이터를 그래프를 통해 비교
plt.plot(y_true, label = 'Actual')
plt.plot(y_pred, label = 'Predicted')
plt.title('model-comparision')
plt.legend()
plt.show()

