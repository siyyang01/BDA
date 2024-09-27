import matplotlib.pyplot as plt
import pandas as pd

data = pd.read_csv('data\SSTAnomalies.csv')

plt.figure(figsize=(10, 6))

# TOTAL
plt.plot(data['YEAR'] + (data['MON'] - 1) / 12, data['TOTAL'], label='TOTAL', marker='o', color='b')

# CLIMADJUST
# plt.plot(data['YEAR'] + (data['MON'] - 1) / 12, data['ClimAdjust'], label='ClimAdjust', marker='o', color='r')

special_years = [(1982, 1), (1983, 12), (1997, 1), (1998, 12), (2014, 1), (2016, 12)]
for year, month in special_years:
    plt.axvline(x=year + (month - 1) / 12, color='lightgreen', linestyle='--', lw=2)

plt.title('TOT,ClimAdjust', fontsize=15)
plt.xlabel('Year)', fontsize=12)
plt.ylabel('Value', fontsize=12)
plt.legend()

# 그래프 출력
plt.grid(True)
plt.show()