import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression

# sklearn normalize 사라져서 데이터 미리 전처리
from sklearn.preprocessing import StandardScaler

# LinearRegression 결측치 처리해야함
from sklearn.impute import SimpleImputer

# 데이터 불러오기
# utf-8로 인코딩 안돼있어서 ISO-8859-1로씀
ElNino_FULL = pd.read_csv(r"MetaAnalysis/metaData/ElNino_FULL_dhw.csv", encoding='ISO-8859-1')
ElNino_afteronly = pd.read_csv(r"MetaAnalysis/metaData/ElNino_afteronly_dhw.csv", encoding='ISO-8859-1')

#.loc를 사용하여 슬라이스된 DataFrame에 값 설정
ElNino_FULL.loc[:, 'Cover_Diff'] = ElNino_FULL['Mean_Cover_Before'] - ElNino_FULL['Mean_Cover_Resp']

# 변환 작업
ElNino_FULL['ACC'] = ElNino_FULL['ACC'].astype('category')
ElNino_afteronly['ACC'] = ElNino_afteronly['ACC'].astype('category')

# 열 이름 변경
ElNino_FULL.rename(columns={'V8': 'DHWnow',
                            'V9': 'MaxDHW_beforeafter',
                            'V10': 'TimeLag_beforeafter',
                            'V11': 'MaxDHW',
                            'V12': 'TimeLag',
                            'V13': 'SSTnow',
                            'V14': 'SSTmean',
                            'V15': 'SSTvar',
                            'V16': 'SSTstd',
                            'V17': 'MMM',
                            'V18': 'MMMind'}, inplace=True)

ElNino_afteronly.rename(columns={'V8': 'DHWnow',
                                'V9': 'MaxDHW_beforeafter',
                                'V10': 'TimeLag_beforeafter',
                                'V11': 'MaxDHW',
                                'V12': 'TimeLag',
                                'V13': 'SSTnow',
                                'V14': 'SSTmean',
                                'V15': 'SSTvar', 
                                'V16': 'SSTstd',
                                'V17': 'MMM',
                                'V18': 'MMMind'}, inplace=True)

# 변동성 및 기타 통계계산
change = ElNino_FULL[['ACC', 'Mean_Cover_Before', 'Mean_Cover_Resp']]
change['Cover_Diff'] = ElNino_FULL['Mean_Cover_Before'] - ElNino_FULL['Mean_Cover_Resp']
change = change.dropna()

abs_max_change = change['Cover_Diff'].max()
p_change = (change['Cover_Diff'] / change['Mean_Cover_Before']) * 100
p_max_change = p_change.max()

max_bleach = ElNino_afteronly['Mean_Bleaching_Resp'].max()

# 0으로 표시된 표준편차에 0.1 추가
ElNino_FULL['SD_Cover_Before'] = ElNino_FULL['SD_Cover_Before'].replace(0, 0.1)
ElNino_FULL['SD_Bleaching_Before'] = ElNino_FULL['SD_Bleaching_Before'].replace(0, 0.1)
ElNino_FULL['SD_Cover_Resp'] = ElNino_FULL['SD_Cover_Resp'].replace(0, 0.1)
ElNino_FULL['SD_Bleaching_Resp'] = ElNino_FULL['SD_Bleaching_Resp'].replace(0, 0.1)
ElNino_afteronly['SD_Bleaching_Resp'] = ElNino_afteronly['SD_Bleaching_Resp'].replace(0, 0.1)

# 분석을 위한 데이터 서브셋팅
cover = ElNino_FULL[ElNino_FULL['Parameter'] == "Cover"]
cover = cover.dropna(subset=['SD_Cover_Before', 'SD_Cover_Resp'])

bleaching = ElNino_FULL[ElNino_FULL['Parameter'] == "Bleaching"]
bleaching = bleaching.dropna(subset=['SD_Bleaching_Resp'])

# 데이터 결합 및 시뮬레이션 데이터 생성
ElNino_afteronly['Mean_Bleaching_Before_sim'] = ElNino_afteronly['Mean_Bleaching_Before'].fillna(5)
ElNino_afteronly['SD_Bleaching_Before_sim'] = ElNino_afteronly['SD_Bleaching_Before'].fillna(15)

# 메타 분석 모델 계산
def run_meta_analysis(data, formula):
    model = sm.OLS.from_formula(formula, data)
    results = model.fit()
    return results

cover_formula = 'Cover_Diff ~ MaxDHW + TimeLag + SSTmean + SSTvar'
cover_model = run_meta_analysis(cover, cover_formula)

# glmulti 대체: GridSearchCV로 모델 선택
X = cover[['MaxDHW', 'TimeLag', 'SSTmean', 'SSTvar']]
y = cover['Cover_Diff']

# 결측치 대체
imputer = SimpleImputer(strategy='mean')
X_imputed = imputer.fit_transform(X)

# 'normalize' 매개변수 제거 및 데이터 스케일링 추가
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_imputed)

param_grid = {
    'fit_intercept': [True, False],
    #'normalize': [True, False]
}

regressor = LinearRegression()
grid_search = GridSearchCV(regressor, param_grid, cv=5, scoring='neg_mean_squared_error')
grid_search.fit(X_scaled, y) ## normalize 대체

# 최적 모델 출력
best_model = grid_search.best_estimator_
print(f"Best model: {best_model}")

# 전체 효과 크기 계산
overall_effect_size = np.mean(cover['Cover_Diff'])
print(f"Overall effect size: {overall_effect_size}")

# 모델 출력 요약
print(cover_model.summary())

# 그래프 생성 (Profile plots)
plt.figure(figsize=(6, 6))
plt.subplot(2, 1, 1)
plt.plot(cover['MaxDHW'], cover['Cover_Diff'], 'o')
plt.title('MaxDHW vs Cover Difference')
plt.xlabel('MaxDHW')
plt.ylabel('Cover Difference')

plt.subplot(2, 1, 2)
plt.plot(cover['SSTmean'], cover['Cover_Diff'], 'o')
plt.title('SSTmean vs Cover Difference')
plt.xlabel('SSTmean')
plt.ylabel('Cover Difference')

plt.tight_layout()
plt.savefig("cover_profileplots.png")
plt.show()

# 저장
cover.to_csv("data/ElNino_after_processing.csv")
