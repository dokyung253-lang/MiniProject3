import pandas as pd
import matplotlib.pyplot as plt
import korean_font

# csv 파일 읽기
df = pd.read_csv(
    'data/raw_data/동물보호법(23-24).csv',
    header=0,
    encoding='CP949'
)

# 형변환
for col in ['2023', '2024']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

print(df.dtypes)
print(df)

# 1. .csv 내보내기
df.to_csv(
   'data/raw_data/동물보호법(23-24).csv',  # 파일경로
    index = False,           # 인덱스 제외
    encoding='utf-8',        # 인코딩 지정
    na_rep='U',              # 결측값 치환
    header= True             # 헤더(열이름) 포함 여부
)

