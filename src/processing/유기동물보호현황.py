import pandas as pd
import matplotlib.pyplot as plt
import korean_font
import seaborn as sns


# 유기동물보호현황

# 유기동물보호현황

# csv 파일 호출
data1 = pd.read_csv(r'./data/유기동물보호현황.csv' , encoding='utf-8-sig' )

# 판다스 병합
df = pd.concat( [data1] , ignore_index=True )

# 확인
df.info()
print( df.head() )

# 결측치 확인
print( df.isnull().sum() )  # 결측치 : 

# 결측치 -> 0으로 변환
df = df.replace( '-' ,  0 )


print(df)

# 컬럼 이름 새로 짓기 (2024.1 대신 분석하기 쉬운 이름으로)
col_names = [ '자치구별' , '합계' , '개_소계' , '개_인도(주인)' , '개_입양_기증' , '개_폐사안락사' , '개_계류방사' , 
                   '고양이_소계' , '고양이_인도(주인)' , '고양이_입양_기증' , '고양이_폐사안락사' , '고양이_계류방사' ,
                   '기타_소계' , '기타_인도(주인)' , '기타_입양_기증' , '기타_폐사안락사' , '기타_계류방사' ]

# iloc[ [ 시작할인덱스 : 끝인덱스 ] , 수정컬럼인덱스 ] = [ 새로운값 ]
df_2023 = df.iloc[ :, [1] + list(range(2,18)) ].copy()
df_2023.columns = col_names
df_2023['연도'] = 2023



df_2024 = df.iloc[ :, [1] + list(range(18,34)) ].copy()
df_2024.columns = col_names
df_2024['연도'] = 2024


df_final = pd.concat([df_2023 , df_2024] , ignore_index=True )

df_final = df_final[~df_final['자치구별'].str.contains('소계|합계|자치구' , na=False)]
# 번호(인덱스)가 중간에 비지 않게 새로 매기기
df_final = df_final.reset_index(drop=True)
df_final = df_final[~df_final['자치구별'].str.contains('소계|합계|자치구' , na=False)]
# 번호(인덱스)가 중간에 비지 않게 새로 매기기
df_final = df_final.reset_index(drop=True)

for col in col_names[1:]:
    df_final[col] = pd.to_numeric( df_final[col] , errors='coerce' ).fillna(0)


# 항목별 리스트화
categories = ['소계','인도(주인)','입양_기증','폐사안락사','계류방사']

for category in categories :
    df_final[f'전체_{category}'] = df_final[f'개_{category}'] + df_final[f'고양이_{category}'] + df_final[f'기타_{category}']


# 가설 : 서울 자치구별 반려동물 등록률이 높은 자치구의 경우, 안락사의 비율은 낮을 것이다.
# 안락사율
df_final['안락사율'] = (df_final['전체_폐사안락사'] / df_final['전체_소계'] * 100).fillna(0)

target_cols = ['자치구별', '연도', '안락사율'] + [f'전체_{category}' for category in categories]
df_report = df_final[target_cols].copy()
print("------------------------------------- 유기동물보호현황 -------------------------------------")
print(df_report.head())
print(df_report.info())

# 가설 : 서울 자치구별 반려동물 등록률이 높을수록 유기 보호 동물 수는 줄어들 것이다.
# 유기 동물 보호수

# 23년
df_2023 = df_report[df_report['연도'] == 2023]
rank_2023 = df_2023[ ['자치구별', '전체_소계'] ].sort_values(by='전체_소계')
print("-------- 23년 자치구별 유기 동물 보호수 현황 --------")
print( rank_2023 )

# 24년
df_2024 = df_report[df_report['연도'] == 2024]
rank_2024 = df_2024[ ['자치구별', '전체_소계'] ].sort_values(by='전체_소계')
print("-------- 24년 자치구별 유기 동물 보호수 현황 --------")
print( rank_2024 )


print("-------- 23년 자치구별 안락사율 현황 --------")
print( df_report[df_report['연도'] == 2023].sort_values(by='안락사율'))
print("-------- 24년 자치구별 안락사율 현황 --------")
print( df_report[df_report['연도'] == 2024].sort_values(by='안락사율'))
