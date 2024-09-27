# matplotlib + basemap 테스트

import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np

data = pd.read_csv('data\Processed_Zero_Coral_Bleaching_Database.csv')

max_year_data = data[data['YEAR'] == 1998]

# 지도 생성
fig, ax = plt.subplots(figsize=(12, 8))
m = Basemap(projection='merc', llcrnrlat=-60, urcrnrlat=60, llcrnrlon=-180, urcrnrlon=180, resolution='c')

# 지형 그리기
m.drawcoastlines()
m.drawcountries()
m.drawmapboundary()

lons = max_year_data['LONGITUDE'].values
lats = max_year_data['LATITUDE'].values
bleaching = max_year_data['MAX_PERCENT_BLEACHED'].values

x, y = m(lons, lats)

# 히트맵 플롯
sc = ax.scatter(x, y, c=bleaching, cmap='coolwarm', s=bleaching, alpha=0.95)

# 컬러바 추가
cbar = plt.colorbar(sc, ax=ax, orientation='vertical', fraction=0.03, pad=0.04)
cbar.set_label('Coral Bleaching Intensity (%)')

plt.title(f'Coral Bleaching Intensity in 1998', fontsize=15)
plt.show()
