import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import korean_font

# 서울 자치구별 반려동물 등록 증가율이 높을 수록, 해당 지역에서 구조된 유기동물의 반환율은 높을 것이다.
# 등록율: (자치구별 전체 유기동물 중 등록번호가 있는 수) / (자치구별 전체 유기동물 수)
# 반환율: (자치구별 전체 유기동물 중 상태가 '반환'인 수) / (자치구별 전체 유기동물 수)

df_list = pd.read_csv("./data/반환상태크롤링.csv", encoding='utf-8') 
df_stat_all = pd.read_csv("./data/protection_status.csv", encoding='utf-8')

# protection에서 2024년 자료만
df_stat_2024 = df_stat_all[df_stat_all['연도'] == 2024].copy()
df_stat_2024 = df_stat_2024.rename(columns={'자치구별': '자치구'})
df_stat_2024['자치구'] = df_stat_2024['자치구'].str.strip()

# 반환상태크롤링에서 2024년 자료만
df_list['연도_추출'] = df_list['공고번호'].str.split('-').str[2].astype(int)
df_list_2024 = df_list[df_list['연도_추출'] == 2024].copy()

# 서울-은평이면 하이픈 제거하고 @@구로 변경
df_list_2024['자치구'] = (df_list_2024['공고번호'].str.split('-').str[1] + "구") .str.replace("구구", "구")

# 2024년 등록 번호 있는 것만
df_list_2024['등록여부'] = df_list_2024['등록번호'].notna() & (df_list_2024['등록번호'].astype(str).str.strip() != "")
df_reg_2024 = df_list_2024[df_list_2024['등록여부'] == True].groupby('자치구').size().reset_index(name='등록번호_보유수')

df_final_2024 = pd.merge(df_stat_2024, df_reg_2024, on='자치구', how='left')

# 계산
df_final_2024['등록번호_보유수'] = df_final_2024['등록번호_보유수'].fillna(0).astype(int)
df_final_2024['등록율'] = (df_final_2024['등록번호_보유수'] / df_final_2024['전체_소계']) * 100
df_final_2024['반환율'] = (df_final_2024['전체_인도(주인)'] / df_final_2024['전체_소계']) * 100

# ============================================================================================

# 등록율 기준으로 내림차순
df_sorted = df_final_2024.sort_values(by='등록율', ascending=False)

# 등록율
regi = sns.barplot(data=df_sorted, x='자치구', y='등록율', color='skyblue', label='등록율 (%)')
regi.set_ylabel('등록율 (%)', fontsize=14, color='blue')
regi.tick_params(axis='y', labelcolor='blue')

# 반환율
retu = regi.twinx()
sns.lineplot(data=df_sorted, x='자치구', y='반환율', color='red', marker='o', linewidth=2, ax=retu, label='반환율 (%)')
retu.set_ylabel('반환율 (%)', fontsize=14, color='red')
retu.tick_params(axis='y', labelcolor='red')

# 범례
lines, labels = regi.get_legend_handles_labels()
lines2, labels2 = retu.get_legend_handles_labels()
retu.legend(lines + lines2, labels + labels2, loc='upper right', fontsize=12)

plt.title('2024년 서울 자치구별 유기동물 등록율 및 반환율 비교')

plt.show()
# plt.savefig('./파일명/save_chart6.png')