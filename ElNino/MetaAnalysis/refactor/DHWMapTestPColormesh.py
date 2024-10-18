'''
폐기
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

lons = np.linspace(-180, 180, 180) 
lats = np.linspace(-30, 30, 60) 
lons, lats = np.meshgrid(lons, lats)

max_dhw = np.random.uniform(low=0, high=30, size=(60, 180))

fig, ax = plt.subplots(figsize=(12, 5))

m = Basemap(projection='cyl', resolution='c', 
            llcrnrlat=-30, urcrnrlat=30, llcrnrlon=-180, urcrnrlon=180, ax=ax)

m.drawcoastlines()
m.drawparallels(np.arange(-30, 31, 15), labels=[1, 0, 0, 0])
m.drawmeridians(np.arange(-180, 181, 30), labels=[0, 0, 0, 1])

mesh = m.pcolormesh(lons, lats, max_dhw, cmap='hot', latlon=True)

cbar = m.colorbar(mesh, location='right', pad="10%")
cbar.set_label('Max DHW during El Niño Event')

plt.title('Maximum DHW during El Niño Event (1997-1998)')
plt.show()
'''
