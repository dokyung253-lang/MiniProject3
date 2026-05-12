import pandas as pd
import korean_font

# [1. 동물 취득 경로 데이터 전처리]
df = pd.read_csv('pet_shop_acquisition.csv', encoding='utf-8')
print( df.head() )


# 1) 연도 컬럼 부여
#df['연도'] = 