#SST 기초통계량

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import het_breuschpagan


file_path = 'data/SSTAnomalies.csv'

sst_data = pd.read_csv(file_path)


monthly_stats = sst_data.groupby('MON').agg({
    'TOTAL': ['mean', 'std', 'min', 'max'],
    'ANOM': ['mean', 'std', 'min', 'max']
})

print(monthly_stats)

# 기초통계량 결과
'''
SST and Anomaly Statistics:
         TOTAL                                  ANOM
          mean       std    min    max          mean       std   min   max
MON
1    26.431600  1.110729  24.47  29.11 -1.493333e-02  1.102472 -1.95  2.56
2    26.641600  0.918143  25.07  29.00 -4.933333e-03  0.909968 -1.66  2.24
3    27.144800  0.709944  25.86  28.90 -5.921189e-18  0.698901 -1.21  1.61
4    27.593067  0.626211  26.29  29.02 -8.666667e-03  0.597371 -1.11  1.32
5    27.699067  0.620000  26.19  28.97 -1.533333e-02  0.592387 -1.37  1.18
6    27.517733  0.625470  25.99  28.90  2.853333e-02  0.598294 -1.44  1.22
7    27.087333  0.689734  25.56  28.85  3.520000e-02  0.665896 -1.45  1.67
8    26.675067  0.787077  25.23  28.78  2.853333e-02  0.767375 -1.38  1.93
9    26.563243  0.889849  25.05  28.92  3.675676e-02  0.867718 -1.59  2.20
10   26.533378  1.033506  24.41  29.07  4.716216e-02  1.014925 -1.71  2.40
11   26.523784  1.133062  24.25  29.41  4.216216e-02  1.117333 -2.09  2.71
12   26.468649  1.163851  24.34  29.26  1.445946e-02  1.152014 -2.06  2.65
'''


# anom 추세선
annual_anomaly_trend = sst_data.groupby('YEAR')['ANOM'].mean()

# 선형회귀
annual_anomaly_trendR = sst_data.groupby('YEAR')['ANOM'].mean().reset_index()

# 이동평균계산
annual_anomaly_trendR['Moving_Avg'] = annual_anomaly_trendR['ANOM'].rolling(window=5).mean()

# 연도별 이상치 평균 시계열 분해
anomaly_series = pd.Series(annual_anomaly_trendR['ANOM'].values, index=annual_anomaly_trendR['YEAR'])
decomposition = sm.tsa.seasonal_decompose(anomaly_series, period=12, model='additive') #STL
# 잔차
residual = decomposition.resid


X = annual_anomaly_trendR['YEAR'].values.reshape(-1, 1)
y = annual_anomaly_trendR['ANOM'].values

model = LinearRegression()
model.fit(X, y)

trend_line = model.predict(X)


# 시계열 분해요소
trend = decomposition.trend
seasonal = decomposition.seasonal
residual = decomposition.resid

print("==== 시계열 분석 결과 ====")
print("1. 추세(Trend):")
print(trend.dropna().to_string())

print("\n2. 계절성(Seasonality):")
print(seasonal.dropna().to_string())

print("\n3. 잔차(Residuals):")
print(residual.dropna().to_string())

print("\n==== 추가 통계 정보 ====")
print(f"추세(Trend)의 평균: {trend.mean():.4f}")
print(f"계절성(Seasonality)의 평균: {seasonal.mean():.4f}")
print(f"잔차(Residuals)의 평균: {residual.mean():.4f}")


'''
#모르겠음
# 이분산성 테스트
annual_anomaly_trendR_const = sm.add_constant(annual_anomaly_trendR[['YEAR']])
annual_anomaly_trendR_const = annual_anomaly_trendR_const.loc[residual.index] #크기맞추기 결측값제거
test = het_breuschpagan(residual.dropna(), annual_anomaly_trendR_const)
print('Breusch-Pagan Test Statistic: {:.4f}'.format(test[0]))
print('p-value: {:.4f}'.format(test[1]))

if test[1] < 0.05:
    print("ㅇ")
else:
    print("ㄴ")
'''


'''
# 그래프
plt.figure(figsize=(10, 6))
plt.plot(annual_anomaly_trend.index, annual_anomaly_trend.values, label='Annual Mean Anomaly', color='b')
plt.plot(annual_anomaly_trendR['YEAR'], trend_line, label='Linear Trend', color='r', linestyle='--')
plt.plot(annual_anomaly_trendR['YEAR'], annual_anomaly_trendR['Moving_Avg'], label='5-Year Moving Average', color='r')
decomposition.plot()

plt.title('Long-term Trend of SST Anomalies')
plt.xlabel('Year')
plt.ylabel('Mean Anomaly')
plt.grid(True)
plt.legend()
plt.show()

# 시각화를 통해 잔차에서 패턴이 있는지 확인
# 잔차 시각화
plt.figure(figsize=(10, 6))
plt.plot(annual_anomaly_trendR['YEAR'], residual, label='Residuals', color='blue')
plt.title('Residuals Over Time')
plt.xlabel('Year')
plt.ylabel('Residuals')
plt.grid(True)
plt.legend()
plt.show()


# 비정상적 사건 탐지
threshold = residual.std() * 2  # 임계값
outliers = residual[abs(residual) > threshold]

print("비정상 연도:")
print(outliers)
'''

'''
#테스트용
# ACF(자기상관 함수) 시각화
plot_acf(residual.dropna(), lags=40)
plt.title('Autocorrelation of Residuals')
plt.show()

# PACF(부분자기상관 함수) 시각화
plot_pacf(residual.dropna(), lags=20)
plt.title('Partial Autocorrelation of Residuals')
plt.show()

# 히스토그램을 통해 잔차 분포 확인
plt.figure(figsize=(10, 6))
plt.hist(residual.dropna(), bins=30, edgecolor='black')
plt.title('Histogram of Residuals')
plt.xlabel('Residuals')
plt.ylabel('Frequency')
plt.show()

# Q-Q 플롯을 통해 정규분포 여부 확인
sm.qqplot(residual.dropna(), line='45')
plt.title('Q-Q Plot of Residuals')
plt.show()
'''



'''
추세: 평균 0.0174 약간의 증가추세, 장기적으로 해양 온도 이상치가 증가할 가능성
계절성: 0에 가까움. 연도간 일정한 변동있음
잔차: 주기적인 변동 제외 나머지 변동이 크지않음
'''
