import pandas as pd
import re

## TODO: 결측값 처리방안 모색, Mortality 열에 문자열은 어떻게???

file_path = 'data\Global_Coral_Bleaching_Database.csv'

data = pd.read_csv(file_path)

def convert_percentage_advanced(value):
    if isinstance(value, str):
        # 1. n% 형식: n으로 변환
        if re.match(r'^\d+%$', value):
            return float(value.replace('%', ''))
        
        # 2. >n% 또는 <n% 형식: n으로 변환
        elif re.match(r'[<>]\d+%$', value):
            return float(re.sub(r'[<>]', '', value.replace('%', '')))
        
        # 3. a%-b% 또는 a% - b% 형식: a와 b의 평균을 구해서 변환
        elif re.match(r'^\d+%-\d+%$', value) or re.match(r'^\d+% - \d+%$', value):
            a, b = re.findall(r'\d+', value)
            return (float(a) + float(b)) / 2
        
    return value

data['PERCENT_BLEACHED'] = data['PERCENT_BLEACHED'].apply(convert_percentage_advanced)
data['PERCENT_MORTALITY'] = data['PERCENT_MORTALITY'].apply(convert_percentage_advanced)

data['PERCENT_BLEACHED'].fillna(0, inplace=True)
data['MIN_PERCENT_BLEACHED'].fillna(0, inplace=True)
data['MAX_PERCENT_BLEACHED'].fillna(0, inplace=True)

