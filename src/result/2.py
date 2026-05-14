import pandas as pd
import matplotlib.pyplot as plt
import korean_font

# 데이터 불러오기
reg = pd.read_csv('data/animal_registration_rate.csv')   # 자치구별 등록증가율
vio = pd.read_csv('data/동물보호법_위반_처리결과.csv')   # 전국 단위 위반 건수 증감률

# 2024년도 데이터만 사용 (index 25 이후)
reg_2024 = reg.iloc[25:].copy()

# 서울 전체 평균 등록증가율 계산
seoul_rate = reg_2024['등록증가율(%)'].mean()

# 전국 단위 위반 건수 증감률 추출
vio_rate = float(vio.loc[0, '증감률_%'])  # 예: -4.18%

# 두 지표를 하나의 그래프로 비교
plt.figure(figsize=(8,6))
plt.bar_label(
        plt.bar(['동물등록증가율 평균(%)', '동물보호법 위반건수 증가율(%)'], [seoul_rate, vio_rate],
                color=['skyblue','salmon']), 
        fmt='%.2f%%', label_type='center'
)        
plt.axhline(0, color='gray', linestyle='--')
plt.title("서울시 반려동물등록률과 위반률 변화")
plt.ylabel("증가율(%)")
plt.legend()
plt.show()
plt.savefig('./src/chart/save_chart2.png')
