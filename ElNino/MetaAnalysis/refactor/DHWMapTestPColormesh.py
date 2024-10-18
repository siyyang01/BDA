import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

# 위도와 경도 데이터를 2D grid로 변환해야 합니다. 이 예시는 임의의 데이터로 작성.
lons = np.linspace(-180, 180, 180)  # 경도 값
lats = np.linspace(-30, 30, 60)  # 위도 값
lons, lats = np.meshgrid(lons, lats)

# MaxDHW 데이터 예시 (실제로는 준비한 데이터를 사용해야 합니다.)
max_dhw = np.random.uniform(low=0, high=30, size=(60, 180))

# Basemap을 사용한 지도 그리기
fig, ax = plt.subplots(figsize=(12, 5))

m = Basemap(projection='cyl', resolution='c', 
            llcrnrlat=-30, urcrnrlat=30, llcrnrlon=-180, urcrnrlon=180, ax=ax)

m.drawcoastlines()
m.drawparallels(np.arange(-30, 31, 15), labels=[1, 0, 0, 0])
m.drawmeridians(np.arange(-180, 181, 30), labels=[0, 0, 0, 1])

# pcolormesh로 데이터를 그리드에 맞게 부드럽게 표현
mesh = m.pcolormesh(lons, lats, max_dhw, cmap='hot', latlon=True)

# 색상 막대 추가
cbar = m.colorbar(mesh, location='right', pad="10%")
cbar.set_label('Max DHW during El Niño Event')

plt.title('Maximum DHW during El Niño Event (1997-1998)')
plt.show()
