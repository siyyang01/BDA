import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.widgets import Slider, Button
import numpy as np

file_path = 'data/Global_Coral_Bleaching_Database.csv'
data = pd.read_csv(file_path)

filtered_data = data[['YEAR', 'LATITUDE', 'LONGITUDE', 'MAX_PERCENT_BLEACHED']].dropna()

# 전구투영법
fig = plt.figure(figsize=(12, 8))
ax = plt.axes(projection=ccrs.PlateCarree())
plt.subplots_adjust(left=0.1, bottom=0.25)  # 슬라이더 공간 추가

ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')

year = 1998
year_data = filtered_data[filtered_data['YEAR'] == year]

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

# 오른쪽 컬러바
cbar = plt.colorbar(sc, label='Max Percent Bleached')

title = plt.title(f'Coral Bleaching in {year}')

ax_slider = plt.axes([0.1, 0.1, 0.65, 0.03])  # 슬라이더 위치
year_slider = Slider(ax_slider, 'Year', int(filtered_data['YEAR'].min()), int(filtered_data['YEAR'].max()), valinit=year, valstep=1)

ax_button = plt.axes([0.8, 0.025, 0.1, 0.04])  # 버튼 위치
play_button = Button(ax_button, 'Play')

# 슬라이더 업뎃
def update(val):
    year = int(year_slider.val)
    title.set_text(f'Coral Bleaching in {year}')
    year_data = filtered_data[filtered_data['YEAR'] == year]
    sc.set_offsets(np.c_[year_data['LONGITUDE'], year_data['LATITUDE']])
    sc.set_array(year_data['MAX_PERCENT_BLEACHED'])
    plt.draw()

year_slider.on_changed(update)

# 재생
playing = [False]

def play(event):
    if not playing[0]:
        playing[0] = True
        while playing[0]:
            current_year = int(year_slider.val)
            if current_year < filtered_data['YEAR'].max():
                year_slider.set_val(current_year + 1)
            else:
                playing[0] = False
            plt.pause(0.5)  # 속도 조절

def stop(event):
    playing[0] = False

play_button.on_clicked(play)

plt.show()
