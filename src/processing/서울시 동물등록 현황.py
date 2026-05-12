import pandas as pd
import korean_font

# =====

# [1. 동물등록 현황 데이터 전처리 및 병합]
df_23 = pd.read_csv('./data/2023년 서울시 동물등록 현황.csv', encoding='utf-8')
df_24 = pd.read_csv('./data/2024년 서울시 동물등록 현황.csv', encoding='utf-8')

# 1) 연도 컬럼 부여
df_23['연도'] = 2023
df_24['연도'] = 2024

# 2) 병합, 정제, 형변환
df_pet = pd.concat([df_23, df_24], ignore_index=True)
df_pet['자치구'] = df_pet['자치구'].str.replace(" ", "")

number_cols = ['계', '내장형', '외장형', '인식표']
for col in number_cols:
    df_pet[col] = pd.to_numeric(df_pet[col], errors='coerce').fillna(0)

# =====

# [2. 파생변수: 동물 등록 증가율]
# 1) 분모: 24년 합계 - 23년 합계
df_23_total = df_pet[(df_pet['자치구']=='합계') & (df_pet['연도']==2023)]['계'].values[0]   # 622137
df_24_total = df_pet[(df_pet['자치구']=='합계') & (df_pet['연도']==2024)]['계'].values[0]
df_demo = df_24_total - df_23_total
# '합계' 퇴장
df_pet = df_pet[df_pet['자치구'] != '합계'].copy()

# 2) 23년도 거 계산 쉽게 '작년계' 만들기
df_dict = df_pet[df_pet['연도'] == 2023].set_index('자치구')['계'].to_dict()
df_pet['작년계'] = df_pet['자치구'].map(df_dict)

# 3) 증가율: (올해 계 - 작년 계) / 서울시 전체 증가량 * 100
df_pet['등록증가율(%)'] = ((( df_pet['계'] - df_pet['작년계'] ) / df_demo ) * 100).round(2)

# 4) '작년계' 지우기
df_pet = df_pet.drop(columns=['작년계'])
df_pet = df_pet.reset_index( drop = True )

# =====

# [3. 확인 후 csv 파일로 내보내기]
# 1) 확인
df_pet.info()
print( df_pet.head() )
print( df_pet.tail() )
print( df_pet.isnull().sum() )

# 2) 내보내기
df_pet.to_csv('./data/animal_registration_rate.csv', index=False, encoding='utf-8-sig')