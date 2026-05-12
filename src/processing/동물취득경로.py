import pandas as pd
import korean_font

# [1. 동물 취득 경로 데이터 전처리]
df = pd.read_csv(r'./data/동물취득경로.csv', encoding='utf-8')
print( df.head() )
df.info()
print( df.isnull().sum() )