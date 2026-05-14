import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import korean_font
import numpy as np

# 가설 3 : 서울 자치구별 반려동물등록 증가율이 높을수록 유기 보호 동물 수는 줄어들 것이다.

df_동물등록현황 = pd.read_csv('./data/animal_registration_rate.csv')
df_유기동물보호현황 = pd.read_csv('./data/protection_status.csv')


df_유기동물보호현황 = df_유기동물보호현황.rename( columns={'자치구별':'자치구'})
df_total = pd.merge(
    df_동물등록현황 , df_유기동물보호현황, on=['자치구','연도'], how='inner')
print( df_total )

df_2024 = df_total[ df_total['연도']  == 2024 ].sort_values('자치구')


x_indexes = np.arange(len(df_2024['자치구'])) # X축 위치를 숫자로 변환 (막대를 옆으로 밀기 위해 필수)
width = 0.4 # 막대 너비

fig, ax = plt.subplots(figsize=(10, 5))




ax.bar( x_indexes - 0.2 , df_2024['전체_소계']  , width=width ,  color = 'aqua' , label = '유기동물보호수' )
ax.bar( x_indexes + 0.3 , df_2024['등록증가율(%)'] , width=width , color = "#FFADE6" , label = '등록증가율(%)')

# 보호수 평균선 (하늘색 점선)
avg_protection = df_2024['전체_소계'].mean()
ax.axhline(avg_protection, color='darkcyan', linestyle='--', linewidth=1, label='보호수 평균')

ax.set_xticks(x_indexes)
ax.set_xticklabels(df_2024['자치구'], rotation=45)

ax.legend(loc='upper right',ncol=2) # 범례 표시

plt.title('2024년 자치구별 유기동물보호수와 동물등록증가율 그래프') 
plt.tight_layout()
plt.show()

plt.savefig('./src/chart/save_chart3.png')