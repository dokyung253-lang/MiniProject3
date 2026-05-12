import pandas as pd
import matplotlib.pyplot as plt
import korean_font

# csv 파일 읽기
df = pd.read_csv(
    'data/동물보호법 위반.csv',
    header=0,
    encoding='utf-8'
)

# 형변환
for col in ['2023', '2024']:
    df[col] = pd.to_numeric(df[col], errors='coerce')
print(df)

# 파생변수 생성
df['증감률_%'] = (df['2024'] - df['2023']) / df['2023'] * 100
print (df['증감률_%'])