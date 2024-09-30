import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("data\Processed_Zero_Coral_Bleaching_Database.csv")

data['MIN_PERCENT_BLEACHED'] = pd.to_numeric(data['MIN_PERCENT_BLEACHED'], errors='coerce')
data['MAX_PERCENT_BLEACHED'] = pd.to_numeric(data['MAX_PERCENT_BLEACHED'], errors='coerce')



regional_min_max_bleaching = data.groupby(['COUNTRY', 'YEAR']).agg({
    'MIN_PERCENT_BLEACHED': 'mean',
    'MAX_PERCENT_BLEACHED': 'mean'
}).reset_index()

selected_countries = ['Australia', 'Fiji', 'Indonesia']

regional_selected = regional_min_max_bleaching[regional_min_max_bleaching['COUNTRY'].isin(selected_countries)]

# 같은 지역 같은 색으로 나오게 수정 10/1 (min max 점선, 실선으로 구분)
'''
# 색상 리스트 해서 zip으로 구현
colors = ['b', 'g', 'r']
'''

# 색상 지정
colors = {
    'Australia': 'b',
    'Fiji': 'g',
    'Indonesia': 'r'
}

plt.figure(figsize=(10, 6))

# zip 트라이 10/1 X
for country in selected_countries:
    country_data = regional_selected[regional_selected['COUNTRY'] == country]
    
    plt.plot(country_data['YEAR'], country_data['MIN_PERCENT_BLEACHED'], label=f'{country} Min Percent Bleached', color=colors[country], linestyle='-', linewidth=2, marker='o')
    
    plt.plot(country_data['YEAR'], country_data['MAX_PERCENT_BLEACHED'], label=f'{country} Max Percent Bleached', color=colors[country], linestyle='--', linewidth=2, marker='s')


# 그래프 조정 10/1 (ChangeBYear.py랑 동일)
plt.title('Regional Change in Min and Max Coral Bleaching Percent Over Time', fontsize=16, fontweight='bold')
plt.xlabel('Year', fontsize=14)
plt.ylabel('Percentage (%)', fontsize=14)
plt.xticks(fontsize=12)
plt.yticks(fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, linestyle=':', linewidth=0.7, color='gray')
plt.tight_layout()
plt.show()

'''
10/1 시사점 분석

Australia(blue):
백화 비율이 낮은 수준을 유지하며 대부분의 기간 동안 0%에 가깝습니다.
2000년대 후반과 2010년대 중반에 백화 비율이 소폭 증가하는 경향을 보였지만, 여전히 낮은 수준에서 유지됩니다.
최대 백화 비율이 약간 상승한 몇 개의 시점이 있지만, 전체적으로 Australia에서 백화가 가장 심하지 않았음을 알 수 있습니다.

Fiji(green):
2000년대 초반에 백화 비율이 급증했으며, 최대 백화 비율이 60%를 넘습니다.
2010년대 중반에도 백화 비율이 급격히 상승하는 모습이 보입니다. 이는 환경 스트레스 요인이 이 시기에 크게 작용했음을 시사합니다.
최소 백화 비율도 한동안 50% 이상을 기록하며, Fiji의 산호초가 상당한 백화 피해를 입었음을 나타냅니다.


Indonesia(red):
다른 지역에 비해 꾸준한 백화 현상이 관찰됩니다.
특히 2000년대 후반부터 2010년대 초반까지 최대 백화 비율이 상승하는 경향을 보입니다. 이 시기에는 백화가 심각했으며, 최대 백화 비율이 20~30% 이상을 기록하는 모습을 보였습니다.
최소 백화 비율도 지속적으로 나타나는 것으로 보아, 광범위한 지역에서 백화가 발생했음을 의미합니다


Australia의 경우, 전체적으로 백화 비율이 낮은 수준에서 유지되며 산호초의 백화가 비교적 덜 발생한 지역으로 보입니다.

Fiji는 주기적인 환경 스트레스로 인해 백화 비율이 급증하는 경향을 보입니다. 특히 2000년대 초반과 2010년대 중반에 백화가 매우 심각했던 것을 알 수 있습니다.
이는 엘니뇨 현상이나 해수 온도 상승과 같은 환경 요인과 관련이 있을 가능성이 큽니다.

Indonesia는 꾸준한 백화 현상을 겪고 있는 것으로 보이며, 일부 연도에 백화 비율이 크게 증가합니다.
이 지역의 산호초가 지속적인 환경적 스트레스를 받고 있을 가능성을 시사합니다.
'''