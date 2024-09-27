# folium 히트맵 테스트

import pandas as pd
import folium
from folium.plugins import HeatMap

data = pd.read_csv('data\Processed_Zero_Coral_Bleaching_Database.csv')

max_year_data = data[data['YEAR'] == 1998]

# 지도 초기화 (초기 위치는 위도와 경도의 평균값으로 설정)
m = folium.Map(location=[max_year_data['LATITUDE'].mean(), max_year_data['LONGITUDE'].mean()], zoom_start=2)

# 백화 강도를 기반으로 히트맵을 그리기 위해 필요한 데이터 준비 (LATITUDE, LONGITUDE, MAX_PERCENT_BLEACHED)
heat_data = [[row['LATITUDE'], row['LONGITUDE'], row['MAX_PERCENT_BLEACHED']] for index, row in max_year_data.iterrows()]
gradient = {
    0.0: 'blue',   
    0.25: 'cyan',   
    0.5: 'lime',    
    0.75: 'yellow', 
    1.0: 'red'       
} # 색상

HeatMap(heat_data, radius=40, blur=15, gradient=gradient, min_opacity=0.5, max_val=100).add_to(m)

# 히트맵이 포함된 지도 저장
m.save("heatmap_coral_bleaching.html")