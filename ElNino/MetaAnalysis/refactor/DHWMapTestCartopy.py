import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import cartopy.crs as ccrs

lons = np.array([-80, -75, -120, 90, 110])  
lats = np.array([0, 10, -15, -5, 5])        
dhw = np.array([10, 15, 20, 25, 5])         

plt.figure(figsize=(10, 5))

m = Basemap(projection='cyl', resolution='l', 
            llcrnrlat=-30, urcrnrlat=30, llcrnrlon=-180, urcrnrlon=180)
m.drawcoastlines()
m.drawparallels(np.arange(-30, 31, 15), labels=[1, 0, 0, 0])
m.drawmeridians(np.arange(-180, 181, 30), labels=[0, 0, 0, 1])

sc = m.scatter(lons, lats, c=dhw, cmap='hot', latlon=True, s=100, edgecolor='k')

cbar = m.colorbar(sc, location='right', pad='10%')
cbar.set_label('Max DHW during El Niño Event')

plt.title('Maximum DHW during El Niño Event (1997-1998)')
plt.show()
