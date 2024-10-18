import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import matplotlib.gridspec as gridspec

df = pd.read_csv('MetaAnalysis/metadata/ElNino_FULL_dhw.csv', encoding='ISO-8859-1')
df = df.replace('NA', np.nan)
df['Year.Sampled'] = pd.to_numeric(df['Year.Sampled'], errors='coerce')
df['MaxDHW'] = pd.to_numeric(df['V11'], errors='coerce')
df = df[(df['Year.Sampled'] >= 1997) & (df['Year.Sampled'] <= 1998)].dropna(subset=['Lat.dec', 'Long.dec', 'MaxDHW'])

latitudes = df['Lat.dec']
longitudes = df['Long.dec']
max_dhw = df['MaxDHW']

data = pd.read_csv('data\Processed_Zero_Coral_Bleaching_Database.csv')
max_year_data = data[data['YEAR'] == 1998]

fig = plt.figure(figsize=(12, 12))
gs = gridspec.GridSpec(2, 2, width_ratios=[20, 1], height_ratios=[1, 1], wspace=0.3)

# 첫 번째 플롯: Maximum DHW during El Niño Event (1997-1998)
ax1 = fig.add_subplot(gs[0, 0])
m1 = Basemap(projection='merc', llcrnrlat=-60, urcrnrlat=60, llcrnrlon=-180, urcrnrlon=180, resolution='c', ax=ax1)
m1.drawcoastlines()
m1.drawcountries()
m1.fillcontinents(color='white')
m1.drawmapboundary(fill_color='white')

x, y = m1(longitudes.values, latitudes.values)
sc1 = m1.scatter(x, y, c=max_dhw, cmap='hot', marker='o', s=60, edgecolor='black', alpha=0.75)

axs_cb1 = fig.add_subplot(gs[0, 1])
cb1 = plt.colorbar(sc1, cax=axs_cb1, orientation='vertical')
cb1.set_label('Maximum DHW during El Niño Event', fontsize=12)
ax1.set_title('Maximum DHW 1997-1998 during El Niño Event', fontsize=15)

# 두 번째 플롯: Coral Bleaching Intensity in 1998
ax2 = fig.add_subplot(gs[1, 0])
m2 = Basemap(projection='merc', llcrnrlat=-60, urcrnrlat=60, llcrnrlon=-180, urcrnrlon=180, resolution='c', ax=ax2)
m2.drawcoastlines()
m2.drawcountries()
m2.drawmapboundary()

lons = max_year_data['LONGITUDE'].values
lats = max_year_data['LATITUDE'].values
bleaching = max_year_data['MAX_PERCENT_BLEACHED'].values

x, y = m2(lons, lats)
sc2 = ax2.scatter(x, y, c=bleaching, cmap='coolwarm', s=bleaching, alpha=0.95)

axs_cb2 = fig.add_subplot(gs[1, 1])
cb2 = plt.colorbar(sc2, cax=axs_cb2, orientation='vertical')
cb2.set_label('Coral Bleaching Intensity (%)')

ax2.set_title('Coral Bleaching Intensity in 1998', fontsize=15)

plt.tight_layout()
plt.show()
