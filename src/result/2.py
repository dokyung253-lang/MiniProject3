import pandas as pd
import matplotlib.pyplot as plt
import korean_font

# 데이터 불러오기
reg = pd.read_csv('data/animal_registration_rate.csv')   # 자치구별 등록증가율
vio = pd.read_csv('data/동물보호법_위반_처리결과.csv')   # 전국 단위 위반 건수 증감률

# 2024년도 데이터만 사용 (index 25 이후)
reg_2024 = reg.iloc[25:].copy()

# 1. 자치구별 등록증가율 시각화
plt.figure(figsize=(12,6))
colors = reg_2024['등록증가율(%)'].apply(lambda x: 'green' if x > 0 else 'red')
plt.bar(reg_2024['자치구'], reg_2024['등록증가율(%)'], color=colors)
plt.title("2024 서울 자치구별 반려동물 등록증가율")
plt.xlabel("자치구")
plt.ylabel("등록증가율(%)")
plt.xticks(rotation=45)
plt.show()
