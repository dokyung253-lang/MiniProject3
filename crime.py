import korean_font
import pandas as pd

df = pd.read_csv(
    './crime(23-24).csv',
    header=0,
    usecols=['발생대비 검거건수 (%)', '2023년', '2024년'],
    encoding= 'CP949',
    na_values= [' '],
    on_bad_lines='warn'
)
print( df )