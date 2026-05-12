import pandas as pd
import korean_font

# [1. 동물 취득 경로 데이터 전처리]
df = pd.read_csv(r'./data/반려동물취득경로.csv', encoding='utf-8')
print( df.head() )
df.info()
print( df.isnull().sum() )

# 결측치 -> 0으로 변환
df = df.replace( '-' ,  0 )

print( df )

col_names = ['자치구별', '펫샵구매', '친척친구_무료', '친척친구_유료', '인터넷구매', '유기동물입양', '반려동물의 자식', '기타']

# 23 펫샵구매+인터넷구매
buy_2023 = df.iloc[ : , [1] + list(range(2,9)) ].copy()
buy_2023.columns = col_names
for col in col_names[1: ] :
    buy_2023[col] = pd.to_numeric( buy_2023[col] , errors='coerce' ).fillna(0)

buy_2023['펫샵_구매'] = buy_2023['펫샵구매'] + buy_2023['인터넷구매']
buy_2023['연도'] = 2023


# 24
buy_2024 = df.iloc[ : , [1] + list(range(9,16)) ].copy()
buy_2024.columns = col_names
for col in col_names[1: ] :
    buy_2024[col] = pd.to_numeric( buy_2024[col] , errors='coerce' ).fillna(0)
buy_2024['펫샵_구매'] = buy_2024['펫샵구매'] + buy_2024['인터넷구매']
buy_2024['연도'] = 2024



buy_final = pd.concat([buy_2023,buy_2024],ignore_index=True)
buy_final = buy_final[~buy_final['자치구별'].str.contains('구분별|지역소분류', na=False)]


print( buy_final )

# 총합
path_cols = col_names = ['펫샵구매' ,'친척친구_무료', '친척친구_유료', '유기동물입양', '반려동물의 자식', '기타']
buy_final['총합'] = buy_final[path_cols].sum(axis=1)

# 펫샵구매율
buy_final['펫샵_구매비중'] = (buy_final['펫샵_구매']/buy_final['총합'] * 100).fillna(0)


# 펫샵 나머지
buy_final['그외_구매비중'] = 100 - buy_final['펫샵_구매비중']


buy_report = buy_final[['자치구별' , '연도' , '펫샵_구매비중' , '그외_구매비중']]

print( buy_report )