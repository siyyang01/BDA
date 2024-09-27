import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

file_path = 'data\Global_Coral_Bleaching_Database.csv'
data = pd.read_csv(file_path)

filtered_data = data[['YEAR', 'LATITUDE', 'LONGITUDE', 'MAX_PERCENT_BLEACHED']].dropna()

year = 1998
year_data = filtered_data[filtered_data['YEAR'] == year]

# 전구투영법
fig = plt.figure(figsize=(12, 8))
ax = plt.axes(projection=ccrs.PlateCarree())

ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')

sc = plt.scatter(
    year_data['LONGITUDE'],
    year_data['LATITUDE'],
    c=year_data['MAX_PERCENT_BLEACHED'],
    cmap='Reds',
    s=50,
    transform=ccrs.PlateCarree(),
    edgecolor='k',
    alpha=0.7
)

plt.colorbar(sc, label='Max Percent Bleached')

plt.title(f'Coral Bleaching in {year}')
plt.show()