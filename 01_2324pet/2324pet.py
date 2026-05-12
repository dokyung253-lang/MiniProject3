import pandas as pd
import korean_font

# =====
# << 주의 >>
# '서울가구수'는 동물등록률과 관련 없이 서울 자치구 당 전체 가구 수를 의미합니다.
# =====

# [1. 동물등록 현황 데이터 전처리 및 병합]
df_23 = pd.read_csv('./01_2324pet/2023년 서울시 동물등록 현황.csv', encoding='utf-8')
df_24 = pd.read_csv('./01_2324pet/2024년 서울시 동물등록 현황.csv', encoding='utf-8')

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

# [2. 가구수 데이터 평탄화 전처리]
df_h = pd.read_csv('./01_2324pet/seoul_household.csv', skiprows=5, header=None, encoding='utf-8')

# 1) 2023 가구수 데이터 새로 만들기
df_h_23 = df_h[ [1, 2] ].copy()
df_h_23.columns = ['자치구', '서울가구수']
df_h_23['연도'] = 2023

print(df_h)
# 2) 2024 가구수 데이터 새로 만들기
df_h_24 = df_h[ [1, 22] ].copy()
df_h_24.columns = ['자치구', '서울가구수']
df_h_24['연도'] = 2024

# 3) 가구수 데이터 통합
df_household = pd.concat( [df_h_23, df_h_24] , ignore_index=True )
df_household['자치구'] = df_household['자치구'].str.strip()
df_household = df_household[ ~df_household['자치구'].isin( ['소계', '합계'] ) ]

# 4) 가구수 수치 형변환
df_household['서울가구수'] = pd.to_numeric(df_household['서울가구수'].astype(str).str.replace(',', ''), errors='coerce')
#print(df_household)

# =====

# [3. 최종 테이블 (등록률 포함시킨 것)]
# 1) 자치구와 연도 기준 -> 테이블 하나로 병합
df_final = pd.merge( df_pet , df_household , on=['자치구', '연도'], how='inner' )

# 2) 파생변수
df_final['동물등록률'] = ( df_final['계'] / df_final['서울가구수'] ) * 100

print(df_final.head())
print(f"동물등록 데이터 행 개수: {len(df_pet)}")
print(f"최종 병합 데이터 행 개수: {len(df_final)}")
