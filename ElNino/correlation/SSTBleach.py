# SST와 백화강도의 상관관계

import pandas as pd

sst_data = pd.read_csv('data\SSTAnomalies.csv')
bleaching_data = pd.read_csv('data\Processed_Zero_Coral_Bleaching_Database.csv')

combined_data = pd.merge(sst_data, bleaching_data, on='YEAR')

# 결합된 데이터 확인
# print(combined_data.head())

# SST anomalies와 MAX_PERCENT_BLEACHED 사이의 상관관계
# correlation = combined_data[['ANOM', 'MAX_PERCENT_BLEACHED']].corr()
# print(correlation)

'''
                          ANOM  MAX_PERCENT_BLEACHED
ANOM                  1.000000              0.040714
MAX_PERCENT_BLEACHED  0.040714              1.000000
'''

# 해수면 온도와 MAX_PERCENT_BLEACHED 사이의 상관관계
# correlation = combined_data[['TOTAL', 'MAX_PERCENT_BLEACHED']].corr()
# print(correlation)

'''
TOTAL                 1.000000              0.037725
MAX_PERCENT_BLEACHED  0.037725              1.000000
'''


# YEAR 열을 기준으로 두 데이터 병합
combined_data_updated = pd.merge(sst_data, bleaching_data, on='YEAR', how='inner')

# 병합된 데이터를 새로운 CSV 파일로 저장
combined_data_updated.to_csv('updated_combined_SST_bleaching_data.csv', index=False)