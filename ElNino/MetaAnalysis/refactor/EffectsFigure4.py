import numpy as np
import matplotlib.pyplot as plt
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri

pandas2ri.activate()

'''
R_HOME must be set in the environment or Registry 오류:
R 설치경로 환경변수 설정해줘야함

터미널에
setx R_HOME "C:\Program Files\R\R-4.3.2"
(R버전입력)
입력 후 재부팅 or 터미널 재시작
'''

robjects.r['load']('MetaAnalysis/metadata/ElNino.RData')

# R 객체에서 데이터 추출
cover_rma_1yr = robjects.r['cover.rma.1yr']
bleaching_rma = robjects.r['bleaching.rma']
bl_est = robjects.r['bl.est']
bl_lb = robjects.r['bl.lb']
bl_ub = robjects.r['bl.ub']
cov_1yr_est = robjects.r['cov.1yr.est']
cov_1yr_lb = robjects.r['cov.1yr.lb']
cov_1yr_ub = robjects.r['cov.1yr.ub']

# 효과 크기와 95% 신뢰 구간 값 설정
all_cov = cover_rma_1yr.rx2('b')[0].item()
all_bl = bleaching_rma.rx2('b')[0].item()
overall = [all_bl, all_cov]

lb_res_cov = float(cover_rma_1yr.rx2('ci.lb')[0])
ub_res_cov = float(cover_rma_1yr.rx2('ci.ub')[0])
lb_res_bl = float(bleaching_rma.rx2('ci.lb')[0])
ub_res_bl = float(bleaching_rma.rx2('ci.ub')[0])

fig, axs = plt.subplots(3, 1, figsize=(8, 12))

# Panel 1: 전체 모델
axs[0].plot([lb_res_bl, ub_res_bl], [0.7, 0.7], color='black', linewidth=2)
axs[0].plot([lb_res_cov, ub_res_cov], [0.3, 0.3], color='darkred', linewidth=2)
axs[0].scatter(overall, [0.7, 0.3], color=['black', 'darkred'], s=100)
axs[0].axvline(x=0, color='grey', linestyle='--')
axs[0].set_xlim([-2.5, 2.5])
axs[0].text(2.2, 0.7, "Bleaching*", fontsize=12)
axs[0].text(2.2, 0.3, "Cover**", fontsize=12)
axs[0].text(-2.5, 0.9, "a)", fontsize=14)
axs[0].set_xlabel("Standardized Mean Difference ± 95% CI")
axs[0].set_yticks([])

# Panel 2: Bleaching 모델과 조정 변수
# .lb값을 못가져오는 오류가 있어서 직접 지정해야함
# ElNino.Rdata에서 직접 가져온 값들
# 이하 내용들도 동일
full_bl = [bl_est[2].item(), bl_est[1].item()]
lb_bl_tmean = 0.00427929198659888
ub_bl_tmean = 0.399197595993162
lb_bl_timelag = -0.00110958440088402
ub_bl_timelag = -2.52970784442735e-05


axs[1].plot([lb_bl_timelag, ub_bl_timelag], [0.7, 0.7], color='black', linewidth=2)
axs[1].plot([lb_bl_tmean, ub_bl_tmean], [0.3, 0.3], color='black', linewidth=2)
axs[1].scatter(full_bl, [0.7, 0.3], color='black', s=100)
axs[1].axvline(x=0, color='grey', linestyle='--')
axs[1].set_xlim([-1.1, 1.1])
axs[1].set_yticks([])
axs[1].text(-0.5, 0.7, "TimeLag:MaxDHW*", fontsize=12)
axs[1].text(-0.5, 0.3, "SSTmean*", fontsize=12)
axs[1].text(-1.1, 0.9, "b)", fontsize=14)

# Panel 3: 피복도(Cover) 모델과 조정 변수
full_cov = [float(cov_1yr_est[1]), float(cov_1yr_est[2])]
lb_cov_dhw = -0.0861672289200438
ub_cov_dhw = -0.0259957176620859
lb_cov_tmean = -0.745941871051528
ub_cov_tmean = -0.266254377159495

axs[2].plot([lb_cov_dhw, ub_cov_dhw], [0.7, 0.7], color='darkred', linewidth=2)
axs[2].plot([lb_cov_tmean, ub_cov_tmean], [0.3, 0.3], color='darkred', linewidth=2)
axs[2].scatter(full_cov, [0.7, 0.3], color='darkred', s=100)
axs[2].axvline(x=0, color='grey', linestyle='--')
axs[2].set_xlim([-1.1, 1.1])
axs[2].set_yticks([])
axs[2].text(0.5, 0.7, "MaxDHW***", fontsize=12, color="darkred")
axs[2].text(0.5, 0.3, "SSTmean***", fontsize=12, color="darkred")
axs[2].text(-1.1, 0.9, "c)", fontsize=14)

plt.tight_layout()
plt.savefig("MetaAnalysis/refactor/figures/Fig4.png")
plt.show()
