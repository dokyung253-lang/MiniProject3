import pandas as pd
import matplotlib.pyplot as plt
import korean_font

# csv 파일 읽기
df = pd.read_csv(
    'data/동물보호법 위반.csv',
    header=0,
    encoding='utf-8'
)

# 결측치 대체
df['동물보호법_위반건수'] = df['동물보호법_위반건수'].replace('U', 'unknown')

# 형변환
for col in ['2023', '2024']:
    df[col] = pd.to_numeric(df[col], errors='coerce')
print(df)

# 파생변수 생성
df['증감률(%)'] = (df['2024'] - df['2023']) / df['2023'] * 100
print (df['증감률(%)'])

# CSV 파일로 내보내기
df.to_csv('data/동물보호법_위반_처리결과.csv', index=False, encoding='utf-8-sig')