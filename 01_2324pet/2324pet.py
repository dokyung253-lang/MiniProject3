import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import korean_font

df_23 = pd.read_csv('./01_2324pet/2023년 서울시 동물등록 현황.csv', encoding='utf-8')
df_24 = pd.read_csv('./01_2324pet/2024년 서울시 동물등록 현황.csv', encoding='utf-8')

# 전처리

# 1. 병합
# : 분리된 데이터를 하나로 통합하고 연도 인덱스를 추가
df = pd.concat( [df_23 , df_24], ignore_index=True )
df_23['연도'] = 2023
df_24['연도'] = 2024

print( df.isnull().sum() )

# 2. 정제
# : 자치구 문자의 공백 제거
df['자치구'] = df['자치구'].str.replace(" ", "")

# 3. 형변환
# : 계, 내장형, 외장형, 인식표 주요 수치형 변수는 pd.to_numeric으로 변환
number_cols = ['계', '내장형', '외장형', '인식표']
for col in number_cols:
    df[col] = pd.to_numeric( df[col] , errors='coerce').fillna(0)

# 4. 확인
# df.info()
# print(df.head())
# print( df.isnull().sum() )