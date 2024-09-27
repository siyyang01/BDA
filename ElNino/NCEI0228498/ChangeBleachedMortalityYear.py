# 백화현상, 사망률 추세분석

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression
import numpy as np

data = pd.read_csv("data\Global_Coral_Bleaching_Database.csv")

data['PERCENT_BLEACHED'] = pd.to_numeric(data['PERCENT_BLEACHED'], errors='coerce')
data['PERCENT_MORTALITY'] = pd.to_numeric(data['PERCENT_MORTALITY'], errors='coerce')

annual_bleaching_mortality = data.groupby('YEAR').agg({
    'PERCENT_BLEACHED': 'mean',
    'PERCENT_MORTALITY': 'mean'
}).reset_index()

plt.figure(figsize=(10, 6))

# 백화 비율, 사망률 시각화
plt.plot(annual_bleaching_mortality['YEAR'], annual_bleaching_mortality['PERCENT_BLEACHED'], label='Average Percent Bleached', color='b')
plt.plot(annual_bleaching_mortality['YEAR'], annual_bleaching_mortality['PERCENT_MORTALITY'], label='Average Percent Mortality', color='r')

plt.title('Change in Coral Bleaching and Mortality Over Time')
plt.xlabel('Year')
plt.ylabel('Percentage (%)')
plt.legend()
plt.grid(True)
plt.show()


