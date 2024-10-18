import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# 데이터 불러오기 (1997-1998년도의 데이터만 필터링)
df = pd.read_csv('MetaAnalysis/metadata/ElNino_FULL_dhw.csv', encoding='ISO-8859-1')

# 결측치 처리 및 연도 필터링 (1997-1998년)
df = df.replace('NA', np.nan)
df['Year.Sampled'] = pd.to_numeric(df['Year.Sampled'], errors='coerce')
df['MaxDHW'] = pd.to_numeric(df['V11'], errors='coerce')
df = df[(df['Year.Sampled'] >= 1997) & (df['Year.Sampled'] <= 1998)].dropna(subset=['Lat.dec', 'Long.dec', 'MaxDHW'])

# Lat.dec와 Long.dec를 경위도로 사용하고, MaxDHW를 색으로 표시
latitudes = df['Lat.dec']
longitudes = df['Long.dec']
max_dhw = df['MaxDHW']

# 지도 그리기
plt.figure(figsize=(12, 8))

# Basemap 설정 (위도, 경도 범위 설정)
m = Basemap(projection='cyl', llcrnrlat=-30, urcrnrlat=30, llcrnrlon=-180, urcrnrlon=180, resolution='c')

# 해안선, 대륙 그리기
m.drawcoastlines()
m.drawcountries()
m.fillcontinents(color='white', lake_color='aqua')
m.drawmapboundary(fill_color='aqua')

# 위도 경도 선 추가
m.drawparallels(np.arange(-30., 31., 15.), labels=[True, False, False, False])
m.drawmeridians(np.arange(-180., 181., 60.), labels=[False, False, False, True])

# 데이터 플롯 (위도를 Mercator 좌표계에 맞게 변환)
x, y = m(longitudes.values, latitudes.values)
sc = m.scatter(x, y, c=max_dhw, cmap='hot', marker='o', s=60, edgecolor='black', alpha=0.75)

# 색상 막대 추가
cb = plt.colorbar(sc, orientation='vertical', pad=0.05)
cb.set_label('Maximum DHW during El Niño Event', fontsize=12)

# 제목 추가
plt.title('Maximum DHW 1997-1998 during El Niño Event', fontsize=15)
plt.show()
