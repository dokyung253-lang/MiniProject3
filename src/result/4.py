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
num_districts = len(districts)

# 자치구 개수만큼 숫자를 생성해서 색상 데이터로 활용]
my_cmap = plt.get_cmap('nipy_spectral' , num_districts)
colors = np.arange(len(df_2024))
cmap='tab20' # 20~25가지 색이 들어있는 팔레트 이름을 지정 (알록달록해짐)
# 산점도 : 펫숍구매비중 대비 등록률

fig, ax = plt.subplots(figsize=(12, 8))
for i, district in enumerate(districts):
    # 해당 자치구 데이터만 필터링
    target_data = df_2024[df_2024['자치구'] == district]
    x = target_data['펫샵_구매비중'].values[0]
    y = target_data['등록증가율(%)'].values[0]
    ax.scatter(
        x , y ,
        s=300,
        alpha=0.6, 
        label=district,  # 여기서 각 구의 이름을 라벨로 지정!
        color=my_cmap(i), # 색상을 순서대로 할당
        edgecolors='gray'
    )
    # 2. 원 옆에 자치구 이름 표시하기
    # x+0.1, y+0.1 처럼 약간의 간격을 주어 글자가 원에 겹치지 않게 합니다.
    ax.text(
        x + 0.2, y + 0.1, 
        district, 
        fontsize=7, 
        fontweight='bold',
        va='bottom',          # 수직 정렬
        ha='left'             # 수평 정렬
    )


df_2024.columns = df_2024.columns.str.strip() 

# 확인을 위해 컬럼명 출력
print("현재 사용 가능한 컬럼명:", df_2024.columns.tolist())
sns.regplot(
    data=df_2024, 
    x='펫샵_구매비중',
    y='등록증가율(%)', 
    scatter=False, 
    ax=ax, 
    color='red', 
    line_kws={'linestyle': '--', 'linewidth': 2},
    label='추세선'
)


    
plt.xlabel('펫숍구매비율')
plt.ylabel('등록률')
plt.title('펫숍구매율 대비 등록률')
plt.legend(bbox_to_anchor=(1.02, 1), ncol=2 , loc='upper left', borderaxespad=0, title='자치구')
plt.tight_layout()
plt.grid(True, linestyle='--', alpha=0.5) # 격자
plt.show()