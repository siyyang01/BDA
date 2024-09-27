import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Point

import os
os.environ["SHAPE_RESTORE_SHX"] = "YES"
'''
오류
pyogrio.errors.DataSourceError: Unable to open ne_110m_admin_0_countries\Admin0countries.shx or ne_110m_admin_0_countries\Admin0countries.SHX. Set SHAPE_RESTORE_SHX config option to YES to restore or create it.
'''

processed_data = pd.read_csv('data\Processed_Zero_Coral_Bleaching_Database.csv')

max_year_data = processed_data[processed_data['YEAR'] == 1998]

# Geopandas를 이용한 지리 정보 처리
gdf = gpd.GeoDataFrame(max_year_data, geometry=gpd.points_from_xy(max_year_data.LONGITUDE, max_year_data.LATITUDE))

'''
# 세계 지도 불러오기 (Geopandas 내장 데이터) geopandas1.0에서 삭제됨
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
'''
world = gpd.read_file("ne_110m_admin_0_countries\Admin0countries.shp")

fig, ax = plt.subplots(figsize=(12, 8))
world.plot(ax=ax, color='lightgray')
gdf.plot(ax=ax, markersize=gdf['MAX_PERCENT_BLEACHED'], color='red', alpha=0.6) # 산호 백화 데이터

plt.title(f'Coral Bleaching Intensity in {1998}', fontsize=15)
plt.show()
