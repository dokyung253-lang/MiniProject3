import pandas as pd
import matplotlib.pyplot as plt
import koreanfont
import seaborn as sns


# csv 파일 호출
data1 = pd.read_csv('./newFolder/유기동물보호+현황_20260511160816.csv' , encoding='cp949' )

# 판다스 병합
df = pd.concat( [data1] , ignore_index=True )

# 확인
df.info()
print( df.head() )


