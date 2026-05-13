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




ax.bar( x_indexes - 0.2 , df_2024['안락사율']  , width=width ,  color = 'blue' , label = '안락사율(%)' )
ax.bar( x_indexes + 0.3 , df_2024['등록증가율(%)'] , width=width , color = 'green' , label = '등록증가율(%)')

ax.set_xticks(x_indexes)
ax.set_xticklabels(df_2024['자치구'], rotation=45)

ax.legend() # 범례 표시

plt.title('2024년 자치구별 안락사율과 동물등록증가율 그래프') 
plt.tight_layout()
plt.show()

