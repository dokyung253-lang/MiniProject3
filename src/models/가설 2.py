import pandas as pd

# 1. .csv 불러오기
df = pd.read_csv(
    'data/raw_data/동물보호법(23-24).csv',
    header=0,
    usecols=['발생대비 검거건수 (%)', '2023', '2024'],
    encoding= 'utf-8',
    na_values= [' '],
    on_bad_lines='warn'
)
print( df )