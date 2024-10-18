import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

el_nino_full = pd.read_csv('MetaAnalysis/metadata/ElNino_FULL_dhw.csv', encoding='ISO-8859-1')

# 연도, 월, 일 열을 datetime 형식으로 변환
el_nino_full.replace('NA', np.nan, inplace=True)

month_map = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
             'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}

el_nino_full['Month.Sampled'] = el_nino_full['Month.Sampled'].map(month_map)

el_nino_full['Day.Sampled'] = el_nino_full['Day.Sampled'].fillna(1)
el_nino_full['Month.Sampled'] = el_nino_full['Month.Sampled'].fillna(1)
el_nino_full['Year.Sampled'] = el_nino_full['Year.Sampled'].fillna(method='ffill')  # 연도는 앞 값으로 채움

el_nino_full['Year.Sampled'] = pd.to_numeric(el_nino_full['Year.Sampled'], errors='coerce').astype(int)
el_nino_full['Month.Sampled'] = pd.to_numeric(el_nino_full['Month.Sampled'], errors='coerce').astype(int)
el_nino_full['Day.Sampled'] = pd.to_numeric(el_nino_full['Day.Sampled'], errors='coerce').astype(int)

el_nino_full['Date'] = pd.to_datetime({
    'year': el_nino_full['Year.Sampled'],
    'month': el_nino_full['Month.Sampled'],
    'day': el_nino_full['Day.Sampled']
})

el_nino_full = el_nino_full.sort_values(by='Date')  # 날짜 기준으로 정렬

el_nino_mean = el_nino_full.groupby('Date', as_index=False)['V11'].mean() # 같은 날짜 DHW평균치 적용
el_nino_mean['V11'] = el_nino_mean['V11'].interpolate(method='linear') # 비어있는 구간 선형보간법으로 이어줌


plt.figure(figsize=(10, 6))
plt.plot(el_nino_mean['Date'], el_nino_mean['V11'], label='MaxDHW (Full Data)',
         color='red', marker='o', markersize=4, linestyle='-', linewidth=1.5)  # 마커와 선 크기 조정

# x축에 날짜 라벨 설정
plt.gca().xaxis.set_major_formatter(plt.matplotlib.dates.DateFormatter('%Y'))
plt.gca().xaxis.set_major_locator(plt.matplotlib.dates.YearLocator(2))  # 2년마다 마커 설정

plt.xticks(rotation=45)  # 라벨이 겹치지 않도록 45도 회전
plt.xlabel('Date')
plt.ylabel('MaxDHW')
plt.title('MaxDHW over Time', fontsize=14, fontweight='bold')
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc='upper left', fontsize=10)
plt.tight_layout()

plt.show()
