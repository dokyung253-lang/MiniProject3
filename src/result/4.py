import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import korean_font
import numpy as np

# 동물 취득 경로가 펫숍으로 나타나는 비중이 높은 자치구 일수록 서울 자치구별 반려동물 등록 증가율이 낮을 것이다.
df_동물등록현황 = pd.read_csv('./data/animal_registration_rate.csv')
df_취득경로 = pd.read_csv('./data/wherefrom.csv')


df_취득경로 = df_취득경로.rename( columns={'자치구별':'자치구'})
df_total = pd.merge(
    df_동물등록현황 , df_취득경로, on=['자치구','연도'], how='inner')
print( df_total )
df_total['펫샵_구매비중'] = pd.to_numeric(df_total['펫샵_구매비중'].astype(str).str.replace(" ", ""), errors='coerce').fillna(0)
df_2024 = df_total[ df_total['연도']  == 2024 ].sort_values('자치구')

districts = df_2024['자치구'].unique()
# 자치구 개수만큼 숫자를 생성해서 색상 데이터로 활용]
my_cmap = plt.get_cmap('tab20')
colors = np.arange(len(df_2024))
cmap='tab20' # 20~25가지 색이 들어있는 팔레트 이름을 지정 (알록달록해짐)
# 산점도 : 펫숍구매비중 대비 등록률

fig, ax = plt.subplots(figsize=(12, 8))
for i, district in enumerate(districts):
    # 해당 자치구 데이터만 필터링
    target_data = df_2024[df_2024['자치구'] == district]
    
    ax.scatter(
        target_data['펫샵_구매비중'], 
        target_data['등록증가율(%)'], 
        s=target_data['등록증가율(%)'] * 100, 
        alpha=0.6, 
        label=district,  # 여기서 각 구의 이름을 라벨로 지정!
        color=my_cmap(i % 20), # 색상을 순서대로 할당
        edgecolors='gray'
    )


    
plt.xlabel('펫숍구매비율')
plt.ylabel('등록률')
plt.title('펫숍구매율 대비 등록률')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0, title='자치구')
plt.tight_layout()
plt.show()