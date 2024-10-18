import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

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

plt.figure(figsize=(10, 8))

m = Basemap(projection='merc', llcrnrlat=-30, urcrnrlat=30, llcrnrlon=-180, urcrnrlon=180, resolution='i')

m.drawcoastlines()
m.fillcontinents(color='lightgray', lake_color='aqua')
m.drawmapboundary(fill_color='aqua')

x, y = m(longitudes.values, latitudes.values)
sc = m.scatter(x, y, c=max_dhw, cmap='hot', marker='o', s=50, edgecolor='k', alpha=0.7)

plt.colorbar(sc, label='MaxDHW')

plt.title('Maximum DHW during El Niño Event (1997-1998)', fontsize=15)
plt.show()
