import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("data\Processed_Zero_Coral_Bleaching_Database.csv")

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
