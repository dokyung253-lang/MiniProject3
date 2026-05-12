import pandas as pd
import koreanfont

# [1. 동물 취득 경로 데이터 전처리]
df = pd.read_csv(r'./newFolder/pet_shop_acquisition.csv', encoding='utf-8')
print( df.head() )
df.info()
print( df.isnull().sum() )