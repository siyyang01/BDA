import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("data\Processed_Zero_Coral_Bleaching_Database.csv")

data['MIN_PERCENT_BLEACHED'] = pd.to_numeric(data['MIN_PERCENT_BLEACHED'], errors='coerce')
data['MAX_PERCENT_BLEACHED'] = pd.to_numeric(data['MAX_PERCENT_BLEACHED'], errors='coerce')

'''
# 파란색 그래프 빨간색이랑 겹친건지 비어있는건지 모르겠음 10/1
# 원래 결측치 없었음
# 선형 보간법으로 비어있는 구간 채워넣음 (원본 결측치 0으로 미리 전처리한 데이터셋)
data['MIN_PERCENT_BLEACHED'] = data['MIN_PERCENT_BLEACHED'].interpolate(method='linear')
data['MAX_PERCENT_BLEACHED'] = data['MAX_PERCENT_BLEACHED'].interpolate(method='linear')

print(data[['MIN_PERCENT_BLEACHED', 'MAX_PERCENT_BLEACHED']].isna().sum())
'''

# 의미없어보이는 관측량(1960~1980) 그래프 삭제 10/1
filtered_data = data[data['YEAR'] >= 1980]

# 연도별 최소 백화 비율과 최대 백화 비율의 평균 계산
annual_min_max_bleaching = filtered_data.groupby('YEAR').agg({
    'MIN_PERCENT_BLEACHED': 'mean',
    'MAX_PERCENT_BLEACHED': 'mean'
}).reset_index()

# 10/1 플롯에 엘니뇨 기간 초록색 점선 추가
special_years = [(1982, 1), (1983, 12), (1995, 1), (1996, 12), (2014, 1), (2016, 12)]


plt.figure(figsize=(10, 6))
plt.plot(annual_min_max_bleaching['YEAR'], annual_min_max_bleaching['MIN_PERCENT_BLEACHED'], label='Average Min Percent Bleached', color='b')
plt.plot(annual_min_max_bleaching['YEAR'], annual_min_max_bleaching['MAX_PERCENT_BLEACHED'], label='Average Max Percent Bleached', color='r')

for year, month in special_years:
    plt.axvline(x=year + (month - 1) / 12, color='lightgreen', linestyle='--', lw=2)

plt.title('Change in Min and Max Coral Bleaching Percent Over Time', fontsize=16, fontweight='bold')
plt.xlabel('Year', fontsize=14)
plt.ylabel('Percentage (%)', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle=':', linewidth=0.7, color='gray')
plt.tight_layout()
plt.show()

# 최소, 최대 백화율에 관한 아이디어 10/1
# articles/Hughes et al. Bleaching ms Feb13.pdf 387번쨰줄 히트맵표현 부분에서 채용

