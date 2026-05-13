import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import korean_font
import numpy as np

# 동물 취득 경로가 펫숍으로 나타나는 비중이 높은 자치구 일수록 서울 자치구별 반려동물 등록 증가율이 낮을 것이다.
df_동물등록현황 = pd.read_csv('./data/animal_registration_rate.csv')
df_취득경로 = pd.read_csv('./data/wherefrom.csv')

df_취득경로 = df_취득경로.rename( columns={'자치구별':'자치구'})
df_total = pd.merge(
    df_동물등록현황 , df_취득경로, on=['자치구','연도'], how='inner')
print( df_total )