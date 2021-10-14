from fbprophet import Prophet
import pandas as pd
from matplotlib import pyplot as plt

df = pd.read_csv('./temp.csv', header = 0)


df = df.drop(['week'], axis = 'columns')
# print(df.head())

df.columns = ['ds', 'y']
df['ds'] = pd.to_datetime(df['ds'])

# ------------------------------- 마지막 7일 사전 예측 비교 --------------------------------------------
train = df.drop(df.index[-7:])
y_true = df['y'][-7:].values
model = Prophet()
model.fit(train)

model_1month = list()
for i in range(25,32):
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

