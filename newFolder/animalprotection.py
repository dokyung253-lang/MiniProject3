import pandas as pd
import matplotlib.pyplot as plt
import koreanfont
import seaborn as sns


# 유기동물보호현황

# csv 파일 호출
data1 = pd.read_csv(r'./newFolder/유기동물보호현황.csv' , encoding='utf-8-sig' )

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

for col in col_names[1:]:
    df_final[col] = pd.to_numeric( df_final[col] , errors='coerce' ).fillna(0)


# 항목별 리스트화
categories = ['소계','인도(주인)','입양_기증','폐사안락사','계류방사']

for category in categories :
    df_final[f'전체_{category}'] = df_final[f'개_{category}'] + df_final[f'고양이_{category}'] + df_final[f'기타_{category}']



target_cols = ['자치구별' , '연도'] + [f'전체_{category}' for category in categories]

df_report = df_final[target_cols].copy()

print("------------------------------------- 유기동물보호현황 -------------------------------------")
print(df_report.head())
print(df_report.info())