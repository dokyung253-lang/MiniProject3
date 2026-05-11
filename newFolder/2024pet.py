import pandas as pd
import matplotlib.pyplot as plt
import koreanfont
import seaborn as sns

df=pd.read_csv("./newFolder/2024년 서울시 동물등록 현황.csv")
df.info()
print(df.isnull().sum())

# 연번,자치구,계,내장형,외장형,인식표