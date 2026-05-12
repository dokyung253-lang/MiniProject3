import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import korean_font  # 한글 폰트 깨짐 방지


# [1. 전처리 완료된 데이터 불러오기]
df_pet = pd.read_csv('./data/animal_registration_rate.csv', encoding='utf-8-sig')
df_report = pd.read_csv('./data/protection_status.csv', encoding='utf-8-sig')

# [2. 두 데이터 병합하기 (최종 데이터)]
df_report = df_report.rename(columns={'자치구별': '자치구'})
df_report['자치구'] = df_report['자치구'].astype(str).str.replace(" ", "")
df_pet['자치구'] = df_pet['자치구'].astype(str).str.replace(" ", "")

# '자치구'와 '연도'를 기준으로 병합
df_final = pd.merge(df_pet, df_report, on=['자치구', '연도'], how='inner')
