import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import korean_font  # 한글 폰트 깨짐 방지


# [1. 전처리 완료된 데이터 불러오기]
df_pet = pd.read_csv('./data/animal_registration_rate.csv', encoding='utf-8-sig')
df_report = pd.read_csv('./data/protection_status.csv', encoding='utf-8-sig')

# [2. 두 데이터 형식 통일하고 병합하기 (최종 데이터)]
df_report = df_report.rename(columns={'자치구별': '자치구'})
df_report['자치구'] = df_report['자치구'].astype(str).str.replace(" ", "")
df_pet['자치구'] = df_pet['자치구'].astype(str).str.replace(" ", "")
# '자치구'와 '연도'를 기준으로 병합
df_final = pd.merge(df_pet, df_report, on=['자치구', '연도'], how='inner')
#print(df_final)

# [3. 2024년 데이터만 필터링]
df_24 = df_final[df_final['연도']==2024].copy()

# [4. 회귀, 산점 그래프]
# 1. 크기 설정
plt.figure(figsize=(12,7))
# 2. 산점도
sns.scatterplot(
    data=df_24,
    x='등록증가율(%)',
    y='안락사율',
    hue='자치구',        # 색 나누기
    palette='tab20',    # 색
    s=150,              # size라고 쓰니까 이상하게 나옴
    alpha=0.9,
    edgecolor='white'   # 테두리 색
)
# 3. 회귀선
sns.regplot(
    data=df_24,
    x='등록증가율(%)',
    y='안락사율',
    scatter=False,      # 점 False
    color='tomato',     # 토마토 색
    line_kws={'linewidth':2.5, 'linestyle':'--'}    # 실선 잘 안 보임 -> 점선으로
)
# 4. 기타
plt.title('2024년 서울시 자치구별 반려동물 등록증가율과 안락사율')
plt.xlabel('등록증가율(%)')
plt.ylabel('안락사율')
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0, title='자치구명')
plt.tight_layout()  # 범례 안 잘리게 해줌
plt.savefig('./src/chart/save_chart5.png')
plt.show()