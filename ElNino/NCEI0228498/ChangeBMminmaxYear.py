# 백화현상 min, max만 사용해서 분석
# Percent_Bleached열 >%와 같은 셀 존재 문제
# TODO: min max 간의 간극을 어떻게 조정해야 할지?
# 폐기

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

data = pd.read_csv("data\Global_Coral_Bleaching_Database.csv")

data['MIN_PERCENT_BLEACHED'] = pd.to_numeric(data['MIN_PERCENT_BLEACHED'], errors='coerce')
data['MAX_PERCENT_BLEACHED'] = pd.to_numeric(data['MAX_PERCENT_BLEACHED'], errors='coerce')

# 연도별 최소 백화 비율과 최대 백화 비율의 평균 계산
annual_min_max_bleaching = data.groupby('YEAR').agg({
    'MIN_PERCENT_BLEACHED': 'mean',
    'MAX_PERCENT_BLEACHED': 'mean'
}).reset_index()

plt.figure(figsize=(10, 6))
plt.plot(annual_min_max_bleaching['YEAR'], annual_min_max_bleaching['MIN_PERCENT_BLEACHED'], label='Average Min Percent Bleached', color='b')
plt.plot(annual_min_max_bleaching['YEAR'], annual_min_max_bleaching['MAX_PERCENT_BLEACHED'], label='Average Max Percent Bleached', color='r')

plt.title('Change in Min and Max Coral Bleaching Percent Over Time')
plt.xlabel('Year')
plt.ylabel('Percentage (%)')
plt.legend()
plt.grid(True)
plt.show()


# 추세분석(안됨)
annual_min_max_bleaching_clean = annual_min_max_bleaching.dropna()
X_clean = annual_min_max_bleaching_clean['YEAR'].values.reshape(-1, 1)

# 최소 백화 비율에 대한 선형 회귀
min_model_clean = LinearRegression()
min_model_clean.fit(X_clean, annual_min_max_bleaching_clean['MIN_PERCENT_BLEACHED'])
min_trend_line_clean = min_model_clean.predict(X_clean)

# 최대 백화 비율에 대한 선형 회귀
max_model_clean = LinearRegression()
max_model_clean.fit(X_clean, annual_min_max_bleaching_clean['MAX_PERCENT_BLEACHED'])
max_trend_line_clean = max_model_clean.predict(X_clean)

plt.figure(figsize=(10, 6))

plt.plot(annual_min_max_bleaching_clean['YEAR'], annual_min_max_bleaching_clean['MIN_PERCENT_BLEACHED'], label='Average Min Percent Bleached', color='b')
plt.plot(annual_min_max_bleaching_clean['YEAR'], min_trend_line_clean, label='Min Percent Trend', color='b', linestyle='--')

plt.plot(annual_min_max_bleaching_clean['YEAR'], annual_min_max_bleaching_clean['MAX_PERCENT_BLEACHED'], label='Average Max Percent Bleached', color='r')
plt.plot(annual_min_max_bleaching_clean['YEAR'], max_trend_line_clean, label='Max Percent Trend', color='r', linestyle='--')

plt.title('Trend Analysis of Min and Max Coral Bleaching Percent Over Time')
plt.xlabel('Year')
plt.ylabel('Percentage (%)')
plt.legend()
plt.grid(True)
plt.show()

#기울기, 절편
min_slope_clean, min_intercept_clean = min_model_clean.coef_[0], min_model_clean.intercept_
max_slope_clean, max_intercept_clean = max_model_clean.coef_[0], max_model_clean.intercept_

min_slope_clean, max_slope_clean, min_intercept_clean, max_intercept_clean