9/26
vscode에서 작성
python 3.9.13 venv 가상환경

사용 패키지
pandas
numpy
matplotlib
sklearn
statsmodel
cartopy
basemap
geopandas
folium


10/1 수정사항 *커밋내역 확인해주세요*

NOAA 사이트에서 bleached, mortality열 N/A값은 백화 현상 발생 관측되지 않은값이라서 0으로 하는게 맞는것같아요

0으로 전처리한 데이터셋으로 그림 수정하겠습니다

ChangeBRegion.py 그래프 같은지역 같은색상 나오게 수정, 시사점 분석 내용 추가

ChangeBYear.py 그래프 의미없는 관측량(1960~1980) 삭제

HeatmapTestFolium.py, heatmap_coral_bleaching.html 우측 상단에 색깔 수치 인디케이터 컬러바 추가

articles:

Hughes et al. Bleaching ms Feb13.pdf: min, max 데이터의 중요성 시사

mcmp_man_part5_references: 선행연구 목록

.

.

10/15 수정사항

갖고있는 데이터만으로는 상관성 입증이 어려운데 찾아보니 메타회귀분석이라는게 있어서 좀 해봤습니다
