import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import korean_font

df_23 = pd.read_csv('./01_2324pet/2023년 서울시 동물등록 현황.csv', encoding='utf-8')
df_24 = pd.read_csv('./01_2324pet/2024년 서울시 동물등록 현황.csv', encoding='utf-8')

# 전처리

# 1. 연도 속성 추가
df_23['연도'] = 2023
df_24['연도'] = 2024

# 2. 합치기
df = pd.concat( [df_23 , df_24], ignore_index=True )

# 3. 공백제거
df['자치구'] = df['자치구'].str.replace(" ", "")
number_cols = ['계', '내장형', '외장형', '인식표']
for col in number_cols:
    df[col] = pd.to_numeric( df[col] , errors='coerce').fillna(0)


# 4. 확인
# df.info()
# print(df.head())
print( df.isnull().sum() )