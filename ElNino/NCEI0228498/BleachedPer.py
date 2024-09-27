import matplotlib.pyplot as plt
import pandas as pd

file_path = 'data\Global_Coral_Bleaching_Database.csv'

data = pd.read_csv(file_path)

filtered_data = data[['YEAR', 'MIN_PERCENT_BLEACHED', 'MAX_PERCENT_BLEACHED']].dropna()

filtered_data['YEAR'] = pd.to_numeric(filtered_data['YEAR'], errors='coerce')
filtered_data['MIN_PERCENT_BLEACHED'] = pd.to_numeric(filtered_data['MIN_PERCENT_BLEACHED'], errors='coerce')
filtered_data['MAX_PERCENT_BLEACHED'] = pd.to_numeric(filtered_data['MAX_PERCENT_BLEACHED'], errors='coerce')

annual_bleaching = filtered_data.groupby('YEAR').mean()

# 시계열 데이터 시각화
plt.figure(figsize=(10, 6))
plt.plot(annual_bleaching.index, annual_bleaching['MIN_PERCENT_BLEACHED'], label='Min Percent Bleached', marker='o')
plt.plot(annual_bleaching.index, annual_bleaching['MAX_PERCENT_BLEACHED'], label='Max Percent Bleached', marker='o')
plt.title('Annual Coral Bleaching (Min and Max Percent)')
plt.xlabel('Year')
plt.ylabel('Percentage Bleached')
plt.grid(True)
plt.legend()
plt.show()
